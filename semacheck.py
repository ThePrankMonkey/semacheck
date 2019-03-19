#!/usr/bin/python

############
# Settings #
############
# import required modules
try:
    import argparse
    import datetime
    import sys
    import time
    import traceback
    from selenium.webdriver import Firefox
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception as e:
    print('Issue with imports', e)
    exit(30)

DEFAULT_WAIT = 10 # seconds


# get arguments from commandline
try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-n', help="username for the SEMA Connect user", type=str)
    parser.add_argument('--password', '-p', help="password for the SEMA Connect user", type=str)
    parser.add_argument('--search', '-s', help="search string for location", type=str)
    args = parser.parse_args()
except Exception as e:
    print('Issue with arguements', e)
    exit(31)


#############
# Functions #
#############
def setValue(browser, locator, value):
    elem = browser.find_element(*locator)
    elem.clear()
    elem.send_keys(Keys.BACK_SPACE, value) # backspace needed for fields that contain space.

def waitCondition(browser, locator, text, timeout=10):
    return WebDriverWait(browser, timeout).until(
        EC.text_to_be_present_in_element(
            locator,
            text
        )
    )

def main():
    try:
        # Open Browser
        try:
            opts = Options()
            opts.set_headless()
            assert opts.headless  # Operating in headless mode
            browser = Firefox(options=opts)
            browser.get('https://network.semaconnect.com/ev-charging-stations/stationlocator.php')
            # assert 'Sign in [Jenkins]' in browser.title
        except Exception as e:
            print('Issue with opening browser', e)
            exitcode = 30

        # Enter credentials
        try:
            waitCondition(
                browser=browser,
                locator=(By.TAG_NAME, 'h2'),
                text='SIGN IN HERE'
            )
            setValue(browser, (By.ID, 'username'), args.username)
            setValue(browser, (By.ID, 'password'), args.password)
            signin_button = browser.find_element(By.CLASS_NAME, 'green-btn')
            signin_button.click()
        except Exception as e:
            print('Issue entering password', e)
            exitcode = 21
        
        # Switch to Station Locator
        try:
            waitCondition(
                browser=browser,
                locator=(By.ID, 'subscriber_station_locator'),
                text='Station Locator'
            )
            locator_button = browser.find_element(By.ID, 'subscriber_station_locator')
            locator_button.click()
        except Exception as e:
            print('Issue switching to station locator', e)
            exitcode = 22

        # Fill in location
        loopstate = True
        while loopstate:
            try:
                setValue(browser, (By.ID, 'location_address'), args.search)
                submit_button = browser.find_element(By.CSS_SELECTOR, '.searchbox > form:nth-child(1) > input:nth-child(2)')
                submit_button.click()
                WebDriverWait(browser, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CLASS_NAME, 'location-list-right'),
                        args.search
                    )
                )
                elem = browser.find_element(By.CLASS_NAME, 'location-list-right').text.split('\n')
                print('{} - There are {} available spots at {}'.format(datetime.datetime.now().strftime("%X"), elem[0], elem[3]))
                if elem[0][0] != '0':
                    loopstate = False
                    exitcode = 0
                time.sleep(5)
            except Exception as e:
                print('Issue during loop', e)
                exitcode = 23
    finally:
        browser.quit()
        exit(exitcode)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Unexpected Issue', e)
        exit(1)
