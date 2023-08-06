import time

from selenium import webdriver
from selenium.webdriver.common.by import By

class FormFiller():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "https://docs.google.com/forms/d/e/1FAIpQLSdP7QPtkyRcTfY17TJ29VBHBS1QMh_-b0oQfkIDQ0ND8m1uFg/viewform?usp=sf_link"


    def add_via_form(self, title_data):
        self.driver.get(self.url)

        time.sleep(1)
        form = self.driver.find_elements(By.XPATH, "//div[@role='listitem']")
        save_button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

        for field in form:
            field_name = field.find_element(By.TAG_NAME,"span").text
            value = title_data[field_name]
            field_input = field.find_element(By.TAG_NAME, "input")
            field_input.send_keys(value)

        save_button.click()

    def close_browser(self):
        input("Do you want to exit?")
        self.driver.close()
        self.driver.quit()


