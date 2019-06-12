import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import csv
import array as arr

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PyQt4.QtGui import *

import ctypes  # An included library with Python install.

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

class MyDialog(QDialog):
    def __init__(self):

        QDialog.__init__(self)

        self.edUsername = QLineEdit()
        self.edUsername.setPlaceholderText("username")
        self.edPassword = QLineEdit()
        self.edPassword.setEchoMode(QLineEdit.Password)
        self.edUpdateUsername = QLineEdit()
        self.edUpdateUsername.setPlaceholderText("update username")

        btnOk = QPushButton("Start")

        layout = QVBoxLayout()
        layout.addWidget(self.edUsername)
        layout.addWidget(self.edPassword)
        layout.addWidget(self.edUpdateUsername)
        layout.addWidget(btnOk)
        self.setLayout(layout)

        btnOk.clicked.connect(self.btnOkClicked)

    def btnOkClicked(self):
        username = self.edUsername.text()
        password = self.edPassword.text()
        username1 = self.edUpdateUsername.text()

        try:

            driver = webdriver.Chrome("chromedriver.exe")
            driver.set_page_load_timeout(-1)

            driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
            # driver.get("https://localhost/zzz")
            time.sleep(1)

            driver.find_element_by_name("username").clear()
            driver.find_element_by_name("username").send_keys(username)
            # time.sleep(1)

            driver.find_element_by_name("password").clear()
            driver.find_element_by_name("password").send_keys(password)
            # time.sleep(1)

            dom = driver.find_element_by_xpath('//*')
            login_button = dom.find_element_by_xpath('//*[@class="_0mzm- sqdOP  L3NKy       "]')
            login_button.click()

        except NoSuchElementException:
            # print(csvData)
            Mbox('fail!', "username or password invalid", 1)
            # time.sleep(3)
            driver.quit()

        # notnow_button = bs.find('button', 'class=aOOlW   HoLwm ')
        # notnow_button.click()
        try:
            notnow_button = "//button[contains(.,'Not Now')]"
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, notnow_button)))
            element.click()

            span = "//span[contains(.,'Profile')]"
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, span)))
            element.click()

            driver.get("https://www.instagram.com/" + username + "/")

            editprofile_button = "//button[contains(.,'Edit Profile')]"
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, editprofile_button)))
            element.click()
            time.sleep(1)

            driver.find_element_by_id("pepUsername").clear()
            driver.find_element_by_id("pepUsername").send_keys(username1)
            # time.sleep(1)

            submit_button = "//button[contains(.,'Submit')]"
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button)))
            element.click()
            time.sleep(1)

            driver.get("https://www.instagram.com/" + username1 + "/")
            Mbox('Successful!', username + "->" + username1, 1)


        except NoSuchElementException:
            # print(csvData)
            print('No found Element')
            # time.sleep(3)
            # driver.quit()

    # sys.exit(appctxt.app.exec_())


app = QApplication([])
dialog = MyDialog()
dialog.show()
app.exec_()