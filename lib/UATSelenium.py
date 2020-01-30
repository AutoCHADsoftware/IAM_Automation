from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time as t
from subprocess import *
from contextlib import contextmanager
from lib.UATMain import MainStart


ms = MainStart(controller='', parent='')
creds = ms.getIDandPassword()


class BrowserSelect:
    def __init__(self, browser, input_browser, url):
        self.browser = browser
        self.input_browser = input_browser
        self.url = url


    @contextmanager
    def wait(self, timeout):

        old_page = self.browser.find_element_by_tag_name('html')
        # yield
        WebDriverWait(self.browser, timeout).until(staleness_of(old_page))


    def browserDefintion(self):

        self.input_browser = str(input("Enter 1 for Safari, 2 for Firefox, 3 to Update Software: "))

        if self.input_browser == str('1'):
            self.browser = webdriver.Safari()
            return self.input_browser

        elif self.input_browser == str('2'):
            try:
                binary = FirefoxBinary('/Applications/IBM Firefox.app')
                self.browser = webdriver.Firefox(firefox_binary=binary)
                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.dir", 'PATH TO DESKTOP')
                profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
                return self.input_browser
            except SessionNotCreatedException as error:
                print("Session not created: " + str(error), error.args)

        elif self.input_browser == str('3'):
            result = run(['xcode-select', '--install'], stdout=PIPE)
            output = result.stdout.decode('utf-8')
            print("Output 1: " + output)
            result1 = run(['brew', 'install', 'geckodriver'], stdout=PIPE)
            output1 = result1.stdout.decode('utf-8')
            print("Output 1: " + output1)

        else:
            print("Please enter 1, 2, or 3")


    def uatDownloadCSV(self):
        wait = WebDriverWait(self.browser, 20)

        # send browser to UAT and log in
        # self.browser.maximize_window()
        self.browser.get(self.url)
        self.browser.find_element_by_xpath("//input[@name='username']").send_keys(creds[0])
        self.browser.find_element_by_xpath("//input[@name='password']").send_keys(creds[1] + "\n")

        # go to Reports link
        wait.until(ec.presence_of_element_located((By.XPATH, "//a[@href='./tkt/index.php']")))
        self.browser.get('https://uat.us.ibm.com/iam/tools/tkt/report/report.php')

        # go to Report download section
        # BrowserSelect.wait_for_page_load(self, timeout=10)
        self.browser.implicitly_wait(100)
        self.browser.get('https://uat.us.ibm.com/iam/tools/tkt/report/report_queue_execution.php')

        # attempt 1
        # try:
        #     WebElement.checkbox = self.browser.find_element_by_xpath("//div[@id='content-main']")
        #     self.browser.switch_to.frame(WebElement.checkbox)
        # except NoSuchFrameException as e:
        #     print("Content-main not found: " + str(e), e.args)
        #
        # attempt 2
        # wait = WebDriverWait(self.browser, 10)
        # men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@value='TKT_SRV']")))
        # ActionChains(self.browser).move_to_element(men_menu).perform()
        # t.sleep(5)
        # fastrack = WebDriverWait(self.browser, 10).until(
        #     ec.visibility_of_element_located((By.XPATH, "//input[@value='TKT_SRV']")))
        # fastrack.click()
        #
        # attempt 3
        # BrowserSelect.wait_for_page_load(self, timeout=10)
        # xpath_element_present = ec.presence_of_element_located((By.XPATH, "//input[@value='TKT_SRV']"))
        # WebDriverWait(self.browser, delay).until(xpath_element_present)
        # self.browser.implicitly_wait(100)
        # self.browser.find_element_by_xpath("//input[@value='TKT_SRV']").click()

        try:
            print("Attempt to click checkbox")
            wait.until(ec.presence_of_element_located((By.XPATH,
                "//form[@id='Reports_Queue_Execution']/table/tbody/tr[4]/td[2]/input")))
            checkbox = self.browser.find_element_by_xpath("//form[@id='Reports_Queue_Execution']/table/tbody/tr[4]/td[2]/input")
            checkbox.send_keys(" ")
        except Exception as e:
            print("Checkbox error: ", e)

        try:
            # click report drop down menu
            print("Attempting to click drop down menu")
            wait.until(ec.presence_of_element_located((By.XPATH, "//select[@name='numDelivery']")))
            self.browser.find_element_by_xpath("//select[@name='numDelivery']/option[@value='0']").click()
        except Exception as e:
            print("Dropdown menu error: ", e)

        # attempt 1
        # t.sleep(3)
        # try:
        #         #     # when focus leaves to pop-up, driver can distinguish between original and new window
        #         #     print("Attempting to click .csv link window")
        #         #     wait.until(ec.presence_of_element_located((By.ID, 'Reports_Queue_Execution')))
        #         #     dl_link = self.browser.find_element_by_id('Reports_Queue_Execution')
        #         #     dl_link.send_keys(Keys.RETURN)
        #         # except Exception as e:
        #         #     print(".csv link error: ", e)

        t.sleep(3)
        # attempt 2
        try:
            # when focus leaves to pop-up, driver can distinguish between original and new window
            print("Attempting to click .csv link window")
            wait.until(ec.presence_of_element_located((By.XPATH, "//img[@title='CSV Report']")))
            brad = self.browser.find_element_by_xpath("//img[@title='CSV Report']")
            brad.click()
        except ec.NoSuchElementException() as e:
            print(".csv link error: {}".format(e))



        # try:
        print("Attempting to creating window handling logic")
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.browser.current_window_handle
        download_window_handle = None
        while not download_window_handle:
            for handle in self.browser.window_handles:
                if handle != main_window_handle:
                    download_window_handle = handle
                    break

        self.browser.switch_to.window(download_window_handle)
        print("Attempting to click download link")
        wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, ".csv")))
        self.browser.find_element_by_partial_link_text(".csv").click()

        self.browser.switch_to.window(main_window_handle)
        # except Exception as e:
        #     print("Couldn't switch windows: ", e)


        t.sleep(3)
        print("great success?")


    def uatGrabInfoSafari(self):

        self.browser.get('https://uat.us.ibm.com/iam?SSOlogin=true')
        # force wait for each page to load
        WebDriverWait(self.browser, 10).until(
            lambda d: d.execute_script(script="return document.readyState") == "complete")

        self.browser.find_element_by_xpath("//input[@name='username']").send_keys(creds[0])
        self.browser.find_element_by_xpath("//input[@name='password']").send_keys(creds[1])

        self.browser.find_element_by_id("btn_signin").click()
    
        WebDriverWait(self.browser, 10).until(
            lambda d: d.execute_script(script="return document.readyState") == "complete")
        t.sleep(20)
    
        self.browser.get('https://uat.us.ibm.com/iam/tools/tkt/request/request_queue.php')
        print("wow, it's working perfectly")
        t.sleep(10)
        WebDriverWait(self.browser, 10).until(
            lambda d: d.execute_script(script="return document.readyState") == "complete")
        self.browser.find_element_by_xpath("//a[@href='#']").click()
        t.sleep(10)
        WebDriverWait(self.browser, 10).until(
            lambda d: d.execute_script(script="return document.readyState") == "complete")
        print("wow, we made it, lads")
        t.sleep(10)
    
        self.browser.find_element_by_xpath("//select[@name='numLimit']/option[@value='250']").click()
    
        t.sleep(10)
    
        command = self.browser.find_element_by_xpath("//td[@colspan='6']").get_attribute("")
        print(command)


    def uatClose(self):

        self.browser.get('https://uat.us.ibm.com/iam/tools/tkt/request/request_queue_bulk_actions.php')
        t.sleep(2)


    def uatCancel(self):
        pass


    def uatUpdate(self):
        pass


    def uatSolver(self):
        pass
