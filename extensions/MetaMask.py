import chromedriver_binary
#Selenium関連のモジュール読み込み
from selenium import webdriver #ブラウザ制御
from selenium.webdriver.chrome.options import Options #ブラウザ制御を始める時のオプション設定
from selenium.webdriver.common.by import By #要素の選択方法
from selenium.webdriver.support.ui import WebDriverWait #待機
from selenium.webdriver.support import expected_conditions as EC #待機条件指定
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os
from MySeleniumSystem import MySeleniumSystem

extension_path = '/Users/ogawa/Library/Application Support/Google/Chrome/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/10.16.2_0'
dummy_backup_phrase = ["mosquito", "palm", "pitch", "alert", "immune", "total", "mammal", "kiwi", "police", "balcony", "wait", "involve"]
dummy_password = "ttsx6puyw44u5"
wallet_address = "0xC6A17Edc82e33771D1f1cbF91490D4b5aDf09812"

mss = MySeleniumSystem(extension=extension_path)

#メタマスク初期化
def metamask_init(dummy_backup_phrase, dummy_password):
    
    #新しいwindowが出現する場合少しsleepを入れておかないとたまに失敗する。
    #0.1秒待機
    sleep(0.1)
    
    #windowが2個表示されるまで待つ
    mss.wait_for_window(2)
    
    #0から数えて１番目のwindowに移動,[a,b,c]のb
    mss.change_window(1)
    
    # [開始]
    mss.wait_and_click('//*[@id="app-content"]/div/div[2]/div/div/div/button')

    # [ウォレットをインポート]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()

    # [同意する]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]').click()


    # [シークレットリカバリーフレーズ] waitを入れないと、たまに入力に失敗するのでwait_and_inputを指定
    [mss.wait_and_input(f'//*[@id="import-srp__srp-word-{i}"]', dummy_backup_phrase[i]) for i in range(12)]

    # [新しいパスワード (最低8文字)]
    mss.browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(dummy_password)
    
    # [パスワードの確認]
    mss.browser.find_element(By.XPATH, '//*[@id="confirm-password"]').send_keys(dummy_password)

    # [利用規約を読んで同意しました]
    mss.browser.find_element(By.XPATH, 
        '//*[@id="create-new-vault__terms-checkbox"]').click()

    # [インポート]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button').click()

    # [すべて完了]
    mss.wait_and_click('//*[@id="app-content"]/div/div[2]/div/div/button')

    # [ダークモードを有効にする]
    mss.wait_and_click('//*[@id="popover-content"]/div/div/section/div[2]/div/div[1]/button')
    
    # [ネットワークのボタンをクリック]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/div[2]').click()
    
    # [ネットワークを追加]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/button').click()


    # [ネットワークを入力]
    bsc = ["Smart Chain", "https://bsc-dataseed.binance.org/", "56", "BNB", "https://bscscan.com"]
    [mss.wait_and_input(f'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[{i+1}]/label/input', bsc[i]) for i in range(5)]

    # [保存]
    mss.browser.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]').click()

    # 完了メッセージ
    print("Metamaskにアカウント追加完了")

#メタマスク接続
def metamask_connect():
    #お約束、新ウィンドウ開くときは0.1秒待機
    sleep(0.1)
    #ウィンドウの個数が3個になるまで待つ
    mss.wait_for_window(3)
    #0から数えて2番目のウィンドウに移動（メタマスクの接続承認ウィンドウ）が出てくるまで待つ
    mss.change_window(2)

    # [次へ]
    mss.wait_and_click(
        '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]')

    # [接続]
    mss.wait_and_click(
        '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]')

    # [署名]
    mss.wait_and_click(
        '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]')

    #ウィンドウの個数が2個になるまで待つ
    mss.wait_for_window(2)

    #0から数えて１番目のウィンドウに移動
    mss.change_window(1)

# サインイン
def metamask_sign():
    #お約束、新ウィンドウ開くときは0.1秒待機
    sleep(0.1)
    #ウィンドウの個数が3個になるまで待つ
    mss.wait_for_window(3)
    #0から数えて2番目のウィンドウに移動（メタマスクの署名ウィンドウ）が出てくるまで待つ
    mss.change_window(2)
    #0から数えて2番目のウィンドウに移動（メタマスクの署名ウィンドウ）が出てくるまで待つ
    mss.wait_and_click('/html/body/div/div/div[3]/div/div[4]/button[2]')
    #0から数えて１番目のウィンドウに移動
    mss.change_window(1)

def metamask_approve():
    #お約束、新ウィンドウ開くときは0.1秒待機
    sleep(0.1)
    #ウィンドウの個数が3個になるまで待つ
    mss.wait_for_window(3)
    #0から数えて2番目のウィンドウに移動（メタマスクの接続承認ウィンドウ）が出てくるまで待つ
    mss.change_window(2)
    #署名ボタンを押す
    mss.wait_and_click('/html/body/div/div/div[3]/div/div[3]/button[2]')
    #0から数えて１番目のウィンドウに移動
    mss.change_window(1)


# ====================================================================================================
def main():

    


    # mss.wait_and_click("/html/body/div/div[3]/div[1]/div[2]")

    # metamask_init(dummy_backup_phrase, dummy_password)

    # metamask_connect()

    # mss.browser.get("https://auth.myrichfarm.com/index/login?l=en-us")

    mss.window_resize()

    canvas_ele = mss.browser.find_element(By.TAG_NAME, "canvas")

    """
    指定サイズ 500,251
    スクショのサイズ 1000, 502
    クリックする時 250, 125.5
    """
    
    
    actions = ActionChains(mss.browser)
    actions.move_to_element_with_offset(canvas_ele, 0, 0)
    actions.move_by_offset(60, 225).click().perform()
    # actions.move_by_offset(0, 20).click().perform()
    # actions.move_by_offset(0, 20).click().perform()




if __name__ == "__main__":
    main()