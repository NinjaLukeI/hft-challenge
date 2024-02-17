from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.chrome.options import Options
import base64
from simplemachine import SimpleMachine


chrome_options = Options()

chrome_options.add_experimental_option("detach", True)

chrome_options.set_capability("goog:loggingPrefs", {
    "browser": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

driver.get("www.challenge.com") # replacing site name to keep challenge secure. need to import name from a gitignore file later
driver.execute_script("""
    var y = document.getElementsByClassName("answer-panel");
                      y[0].style.visibility = "visible";
                      """)

values = []

for i in range(8):
    number_box_id = f"number-box-{i}"
    value = driver.find_element(By.ID, number_box_id).get_attribute("textContent")
    value = re.sub("[^0-9]", "", value)
    values.append(value)

answer_field = driver.find_element(By.ID, "answer")
name_field = driver.find_element(By.ID, "name")

print(values)

answer_field.send_keys("".join(values))
name_field.send_keys("Luke Ibeachum")

button = driver.find_element(By.XPATH, "/html/body/div/div[2]/button")
button.click()

time.sleep(4)

instructions = []


# get console messages
for entry in driver.get_log('browser'):
    val = entry["message"].strip()
    result = re.search('"(.*)"', val)
    if result:
        # print(result.group())
        instructions.append(result.group())

d_instructions = []

# decoded instructions
for instruction in instructions:
    result = re.search('"(.*)"', instruction)
    if result:
        d_instructions.append(base64.b64decode(result.group()).decode('utf-8').strip('"'))

# removing task description and END instruction
d_instructions.pop(0)
d_instructions.pop()

# debugging
print(d_instructions[1]) 

machine = SimpleMachine()

machine.execute_program(d_instructions)

result = machine.sum_registers()

result = base64.b64encode(result.encode())

# debugging
print(result)

script = "ws.send('{}')".format(result.decode())

# debugging
print(script)

driver.execute_script(script)

