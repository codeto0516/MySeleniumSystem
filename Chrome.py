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

    def __init__(self, port=9222, profile=None):

        self.port = port

        # 起動確認
        self.is_active = self._is_active()
        

        print("### オプション ################################################")
        self.options = Options() #ブラウザ制御のオプション設定を読み込み


        ### ポートを指定 ###############################
        self._port()
        
        

        ### プロフィールを指定 ###############################
        if profile: self._profile(profile)

        ###  ###############################
        if not self.is_active:
            self.options.add_experimental_option('detach', True) # 処理終了後ウィンドウを閉じないように
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])  # よくわからん長文をコンソールに表示させない
            

        ### 省メモリ設定 ###############################
        self._memory_saving()


        print(self.options.arguments)
        print(self.options.experimental_options)
        print("##############################################################")


    ###########################################################################################################
    ### オプション処理
    ###########################################################################################################
    ### ポート ###############################
    def _port(self):
        # 起動しているか確認
        if self.is_active:
            # 既に起動している -> ポートから起動済みのウィンドウを指定する
            self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")
            print(f"--- [ポート] {self.port}ポートで")
        else:
            # 起動していない -> ポートを指定して起動する
            self.options.add_argument(f'--remote-debugging-port={self.port}') 
            print(f"--- [ポート] {self.port}ポートでChromeを起動します")
    
    ### プロフィール ###############################
    def _profile(self, profile):
        print(f"--- [プロフィール] {profile}を使用します")

        USER_DATA_DIR = "./user-data"

        # user-dataフォルダがなかったら作成
        if not os.path.exists(USER_DATA_DIR): os.mkdir(USER_DATA_DIR)

        # profileがなかったらフォルダを作成
        profile_path = os.path.join(USER_DATA_DIR, profile)
        if not os.path.exists(profile_path): os.mkdir(profile_path)

        # 設定
        self.options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
        self.options.add_argument(f'--profile-directory={profile}')

    ### 省メモリ設定 ###############################
    def _memory_saving(self):
        self.options.add_argument('--no-sandbox')                 # セキュリティ対策などのchromeに搭載してある保護機能をオフにする。
        self.options.add_argument('--disable-dev-shm-usage')      # ディスクのメモリスペースを使う。
        self.options.add_argument('--remote-debugging-port=9222') # リモートデバッグフラグを立てる。
        self.options.add_argument('--start-maximized')            # 起動時にウィンドウを最大化する
        self.options.add_argument('--disable-gpu')                # GPUハードウェアアクセラレーションを無効にする 「headlessモードで暫定的に必要なフラグ(そのうち不要になる)
        # self.options.add_argument("--blink-settings=imagesEnabled=false") # 画像の読み込みを無効化
        # self.options.add_argument("--disable-application-cache") # キャッシュの無効化


    ###########################################################################################################
    ### ブラウザ処理
    ###########################################################################################################

    # 指定ポートで開いているメモリを取得する
    def _lsof(self, port) -> list:
        stdout:list = subprocess.run(['lsof', f'-i:{port}'], encoding='utf-8', stdout=subprocess.PIPE).stdout
        return [item.split() for item in stdout.split("\n")[1:-1]]

    def _kill(self, pid) -> None:
        subprocess.run(["kill", pid]) 


    # Chromeが指定したポートで起動しているかどうか （ポート9222で開いているメモリを取得する） 
    def _is_active(self) -> bool:

        # chromedriverを全部削除 Googleウィンドウだけ残す
        [self._kill(process[1]) for process in self._lsof(self.port) if process[0] == "chromedri"]

        # もう一度lsof -i:9222をしてGoogleウィンドウがあればそのまま使う
        if self._lsof(self.port):
            print("--- 既に起動しているのでそのまま継続します ---")
            return True
        else:
            print("--- ポートを指定してChromeを起動します ---")
            return False

    # Chromeを起動
    def active(self) -> None:
        # websocketを傍受するために追加
        caps = DesiredCapabilities.CHROME # Chromeブラウザの設定を表すオブジェクトを作成
        caps['goog:loggingPrefs'] = {'performance': 'ALL'} # Chromeブラウザでのパフォーマンスログの収集を有効化

        # ChromeDriverがない場合は自動インストール
        driver_path = ChromeDriverManager().install()

        # Chromeを起動し、Driverを取得
        self.driver = webdriver.Chrome(driver_path, options=self.options, desired_capabilities=caps)
        

    # Chromeを閉じる
    def close(self) -> None:
        print("--- Chromeを終了します ---")
        self.driver.close()
        self.driver.quit()

    def restart(self) -> None:
        print("--- Chromemを再起動します ---")
        
