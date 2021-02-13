#!/usr/bin/env python

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def login (browser):
  browser.find_element_by_id("username").send_keys("95350057")
  browser.find_element_by_id("password").send_keys("hdy8vHSsiuo98hvds")
  browser.find_element_by_id("loginbtn").click()
  return


browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
browser.get('https://lms2.bsuir.by/course/view.php?id=971')
login(browser)
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=1363', 'belorusian');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=976', 'worldWar');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=981', 'isp');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=758', 'logic');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=993', 'mgia');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=994', 'mma');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=998', 'mathlogic');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=1008', 'oaip');")
# browser.execute_script("window.open('https://lms2.bsuir.by/course/view.php?id=1023', 'prog');")

while True:
  time.sleep(3600)
  browser.refresh()
  login(browser)
  for currHandle in browser.window_handles:
    browser.switch_to.window(currHandle)
    browser.refresh()
