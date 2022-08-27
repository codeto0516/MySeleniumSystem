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


class Window:
    def __init__(self, driver) -> None:
        self.driver = driver

    # ウィンドウのサイズを変更する
    def resize(self, width=1400, height=800):
        self.win_width = width
        self.win_height = height
        self.driver.set_window_size(self.win_width, self.win_height)
    

    #N番目のウィンドウに移動する
    def change(self, num):
        sleep(0.1)
        handle = self.driver.window_handles[num-1] #num番目のウィンドウを取得しhandleに保存
        self.driver.switch_to.window(handle) #handleに保存されているウィンドウに移動


    # 現在のウィンドウを閉じる
    def close(self, num):
        self.change(num)
        self.driver.close() #handleに保存されているウィンドウを閉じる

    # ウィンドウハンドルを全取得する
    def get_handle_length(self):
        handles = []
        for i in range(10):
            try:
                handles.append(self.driver.window_handles[i])
            except:
                return handles

    def get(self, url):
        self.driver.get(url)

    def get_iframe(self):
        # トップページにスイッチ
        self.driver.switch_to.default_content()

        return self.driver.find_elements(By.TAG_NAME, 'iframe') # iframeを全部取得