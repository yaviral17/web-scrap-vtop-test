import base64
import os
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO


def getValueFromENV(key):
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if key in line:
                    return line.split('=')[1].strip()
    except:
        key = input(f'Enter the value for {key}: ')
        with open('.env', 'a') as f:
            f.write(f'{key}={key}\n')
        return key
    


def extract_text_from_image(image_path):
    import easyocr

    # Create an OCR reader object
    reader = easyocr.Reader(['en'])

    # Read text from an image
    result = reader.readtext(image_path)

    # Print the extracted text
    return ' '.join([text[1] for text in result])

def check_if_logged_in(driver):
    try:
        for h4 in driver.find_elements(By.TAG_NAME, 'h4'):
            if 'VTOP Login' in h4.text:
                return False
        return True
    except:
        return True # Already logged in

# Setup webdriver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
wait = WebDriverWait(driver, 10)  # Add this line

driver.get('https://vtop.vitbhopal.ac.in/vtop/open/page')

# Find the button of type submit, class name 'btn btn-primary fw-bold' and click it
button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
button.click()

# Find the captcha image and print the src attribute
while True:
    captcha = driver.find_elements(By.TAG_NAME, 'img')
    while len(captcha) <= 1:
        driver.refresh()
        captcha = driver.find_elements(By.TAG_NAME, 'img')
        # sleep(2)
        print('Refreshing...')

    for c in captcha:
        captcha = c.get_attribute('src')
        print(captcha)
        if 'data:image/jpeg;base64' in captcha:
            captcha = captcha.split(",")[1]
            image_data = base64.b64decode(captcha)
            image = Image.open(BytesIO(image_data))
            # Save the image
            image.save('captcha.jpeg')

    uname = getValueFromENV('VIT_USERNAME')
    pwd = getValueFromENV('VIT_PASSWORD')

    # Print the extracted text
    # print(f'Captcha: {extract_text_from_image("captcha.jpeg")}')
    captcha_from_image = extract_text_from_image("captcha.jpeg").replace(' ', '')
    # input(f'Press Enter to continue... Captcha: {captcha_from_image} Username: {uname} Password: {pwd}')
    captcha = ''
    if len(captcha_from_image) != 6:
        driver.refresh()
        continue # Get the captcha from the user
    else:
        captcha = captcha_from_image
    print(f'Username: {uname} Password: {pwd} Captcha: {captcha}')
    print(f'Logged in: {check_if_logged_in(driver)}')
    driver.find_element(By.ID, 'username').send_keys(uname)
    driver.find_element(By.ID, 'password').send_keys(pwd)
    driver.find_element(By.ID, 'captchaStr').send_keys(captcha  )
    driver.find_element(By.ID, 'submitBtn').click()
    if check_if_logged_in(driver):
        break
print("\n"*10+'Logged in successfully...')
# sleep(2)
lst = driver.find_elements(By.TAG_NAME, 'button')
for l in driver.find_elements(By.TAG_NAME, 'button'):
    if l.get_attribute('data-bs-target') == '#expandedSideBar':
        l.click()
        break
for l in driver.find_elements(By.TAG_NAME, 'button'):
    if l.get_attribute('data-bs-target') == '#acMenuCollapseHDG0070':
        l.click()
        break


for l in driver.find_elements(By.TAG_NAME, 'a'):
    print(l.get_attribute('data-url'))
    if l.get_attribute('data-url') == 'examinations/OfflineStudExamSchedule':
        # make sure the element is interactable before clicking
        driver.execute_script("arguments[0].click();", l)



        break


sleep(1)

for l in driver.find_elements(By.TAG_NAME, 'button'):
    print(l.text)
    if l.text == '☰':
        driver.execute_script("arguments[0].click();", l)
        break
select = driver.find_element(By.ID, 'semesterSubId')

for i in range(len(select.find_elements(By.TAG_NAME, 'option'))):
    print(f'{i}: {select.find_elements(By.TAG_NAME, "option")[i].text}')
sem = 3
# sem = int(input('Enter the semester number: '))
select.find_elements(By.TAG_NAME, 'option')[sem].click()

select2 = driver.find_element(By.ID, 'examtype')
for i in range(len(select2.find_elements(By.TAG_NAME, 'option'))):
    print(f'{i}: {select2.find_elements(By.TAG_NAME, "option")[i].text}')
exam = 4
# exam = int(input('Enter the exam type number: '))
select2.find_elements(By.TAG_NAME, 'option')[exam].click()

for l in driver.find_elements(By.TAG_NAME, 'a'):
    print(l.text)
    if l.text == 'submit':
        # make sure the element is interactable before clicking
        driver.execute_script("arguments[0].click();", l)
        break


tableRow = driver.find_elements(By.TAG_NAME, 'tr')
# save the webpage

with open('exam_schedule.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
    f.close()



input('Press Enter to continue...')
# Get and print the page source after the click
# print(driver.page_source)


driver.quit()
exit()
