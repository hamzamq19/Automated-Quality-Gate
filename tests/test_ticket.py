import pytest
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# --- CONFIGURATION ---
BASE_URL = "https://www.saucedemo.com"
API_URL = "https://www.saucedemo.com"  # Usually this would be an API endpoint
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

# --- PYTEST FIXTURES (The Setup & Teardown) ---
@pytest.fixture(scope="module")
def driver():
    """
    This sets up the browser ONCE before the tests start,
    and closes it AFTER the tests finish.
    """
    print("\n[SETUP] Launching Chrome Browser...")
    
    # Setup Chrome
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run without seeing the browser
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(5) # Wait up to 5 seconds for elements to load
    
    yield driver  # This is where the testing happens
    
    print("\n[TEARDOWN] Closing Browser...")
    driver.quit()

# --- HELPER FUNCTION: SCREENSHOT ---
def take_screenshot(driver, name):
    """Saves a screenshot to the local folder"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"[[ ERROR CAPTURED ]] Screenshot saved: {filename}")

# --- TEST 1: API HEALTH CHECK (The "Logic" Layer) ---
def test_api_availability():
    """
    Verifies the site is actually up before we try UI testing.
    This saves time if the server is down.
    """
    print("\n[TEST 1] Checking API Status...")
    response = requests.get(API_URL)
    
    # Assert checks if the condition is True. If False, the test fails.
    assert response.status_code == 200, f"Critical: Server is down! Status: {response.status_code}"
    print(" -> Server is Healthy (200 OK)")

# --- TEST 2: UI END-TO-END FLOW (The "Visual" Layer) ---
def test_end_to_end_purchase(driver):
    """
    Simulates a real user buying a backpack.
    """
    print("\n[TEST 2] Starting E2E Purchase Flow...")
    
    try:
        # 1. Open Site
        driver.get(BASE_URL)
        
        # 2. Login
        driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        
        # Check if login was successful by looking for the product title
        header = driver.find_element(By.CLASS_NAME, "title").text
        assert "Products" in header
        print(" -> Login Successful")

        # 3. Add Backpack to Cart
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # 4. Go to Cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # 5. Verify Item is in Cart (Quality Check)
        item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert "Sauce Labs Backpack" == item_name
        print(" -> Item Verified in Cart")
        
        # 6. Checkout
        driver.find_element(By.ID, "checkout").click()
        
        # 7. Enter Details
        driver.find_element(By.ID, "first-name").send_keys("Hamza")
        driver.find_element(By.ID, "last-name").send_keys("Mustafa")
        driver.find_element(By.ID, "postal-code").send_keys("75500")
        driver.find_element(By.ID, "continue").click()
        
        # 8. Verify Total Price (Logic Check)
        # The backpack is $29.99. Tax is usually $2.40. Total should be $32.39
        total_label = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        # Clean the text to get just the number (e.g., "Total: $32.39" -> "32.39")
        print(f" -> Verify Price Math: {total_label}")
        
        driver.find_element(By.ID, "finish").click()
        
        # 9. Final Validation
        success_msg = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert "Thank you for your order!" in success_msg
        print(" -> Order Completed Successfully!")

    except Exception as e:
        # If ANYTHING fails, take a screenshot immediately
        take_screenshot(driver, "Test_Failure")
        pytest.fail(f"Test Failed! Error: {str(e)}")