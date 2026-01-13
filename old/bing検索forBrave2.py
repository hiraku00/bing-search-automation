from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlencode

# 検索キーワードのベース
base_keyword = "ios swift google api 123456789012345678901234567890"

# BingのベースURL
base_url = "https://www.bing.com/search?"
other_params = "&qs=n&form=QBRE&sp=-1&lq=0&sc=0-37&sk=&cvid=7FEB8E8E3B1845E197330EDAB5C04DBC&ghsh=0&ghacc=0&ghpl="

# リモートデバッグポート
remote_debugging_port = 9222

# Chromeのオプションを設定
options = Options()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{remote_debugging_port}")

try:
    # WebDriver の初期化と接続
    try:
        driver = webdriver.Chrome(options=options)
        print("WebDriver initialized successfully.")
    except Exception as e:
        print(f"WebDriver initialization failed: {e}, type: {type(e)}")
        raise

    # WebDriverWaitのインスタンス化
    wait = WebDriverWait(driver, 20)  # 最大20秒待機

    # 初期ウィンドウが存在することを確認
    try:
        wait.until(EC.number_of_windows_to_be(1))
        print("Initial window is available")
         # 初期ウィンドウのハンドルを取得
        initial_window_handle = driver.current_window_handle
        print(f"Initial window handle: {initial_window_handle}")
    except Exception as e:
          print(f"Failed to wait for initial window: {e}, type: {type(e)}")
          raise

    search_keyword = base_keyword
    search_count = 0  # 検索回数を初期化
    max_searches = 30  # 最大検索回数

    while len(search_keyword) > 0 and search_count < max_searches:
        # 新しいタブを開く
        driver.switch_to.new_window('tab')

        # 検索URLを生成
        params = {"q": search_keyword}
        search_query = urlencode(params)
        search_url = base_url + search_query + other_params

        # 新しいタブでURLをロード
        try:
            driver.get(search_url)
            print(f"検索中 (新しいタブ - {search_count + 1}/{max_searches}): {search_url}")
        except Exception as e:
             print(f"Failed to load URL: {search_url}, error: {e}, type: {type(e)}")
             browser_log = driver.get_log('browser')
             print(f"Browser Log: {browser_log}")
             break  # エラーが発生した場合は、ループを抜ける

        wait.until(EC.url_contains(search_url)) # ページが完全に読み込まれるまで待機
        time.sleep(1)


        # 検索キーワードを1文字減らす
        search_keyword = search_keyword[:-1]
        search_count += 1  # 検索回数をインクリメント

        # 必要であれば、タブを閉じる (最後に開いたタブを閉じる)
        driver.close()

    if search_count == max_searches:
        print(f"最大検索回数({max_searches}回)に達したため終了します。")
    else:
        print("検索キーワードが空になったため終了します。")

except Exception as e:
    print(f"エラーが発生しました: {e}, type: {type(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
