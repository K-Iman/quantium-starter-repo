from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

def pytest_setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options

def pytest_configure(config):
    driver_path = ChromeDriverManager().install()
    os.environ["PATH"] = os.path.dirname(driver_path) + os.pathsep + os.environ["PATH"]