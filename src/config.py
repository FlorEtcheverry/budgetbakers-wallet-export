from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import os

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILE_PATH = os.path.join(_ROOT, "site", "Wallet by BudgetBakers.html")

def configuration():
    service = Service(executable_path=os.path.join(_ROOT, "geckodriver", "geckodriver"))
    options = webdriver.FirefoxOptions()
    options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(service=service, options=options)
    return driver

