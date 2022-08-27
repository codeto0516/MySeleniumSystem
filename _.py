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

import inspect


class MySeleniumSystem():
    def __init__(self, *args, **kwargs):

        self.options = Options() #ブラウザ制御のオプション設定を読み込み

        # leof -i:9222を実行して起動確認
        if self._chrome_judge_running():

            #################################################################################################################
            # 起動している場合
            #################################################################################################################
            self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # ポートから起動済みのウィンドウを指定する

        else:
            #################################################################################################################
            # 起動していない場合
            #################################################################################################################
            # ポートを指定してChromeを起動
            self.options.add_argument('--emote-debugging-port=9222') # ポートを指定して起動する

            ### プロフィールを指定
            self.options.add_argument('--user-data-dir=/Users/ogawa/Library/Application Support/Google/Chrome')
            self.options.add_argument('--profile-directory=eldoah')

            ### 省メモリ設定
            self.options.add_argument('--no-sandbox')                 # セキュリティ対策などのchromeに搭載してある保護機能をオフにする。
            self.options.add_argument('--disable-dev-shm-usage')      # ディスクのメモリスペースを使う。
            self.options.add_argument('--remote-debugging-port=9222') # リモートデバッグフラグを立てる。
            self.options.add_argument('--start-maximized')            # 起動時にウィンドウを最大化する

            ### その他
            self.options.add_experimental_option('detach', True) # 処理終了後ウィンドウを閉じないように
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])  # よくわからん長文をコンソールに表示させない
            
            #################################################################################################################
            # kwrgsに値があったら
            #################################################################################################################

            # ヘッドレスモードを有効にする
            if "headless" in kwargs and kwargs["headless"] == True:
                print("ヘッドレスモードで起動します")
                self.options.add_argument("--headless")                 # ヘッドレスモード起動
                self.options.add_argument('--disable-gpu')              # 「headlessモードで暫定的に必要なフラグ(そのうち不要になる)
                self.options.add_experimental_option('detach', False)   # 処理終了後webdriverを破棄する

            # もし**kwrgsにextensionがあったら拡張機能を読み込む
            if "extension" in kwargs:
                self.options.add_argument(f'load-extension={kwargs["extension"]}')


        # Chromeを起動
        self.chrome_launch()

 
    ###########################################################################################################
    ### ブラウザ処理
    ###########################################################################################################

    # Chromeが指定したポートで起動しているかどうか
    def _chrome_judge_running(self):
        ### ポートで起動したかの確認（ポート9222で開いているウィンドウを取得する）
        result = subprocess.run(['lsof', '-i:9222'], encoding='utf-8', stdout=subprocess.PIPE)
        if result.returncode != 0 or not "Google" in str(result):
            # 起動していない
            print("ポートを指定してChromeを起動します")
            return False
        elif "Google" in str(result):
            # 起動している
            print("既に起動しているのでそのまま継続します")
            return True
        else:
            print("未知のエラー")
            print(result)

    # Chromeを起動
    def chrome_launch(self):
        print("Chromeを起動します")
        ### ブラウザを起動 ###
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # self.browser = webdriver.Chrome(options=self.options)
        self.actions = ActionChains(self.browser)
        # self.browser.maximize_window() # ウィンドウの最大化

    # Chromeを閉じる
    def chrome_close(self):
        self.browser.close()


    ###########################################################################################################
    ### ウィンドウ処理
    ###########################################################################################################

    # ウィンドウのサイズを変更する
    def window_resize(self, width=1400, height=800):
        self.win_width = width
        self.win_height = height
        self.browser.set_window_size(self.win_width, self.win_height)
    

    #N番目のウィンドウに移動する
    def window_change(self, num):
        sleep(0.1)
        handle = self.browser.window_handles[num-1] #num番目のウィンドウを取得しhandleに保存
        self.browser.switch_to.window(handle) #handleに保存されているウィンドウに移動


    # 現在のウィンドウを閉じる
    def window_close(self, num):
        self.window_change(num)
        self.browser.close() #handleに保存されているウィンドウを閉じる

    # ウィンドウハンドルを全取得する
    def get_handle_length(self):
        handles = []
        for i in range(10):
            try:
                handles.append(self.browser.window_handles[i])
            except:
                return handles
            
    


    ###########################################################################################################
    ### 待機処理
    ###########################################################################################################

    def _hover(self, result):
        self.actions.move_to_element(result).perform()

    def _wait(self, until):
        return WebDriverWait(self.browser, 10).until(until)

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
    def wait_for_window(self, num):
        sleep(0.1)
        self._wait(lambda x: len(self.browser.window_handles)==num)

    # 指定要素にテキストが出現するまで待つ
    def wait_for_text(self, xpath, msec=10):
        self._wait(self._clickable(xpath)).text

    # ページがロード完了するまで待つ
    def wait_page_load(self, msec=10):
        self.browser.implicitly_wait(msec)
        self._wait(EC.presence_of_all_elements_located)
        self._wait(self._clickable("body"))

    ###########################################################################################################
    ### 
    ###########################################################################################################

    def get(self, url):
        self.browser.get(url)
