# iTermで以下のコマンドを実行後、ソースコードの実行をする
# /Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlencode

# 検索キーワードのベース
base_keyword = "ios swift google api 123456789012345678901234567890"

# BingのベースURL
base_url = "https://www.bing.com/search?"
other_params = "&qs=n&form=QBRE&sp=-1&lq=0&sc=0-37&sk=&cvid=7FEB8E8E3B1845E197330EDAB5C04DBC&ghsh=0&ghacc=0&ghpl="

try:
    # Braveのオプションを設定
    options = Options()
    # options.add_argument("--headless=new")  # ヘッドレスモードを有効にする
    options.add_argument("--disable-gpu")    # GPUアクセラレーションを無効にする（ヘッドレス環境では推奨）
    options.add_argument("--window-size=1920,1080")  # ウィンドウサイズを指定

    # Braveの実行ファイルのパスを指定（環境に合わせて調整してください）
    brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # macOSでの例
    options.binary_location = brave_path

    # Braveを起動
    driver = webdriver.Chrome(options=options)

    search_keyword = base_keyword
    search_count = 0  # 検索回数を初期化
    max_searches = 30  # 最大検索回数

    while len(search_keyword) > 0 and search_count < max_searches:
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
        print(f"検索中 (新しいタブ - {search_count + 1}/{max_searches}): {search_url}")
        time.sleep(6)

        # 検索キーワードを1文字減らす
        search_keyword = search_keyword[:-1]
        search_count += 1  # 検索回数をインクリメント

        # 必要であれば、タブを閉じる (最後に開いたタブを閉じる)
        driver.close()

        # 元のウィンドウに戻る (開いているウィンドウが複数ある場合のみ)
        if driver.window_handles:
            driver.switch_to.window(driver.window_handles[0])

    if search_count == max_searches:
        print(f"最大検索回数({max_searches}回)に達したため終了します。")
    else:
        print("検索キーワードが空になったため終了します。")

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
