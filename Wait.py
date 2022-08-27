# import chromedriver_binary
from selenium import webdriver #ブラウザ制御
from selenium.webdriver.chrome.options import Options #ブラウザ制御を始める時のオプション設定

from selenium.webdriver.common.by import By #要素の選択方法
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC #待機条件指定
from selenium.webdriver.support.ui import WebDriverWait #待機

from webdriver_manager.chrome import ChromeDriverManager # chromedirverの自動アップデート

from time import sleep
import os
from pprint import pprint
import subprocess



class Wait:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.actions = ActionChains(self.driver)

    def _hover(self, result):
        self.actions.move_to_element(result).perform()

    def _wait(self, until):
        return WebDriverWait(self.driver, 10).until(until)

    def _clickable(self, xpath):
        return EC.element_to_be_clickable((By.XPATH, xpath))

    def _element_loaded(self, xpath):
        return EC.presence_of_element_located((By.XPATH, xpath))

    # クリックできるまで待ってからクリックする
    def click(self, xpath):
        self._wait(self._clickable(xpath)).click()

    # ホバーできるようになってからホバーする
    def hover(self, xpath):
        self._hover(self._wait(self._element_loaded(xpath)))

    # 入力できるまで待ってから入力する
    def input(self, xpath, value):
        self._wait(self._clickable(xpath)).send_keys(value)

    # N個の画面が出てくるまで待つ
    def appear_window(self, num):
        sleep(0.1)
        self._wait(lambda x: len(self.driver.window_handles)==num)

    # 指定要素にテキストが出現するまで待つ
    def appear_text(self, xpath, msec=10):
        self._wait(self._clickable(xpath)).text

    # ページがロード完了するまで待つ
    def page_load(self, msec=10):
        self.driver.implicitly_wait(msec)
        self._wait(EC.presence_of_all_elements_located)
        self._wait(self._clickable("body"))