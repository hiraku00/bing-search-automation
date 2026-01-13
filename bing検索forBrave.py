from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlencode
import random
import string

# 検索キーワードのベース
base_keyword = "swift deepseek claude"

# BingのベースURL
base_url = "https://www.bing.com/search?"
other_params = "&qs=n&form=QBRE&sp=-1&lq=0&sc=0-37&sk=&cvid=7FEB8E8E3B1845E197330EDAB5C04DBC&ghsh=0&ghacc=0&ghpl="

# リモートデバッグポート
remote_debugging_port = 9222

# Chromeのオプションを設定
options = Options()
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{remote_debugging_port}")
options.add_argument("--remote-allow-origins=*")
options.add_argument("--disable-blink-features=AutomationControlled")

try:
    # 既存のBraveに接続
    driver = webdriver.Chrome(options=options)

    # WebDriverWaitのインスタンス化
    wait = WebDriverWait(driver, 10)  # 最大10秒待機

    # 初期ウィンドウのハンドルを取得
    initial_window_handle = driver.current_window_handle

    search_count = 0  # 検索回数を初期化
    max_searches = 30  # 最大検索回数

    while search_count < max_searches:
        # 250202 制限対応 15分待機
        if search_count >= 4 and search_count % 4 == 0:
            print(f'15分待機中... ({search_count}/{max_searches})')
            wait_seconds = 60 * 15  # 15分
            for remaining_seconds in range(wait_seconds, 0, -1):
                print(f"残り待機時間: {remaining_seconds - 1} 秒", end='\r')  # 行末を'\r'にして上書き表示
                time.sleep(1)
            print('\n', end='')
            print("待機完了！")

        # ランダムな文字列を生成 (5~15文字)
        random_length = random.randint(5, 15)
        random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random_length))

        # 検索キーワードを生成
        search_keyword = f"{base_keyword} {random_string}"

        # ウィンドウハンドルを取得して、最初のウィンドウに切り替える
        window_handles = driver.window_handles
        if window_handles:
            driver.switch_to.window(window_handles[0])
        else:
            print("ウィンドウが見つかりませんでした。")
            break

        # 新しいタブを開く
        driver.switch_to.new_window('tab')

        # 検索URLを生成
        params = {"q": search_keyword}
        search_query = urlencode(params)
        search_url = base_url + search_query + other_params

        # 新しいタブでURLをロード
        driver.get(search_url)
        print(f"検索中 ({search_count + 1}/{max_searches}): {search_url}")

        search_count += 1  # 検索回数をインクリメント

        # ランダムな待ち時間 (6~12秒)
        wait_time = random.randint(6, 12)
        time.sleep(wait_time)

        # 必要であれば、タブを閉じる (最後に開いたタブを閉じる)
        driver.close()

        # 元のウィンドウに戻る (開いているウィンドウが複数ある場合のみ)
        if driver.window_handles:
            driver.switch_to.window(driver.window_handles[0])

    print(f"最大検索回数({max_searches}回)に達したため終了します。")

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    if 'driver' in locals():
        pass
