from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

driver.get("http://localhost:3000")
time.sleep(3)

username_field = driver.find_element(By.XPATH, "//*[@id='root']/div/section/div/div/div/div/form/div[1]/input") 
username_field.send_keys("root")
time.sleep(3)

password_field = driver.find_element(By.XPATH, "//*[@id='root']/div/section/div/div/div/div/form/div[2]/input")
password_field.send_keys("root")
time.sleep(3)

login_button = driver.find_element(By.XPATH, "//*[@id='root']/div/section/div/div/div/div/form/div[3]/button")
login_button.click()
time.sleep(3)

test_results = {}

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/nav/a/div"))
    )
    test_results["Login Test"] = "Passed"

    print("Login successful. Dashboard page loaded successfully.")
except:
    test_results["Login Test"] = "Failed"
    print("Login failed or dashboard page did not load.")


#Search function test
try:
    search_queries = ["ko8021", "bfy"]
    i=1
    for search_query in search_queries:

        search_input = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[3]/div[2]/input")
        search_input.clear()
        search_input.send_keys(search_query)

        time.sleep(3)

        table = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div[3]/table")
        rows = table.find_elements(By.XPATH,"//*[@id='root']/div/div/div[3]/table/tbody")
        for row in rows:
            # Get the text of all cells in the row
            cells = row.find_elements(By.TAG_NAME,"td")
            row_text = ' '.join(cell.text for cell in cells)
            if search_query.lower() not in row_text.lower():
                raise AssertionError(f"Search query '{search_query}' not found in table row: {row_text}")

    

    test_results["Search Test"] = "Passed"
except Exception as e:
    test_results["Search Test"] = "Failed"


# Violated Details function test
try:
    violated_detail_button = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div/div[2]/nav/ul/a[2]/a/li/div") 
    violated_detail_button.click()
    time.sleep(5)

    title_present = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div[3]/p").text
    if "Violated Details" in title_present:
        table = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div[3]/table")
        test_results["Violated Details Test"] = "Passed"

except Exception as e:
    test_results["Test 2"] = "Failed: " + str(e)


# All Vehicle details function test
try:
    All_Vehicle_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/nav/ul/a[1]/a/li/div') 
    All_Vehicle_button.click()
    time.sleep(2)
    table = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div[3]/table")
    test_results["All Vehicle Details Test"] = "Passed"

except Exception as e:
    test_results["Test 3"] = "Failed: " + str(e)

time.sleep(1)

# Add details function test
try:
 
    Add_detail_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div[1]/div[2]/div/button') 
    Add_detail_button.click()
    time.sleep(5)

    name_field = driver.find_element(By.XPATH, "//*[@id='formBasicName']")
    name_field.send_keys("Kamal Priyanjith")

    vehicle_number_field = driver.find_element(By.XPATH, "//*[@id='formBasicVN']")
    vehicle_number_field.send_keys("GO1321")

    email_field = driver.find_element(By.XPATH, "//*[@id='formBasicEmail']")
    email_field.send_keys("rre@asdsdaad.com")

    time.sleep(5)

    Submit_button = driver.find_element(By.XPATH, "//*[@id='root']/div/div/form/button") 
    Submit_button.click()

    time.sleep(5)

    alert = driver.switch_to.alert
    alert_text = alert.text
    if(alert_text == "Success: Vehicle details added successfully"):
        test_results["Add All Vehicle Test"] = "Passed"
    if(alert_text == "Error: Invalid Vehicle Number"):
        test_results["Vehicle Number Validation Test"] = "Passed"
  

except Exception as e:
    test_results["Add All Vehicle Test"] = "Failed: " + str(e)



# Print all tests and their results
for test, result in test_results.items():
    print(test + ":", result)

# Close the browser
driver.quit()