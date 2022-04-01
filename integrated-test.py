from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
# to get console.log
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service


def is_error(entry):
    return entry['level'] in ['ERROR']  # or add higher level


def show_log(entries):
    errors = list(filter(is_error, entries))

    if not errors:
        return

    print("log:")
    for e in errors:
        print(f"ERROR: {e['message']}")

    raise Exception(str(errors))


# You may know your chromedriver's path using `chromedriver-path` command
chromedriver_path = "/opt/homebrew/lib/python3.9/site-packages/chromedriver_binary/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument('--headless')

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['logginPrefs'] = {'browser': 'ALL'}

chrome_service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=chrome_service,
                          options=options, desired_capabilities=desired_capabilities)

print("start /register")
# access /register
# click #register-start
driver.get('http://localhost/register')

email_input = driver.find_element(By.ID, 'email_input')
email_input.send_keys('akakou@example.com')

register_start = driver.find_element(By.ID, 'register_email')
register_start.click()

show_log(driver.get_log('browser'))

# receive /registerd
print("end /register")


###


print()
print("start /confirm")
# receive email
# open the link within it (/confirm)
confirm_url = input('URL to confirm: ')

if 'https' in confirm_url:
    confirm_url = confirm_url.replace('https', 'http')

driver.get(confirm_url)

show_log(driver.get_log('browser'))

print("end /confirm")


###


print()
print("start /vote")
# start vote at /incubator by hand
print("please send email at: http://localhost/incubator")

# receive email
# open the link within it (/vote)
vote_url = input('URL to vote: ')

if 'https' in vote_url:
    vote_url = vote_url.replace('https', 'http')

driver.get(vote_url)

# click #start_vote
start_vote = driver.find_element(By.ID, 'start_vote')
start_vote.click()
time.sleep(0.3)

print("end /vote")

show_log(driver.get_log('browser'))


print()
print("start /choose")
# moved to /choose

# for bool-vote in .boolvote
#  click .voteButton[0 or 1]
bool_votes = driver.find_elements(By.CLASS_NAME, 'boolvote')
for v in bool_votes:
    yes_button = v.find_element(By.CLASS_NAME, 'voteButton')
    yes_button.click()

# fill in the .freevote .textArea with some text
freevote = driver.find_element(By.CLASS_NAME, 'freevote')
textarea = freevote.find_element(By.CLASS_NAME, 'textArea')
textarea.send_keys(str(datetime.now()))

print('free-vote: %s' % textarea.get_attribute('value'))

# press #donext button,
next_button = driver.find_element(By.ID, 'donext')
# parent element of the button actually handles click event
# parent = next_button.find_element_by_xpath('..')
# parent.click()
next_button.click()
time.sleep(0.5)

# moved to /choose step 2
# click #donext again (confirm)
next_button = driver.find_element(By.ID, 'donext')
# parent element of the button actually handles click event
# parent = next_button.find_element_by_xpath('..')
# parent.click()
next_button.click()
time.sleep(0.5)

show_log(driver.get_log('browser'))

print("end /choose")


###


print()
print("start /done")

# moved to done
content = driver.find_element(By.CLASS_NAME, 'content').text

if not '投票を完了しました。' in content:
    raise Exception(f'failed to finish vote: {content}')

print("end /done")

print()

print("test has successfully ended")


driver.quit()
