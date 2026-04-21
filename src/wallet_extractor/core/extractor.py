"""
Main wallet data extractor class.

Supports both the legacy CSS-module UI (Selenium) and the current
Mantine/Tailwind UI (BeautifulSoup) used by BudgetBakers Wallet.
"""

import json
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

from ..models.transaction import Transaction
from ..utils.date_utils import parse_date_with_year, determine_transaction_type


class WalletExtractor:
    """
    Extracts transaction data from BudgetBakers Wallet HTML files.

    For the current Mantine-based export format, parsing is done entirely
    with BeautifulSoup (no browser needed).  The legacy CSS-module format
    still uses Selenium.
    """

    def __init__(self, driver=None):
        self.driver = driver
        self.transactions: List[Transaction] = []

    def load_html_file(self, file_path: str):
        self._file_path = file_path
        if self.driver:
            self.driver.get(f"file://{file_path}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_transactions(self, skip_divs: int = 5) -> List[Transaction]:
        self.transactions = []

        with open(self._file_path, "r", encoding="utf-8") as f:
            raw = f.read(4096)

        is_mantine = "mantine" in raw or "grid-cols-record-row" in raw

        if is_mantine:
            self._extract_mantine()
        else:
            self._extract_legacy()

        return self.transactions

    # ------------------------------------------------------------------
    # Mantine / Tailwind UI  (2025-04+)  –  BeautifulSoup
    # ------------------------------------------------------------------

    def _extract_mantine(self):
        print("Parsing HTML (this may take a moment for large files)...")
        with open(self._file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")

        # Date headers have class "sticky … top-[114px]"
        date_headers = [
            h for h in soup.select("div.sticky")
            if "top-[114px]" in (h.get("class") or [])
        ]
        print(f"Found {len(date_headers)} date sections")

        total = 0
        for header in date_headers:
            p = header.find("p")
            date_text = p.get_text(strip=True) if p else "Unknown"

            row_container = header.find_next_sibling("div")
            if not row_container:
                continue

            rows = row_container.select(
                "div[class*='grid-cols-record-row-withCheckbox']"
            )
            for row in rows:
                total += 1
                if total % 500 == 0:
                    print(f"Processing transaction {total}...")
                txn = self._parse_mantine_row(row, date_text)
                if txn:
                    self.transactions.append(txn)

        print(f"Processed {total} transaction rows")

    @staticmethod
    def _parse_mantine_row(row: Tag, raw_date: str) -> Optional[Transaction]:
        try:
            texts = row.select("p.mantine-Text-root")

            md_texts = [t for t in texts if t.get("data-size") == "md"]
            sm_texts = [t for t in texts if t.get("data-size") == "sm"]

            category = md_texts[0].get_text(strip=True) if md_texts else ""

            account = ""
            description = ""
            for t in sm_texts:
                text = t.get_text(strip=True)
                if not text:
                    continue
                if t.select_one("span.rounded-full"):
                    account = text
                elif "dimmed" in (t.get("style") or "") and not description:
                    description = text

            amount = ""
            for t in reversed(md_texts):
                span = t.select_one("span")
                if span:
                    amount = span.get_text(strip=True)
                    break

            labels = [
                l.get_text(strip=True)
                for l in row.select("span.mantine-Pill-label")
                if l.get_text(strip=True)
            ]

            if not category and not amount:
                return None

            return Transaction(
                category=category,
                account=account,
                amount=amount,
                description=description,
                payee="",
                labels=labels,
                date=parse_date_with_year(raw_date),
                transaction_type=determine_transaction_type(amount, description),
                raw_date=raw_date,
            )
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Legacy CSS-module UI  –  Selenium
    # ------------------------------------------------------------------

    _LEGACY = {
        "main_container": ".VypTY5DQ_tmahm5VdHFJK",
        "transaction": "._3wwqabSSUyshePYhPywONa",
        "date": ".MhNEgOnlVNRo3U-Ti1ZHP",
    }

    def _extract_legacy(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from ..utils.dom_utils import extract_payee_and_labels, parse_transaction_text_lines

        if not self.driver:
            raise RuntimeError(
                "Legacy HTML format requires a Selenium WebDriver. "
                "Pass a driver to WalletExtractor()."
            )

        wait = WebDriverWait(self.driver, 30)
        main_container = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self._LEGACY["main_container"])
            )
        )

        print("Finding all transaction elements...")
        elements = main_container.find_elements(
            By.CSS_SELECTOR, self._LEGACY["transaction"]
        )
        print(f"Found {len(elements)} transaction elements")

        for i, elem in enumerate(elements):
            if i % 500 == 0:
                print(f"Processing transaction {i+1}/{len(elements)}...")

            current_date = self._find_legacy_date(elem)
            text_lines = elem.text.split("\n")
            if len(text_lines) < 3:
                continue

            category, account, description, amount = parse_transaction_text_lines(text_lines)
            payee, labels = extract_payee_and_labels(elem)

            self.transactions.append(Transaction(
                category=category,
                account=account,
                amount=amount,
                description=description,
                payee=payee,
                labels=labels,
                date=parse_date_with_year(current_date),
                transaction_type=determine_transaction_type(amount, description),
                raw_date=current_date,
            ))

    def _find_legacy_date(self, trans_elem) -> str:
        from selenium.webdriver.common.by import By

        current = trans_elem
        for _ in range(3):
            try:
                parent = current.find_element(By.XPATH, "..")
                try:
                    date_elem = parent.find_element(
                        By.CSS_SELECTOR, self._LEGACY["date"]
                    )
                    return date_elem.text
                except Exception:
                    pass
                current = parent
            except Exception:
                break
        return "Unknown"

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------

    def save_to_json(self, output_path: str, indent: int = 2):
        transaction_dicts = [t.to_dict() for t in self.transactions]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transaction_dicts, f, indent=indent, ensure_ascii=False)

    def get_statistics(self) -> dict:
        total = len(self.transactions)
        with_payee = len([t for t in self.transactions if t.has_payee()])
        with_labels = len([t for t in self.transactions if t.has_labels()])

        income_count = len([t for t in self.transactions if t.is_income()])
        expense_count = len([t for t in self.transactions if t.is_expense()])
        transfer_count = len([t for t in self.transactions if t.is_transfer()])

        return {
            "total_transactions": total,
            "transactions_with_payee": with_payee,
            "transactions_with_labels": with_labels,
            "income_transactions": income_count,
            "expense_transactions": expense_count,
            "transfer_transactions": transfer_count,
            "payee_coverage": f"{(with_payee/total*100):.1f}%" if total > 0 else "0%",
            "label_coverage": f"{(with_labels/total*100):.1f}%" if total > 0 else "0%",
        }