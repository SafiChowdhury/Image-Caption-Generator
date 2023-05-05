import random
import time

from pyhtmlreport import Report
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

report = Report()

driver: WebDriver = webdriver.Chrome()
report.setup(
    report_folder=r'Reports',
    module_name='Device',
    release_name='Test V1',
    selenium_driver=driver
)

driver.get('http://127.0.0.1:8000/')
#Test Case 1
try:
    report.write_step(
        'Go to Landing Page',
        status = report.status.Start,
        test_number=1
    )
    assert(driver.title=='Image Caption Generator')
    report.write_step(
        'Landing Page Loaded Successfully.',
        status=report.status.Pass,
        screenshot=True
    )
except AssertionError:
    report.write_step(
        'Landing Page loaded Successfully.',
        status=report.status.Fail,
        screenshot=True
    )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status= report.status.Warn,
        screenshot=True
    )
#Test Case 2
try:
    report.write_step(
    'Uploading Photo',
    status=report.status.Start,
    test_number=2
    )
    file_input = driver.find_element(By.CLASS_NAME,"btn btn-secondary").click()
    file_input.send_keys("F:/Saafi/New folder/Flicker8k_Dataset/102455176_5f8ead62d5.jpg")

    # find and click the submit button to upload the file
    submit_button = driver.find_element(By.CLASS_NAME,"btn btn-info")
    submit_button.click()

    # wait for the page to load
    time.sleep(5)
    report.write_step(
        'Successfully Uploaded',
        status=report.status.Pass,
        screenshot=True
    )
except AssertionError:
    report.write_step(
        'Failed to Upload',
        status=report.status.Fail,
        screenshot=True
    )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
    )
#Test Case 3
try:
    report.write_step(
        'Clicking Generate Caption Button',
        status = report.status.Start,
        test_number=3
    )
    submit_button = driver.find_element(By.CLASS_NAME, "btn btn-info")
    submit_button.click()
    report.write_step(
        'Button Clicked',
        status=report.status.Pass,
        screenshot=True
    )
except AssertionError:
    report.write_step(
        'Button Clicked.',
        status=report.status.Fail,
        screenshot=True
    )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status= report.status.Warn,
        screenshot=True
    )
#Test Case 4
driver.get('http://127.0.0.1:8000/Caption')
try:
    report.write_step(
        'Going back to Home page',
        status = report.status.Start,
        test_number=4
    )
    submit_button = driver.find_element(By.CLASS_NAME, "btn btn-info")
    submit_button.click()
    report.write_step(
        'Home Page Loaded Successfully.',
        status=report.status.Pass,
        screenshot=True
    )
except AssertionError:
    report.write_step(
        'Home Page loaded Successfully.',
        status=report.status.Fail,
        screenshot=True
    )
except Exception as e:
    report.write_step(
        'Something went wrong!</br>{e}',
        status= report.status.Warn,
        screenshot=True
    )
finally:
    report.generate_report()
    driver.quit()