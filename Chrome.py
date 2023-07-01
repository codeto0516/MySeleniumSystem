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

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Chrome:

    def __init__(self, port=None, profile=None, headress=False, extension_path=None):

        # 起動確認
        self.is_active = self._judge_active()


        print("### オプション ################################################")
        self.options = Options() #ブラウザ制御のオプション設定を読み込み

        if port: self._port(port)

        if profile: self._profile(profile) # プロフィールを指定

        if not self.is_active:
            self.options.add_experimental_option('detach', True) # 処理終了後ウィンドウを閉じないように
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])  # よくわからん長文をコンソールに表示させない
            
        if headress: 
            if self.is_active:
                print("Chromeが起動しているためヘッドレスモードを有効にできません。再起動してください")
            else:
                self._headless() # ヘッドレスモードを有効にする
                
        if extension_path: self._extension(extension_path) # 拡張機能を読み込む

        self._memory_saving() ### 省メモリ設定



    ###########################################################################################################
    ### オプション処理
    ###########################################################################################################

    def _port(self, port):
        print(f"--- [ポート] {port}")
        if self.is_active:
            self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}") # ポートから起動済みのウィンドウを指定する
        else:
            self.options.add_argument(f'--remote-debugging-port={port}') # ポートを指定して起動する
    
    
    def _profile(self, profile):
        print(f"--- [プロフィール] {profile}")
        user_data_dir = "./user-data"

        # user-dataフォルダがなかったら作成
        if not os.path.exists(user_data_dir): 
            os.mkdir(user_data_dir)

        # profileがなかったら
        path = os.path.join(user_data_dir, profile)
        if not os.path.exists(path): 
            os.mkdir(path)


        self.options.add_argument(f'--user-data-dir={user_data_dir}')
        self.options.add_argument(f'--profile-directory={profile}')


    def _headless(self):
        print("--- [ヘッドレスモード] True")
        self.options.add_argument("--headless")                 # ヘッドレスモード起動
        self.options.add_experimental_option('detach', False)   # 処理終了後webdriverを破棄する


    def _extension(self, extension_path):
        print(f"--- [Chrome拡張機能] {extension_path}")
        self.options.add_argument(f'load-extension={extension_path}')

    def _memory_saving(self):
        self.options.add_argument('--no-sandbox')                 # セキュリティ対策などのchromeに搭載してある保護機能をオフにする。
        self.options.add_argument('--disable-dev-shm-usage')      # ディスクのメモリスペースを使う。
        self.options.add_argument('--remote-debugging-port=9222') # リモートデバッグフラグを立てる。
        self.options.add_argument('--start-maximized')            # 起動時にウィンドウを最大化する
        self.options.add_argument('--disable-gpu')              # GPUハードウェアアクセラレーションを無効にする 「headlessモードで暫定的に必要なフラグ(そのうち不要になる)
    

    ###########################################################################################################
    ### ブラウザ処理
    ###########################################################################################################

    # ポート9222で開いているメモリを取得する
    @property
    def lsof(self) -> list:
        stdout:list = subprocess.run(['lsof', '-i:9222'], encoding='utf-8', stdout=subprocess.PIPE).stdout
        return [item.split() for item in stdout.split("\n")[1:-1]]

    # Chromeが指定したポートで起動しているかどうか （ポート9222で開いているメモリを取得する） 
    def _judge_active(self):

        # chromedriverを全部削除 Googleウィンドウだけ残す
        [subprocess.run(["kill", item[1]]) for item in self.lsof if item[0] == "chromedri"]

        # もう一度lsof -i:9222をしてGoogleウィンドウがあればそのまま使う
        if self.lsof:
            print("--- 既に起動しているのでそのまま継続します ---")
            return True
        else:
            print("--- ポートを指定してChromeを起動します ---")
            return False

    # Chromeを起動
    def active(self):
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        print("--- Chromeを起動します ---")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options, desired_capabilities=caps)
        

    # Chromeを閉じる
    def close(self):
        print("--- Chromeを終了します ---")
        self.driver.close()
        self.driver.quit()

    def restart(self):
        print("--- Chromemを再起動します ---")
        
