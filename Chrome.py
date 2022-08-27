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

class Chrome:

    def __init__(self, *args, **kwargs):

        self.options = Options() #ブラウザ制御のオプション設定を読み込み

        # leof -i:9222を実行して起動確認
        if self._judge_active():
            0000
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
            self.options.add_argument('--disable-gpu')              # GPUハードウェアアクセラレーションを無効にする 「headlessモードで暫定的に必要なフラグ(そのうち不要になる)
        

            ### その他
            self.options.add_experimental_option('detach', True) # 処理終了後ウィンドウを閉じないように
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])  # よくわからん長文をコンソールに表示させない
            
            #######################################################
            # kwrgsに値があったら
            #######################################################
            # ヘッドレスモードを有効にする
            if "headless" in kwargs and kwargs["headless"] == True:
                print("ヘッドレスモードで起動します")
                self.options.add_argument("--headless")                 # ヘッドレスモード起動
                self.options.add_experimental_option('detach', False)   # 処理終了後webdriverを破棄する

            # もし**kwrgsにextensionがあったら拡張機能を読み込む
            if "extension" in kwargs:
                self.options.add_argument(f'load-extension={kwargs["extension"]}')




    ###########################################################################################################
    ### ブラウザ処理
    ###########################################################################################################

    # Chromeが指定したポートで起動しているかどうか
    def _judge_active(self):
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
            exit()


    # Chromeを起動
    def active(self):
        print("Chromeを起動します")
        ### ブラウザを起動 ###
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        

    # Chromeを閉じる
    def deactive(self):
        print("Chromeを終了します")
        self.driver.close()