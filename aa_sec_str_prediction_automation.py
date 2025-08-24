import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Paths
input_folder = "uniprot amino acid sequences"
output_folder = "secondary structure prediction"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Initialize the browser driver
service = Service("C:\\Users\\91630\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    # Open the MIX tool website
    driver.get("http://cib.cf.ocha.ac.jp/bitool/MIX/")

    # Click on the "Chou-Fasman" link
    chou_fasman_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Chou-Fasman"))
    )
    chou_fasman_link.click()

    # Process each amino acid sequence file
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Process only text files
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_aa_pred.txt")

            try:
                # Read the amino acid sequence from the file
                with open(input_file, "r", encoding="utf-8") as f:
                    sequence = f.read().strip()

                # Locate the textarea and paste the sequence
                textarea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "seq"))
                )
                textarea.clear()
                textarea.send_keys(sequence)

                # Submit the form
                submit_button = driver.find_element(By.XPATH, "//input[@value='Submit']")
                submit_button.click()

                # Wait for the results to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "pre"))
                )
                result = driver.find_element(By.TAG_NAME, "pre").text

                # Save the result to a text file
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result)

                print(f"Processed: {filename}")

                # Go back to the Chou-Fasman page for the next sequence
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Chou-Fasman"))
                ).click()

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

finally:
    # Close the browser
    driver.quit()
    print("Browser session closed.")

print("Processing complete. Results are saved in the 'secondary structure prediction' folder.")
