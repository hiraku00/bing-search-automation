import pyautogui
import time
from urllib.parse import urlencode
import pyperclip
import sys
import random
import string

# 検索キーワードのベース
base_keyword = "swift deepseek claude"

def ask_to_resume():
    """コンソールで再開するかどうかを尋ねる."""
    while True:
        choice = input("処理を再開しますか？ (yes/no): ").lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("yes または no で答えてください。")

def get_position():
    # print("URLバーの位置にマウスを移動し、5秒以内にクリックしてください")
    # time.sleep(4)
    # print(pyautogui.position())
    # return pyautogui.position()
    """URLバーの位置をユーザーにクリックさせて取得する。確認付き."""
    print("URLバーの位置にマウスを移動してください。")
    input("準備ができたらEnterキーを押してください...")  # Enterキーを押すまで待機
    position = pyautogui.position()
    print(f"取得した座標: {position}")

    while True:
        confirmation = input("この座標でよろしいですか？ (yes/no): ").lower()
        if confirmation in ['yes', 'y']:
            return position
        elif confirmation in ['no', 'n']:
            print("再度クリックしてください。")
            input("準備ができたらEnterキーを押してください...")
            position = pyautogui.position()
            print(f"取得した座標: {position}")
        else:
            print("yes または no で答えてください。")

def navigate_to_url(url, url_bar_pos):
    pyperclip.copy(url)
    pyautogui.click(url_bar_pos)

    time.sleep(1)

    # URLを入力
    # pyautogui.write(url)
    pyautogui.write(url, interval=0.01)

    time.sleep(0.5)

    # Enterキーを押して検索を実行
    pyautogui.press('enter')

if __name__ == "__main__":

    # URLバーの位置を取得
    url_bar_position = get_position()
    # url_bar_position = pyautogui.Point(x=1205, y=330)
    pyautogui.click(url_bar_position)

    # ベースURL
    base_url = "https://www.bing.com/search?"
    other_params = "&qs=n&form=QBRE&sp=-1&lq=0&sc=0-37&sk=&cvid=7FEB8E8E3B1845E197330EDAB5C04DBC&ghsh=0&ghacc=0&ghpl="

    pyautogui.PAUSE = 0 # 各操作間の待機時間を0に設定

    max_searches = 20

    for i in range(max_searches):
        # 250202 制限対応 15分待機
        if i >= 4 and i % 4 == 0:
            print(f'15分待機中... ({i}/{max_searches})')
            wait_seconds = 60 * 15
            for remaining_seconds in range(wait_seconds, 0, -1):
                print(f"残り待機時間: {remaining_seconds - 1} 秒", end='\r') # 行末を'\r'にして上書き表示
                time.sleep(1)
            print('\n', end='')
            print("待機完了！") # カウントダウン終了後に表示

            # 再開するかどうかを尋ねる
            if ask_to_resume():
                # 処理を再開する場合
                print("処理を再開します。")
                pyautogui.click(url_bar_position)
            else:
                # 処理を再開しない場合
                print("処理を中断します。")
                exit()

        # ランダムな待ち時間 (3~6秒)
        wait_time = random.randint(3, 6)
        time.sleep(wait_time)

        # ランダムな文字列を生成 (5~15文字)
        random_length = random.randint(5, 15)
        # random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random_length))
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(random_length))

        # 検索キーワードを生成
        search_keyword = f"{base_keyword} {random_string}"

        # 検索URLを生成
        params = {"q": search_keyword}
        search_query = urlencode(params)
        search_url = base_url + search_query + other_params

        # URLに移動
        navigate_to_url(search_url, url_bar_position)
        print(f"検索中 ({i + 1}/{max_searches}): {search_url}")
