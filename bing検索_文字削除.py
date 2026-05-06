import pyautogui
import time
from urllib.parse import urlencode
import pyperclip
import sys
import random
import string

# 設定値の定義（関数で動的に設定されるように変更）
MAX_SEARCHES = None
FIXED_KEYWORD = None

def select_execution_mode():
    """実行モード（ブラウザ用/スマホ用/カスタム）を選択させる"""
    print("実行モードを選択してください:")
    print("1: ブラウザ用 (30回)")
    print("2: スマホ用 (20回)")
    print("3: 任意の回数を指定")
    while True:
        choice = input("選択してください (1, 2 または 3): ").strip()
        if choice == '1':
            return 'browser', 30
        elif choice == '2':
            return 'mobile', 20
        elif choice == '3':
            while True:
                try:
                    count_str = input("実行回数を入力してください: ").strip()
                    count = int(count_str)
                    if count > 0:
                        return 'custom', count
                    else:
                        print("1以上の数字を入力してください。")
                except ValueError:
                    print("数字を入力してください。")
        else:
            print("1, 2 または 3 で選択してください。")

def get_prefix_character():
    """検索キーワードの先頭に追加する1文字を入力させる"""
    while True:
        prefix = input("検索キーワードの先頭に追加する1文字を入力してください: ").strip()
        if len(prefix) == 1:
            return prefix
        else:
            print("1文字のみ入力してください。")

def configure_settings(mode, prefix_char, custom_count=None):
    """選択されたモードに応じて設定を変更し、キーワードの先頭に文字を追加"""
    global MAX_SEARCHES, FIXED_KEYWORD
    base_keyword = "vibe coding 開発"
    
    # 選択肢に応じた回数の設定
    mode_names = {
        'browser': ('ブラウザ用', 30),
        'mobile': ('スマホ用', 20),
        'custom': ('カスタム', custom_count)
    }
    
    if mode in mode_names:
        display_name, MAX_SEARCHES = mode_names[mode]
    else:
        raise ValueError("無効なモードです")

    # 指定された回数分、1文字ずつ削除しながら検索できるように十分な長さのドットを追加
    # (キーワード本体 + プレフィックス + 余裕分)
    dots_needed = max(0, MAX_SEARCHES - len(base_keyword) - 2)
    base_keyword2 = "." * (dots_needed + 5)

    FIXED_KEYWORD = f"{prefix_char} {base_keyword} {base_keyword2}"
    print(f"{display_name}設定: 検索回数={MAX_SEARCHES}, キーワード='{FIXED_KEYWORD}'")

def ask_to_resume():
    """コンソールで再開するかどうかを尋ねる."""
    while True:
        choice = input("処理を再開しますか？ (yes/no): ").lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False

def get_positions():
    """検索ボックスの位置を2回取得する。"""
    print("1回目の検索ボックスの位置にマウスを移動してください。")
    input("準備ができたらEnterキーを押してください...")
    pos1 = pyautogui.position()
    print(f"1回目の座標: {pos1}")

    print("\n2回目の検索ボックスの位置（フォーカス後）にマウスを移動してください。")
    input("準備ができたらEnterキーを押してください...")
    pos2 = pyautogui.position()
    print(f"2回目の座標: {pos2}")
    return pos1, pos2

def search_keyword(keyword, pos1, pos2, is_first_search):
    """検索ボックスにキーワードを入力して検索を実行"""
    if is_first_search:
        # 初回検索は2つめの座標を2回クリック（フォーカスを当てるため）
        pyautogui.click(pos2)
        time.sleep(0.4)
        pyautogui.click(pos2)
        time.sleep(0.4)
    else:
        # 2回目以降は1つめの座標を2回クリック
        pyautogui.click(pos1)
        time.sleep(0.4)
        pyautogui.click(pos1)
        time.sleep(0.4)
        # その後2つめの座標をクリック
        pyautogui.click(pos2)
        time.sleep(0.4)
        
    if is_first_search:
        # 初回はフォームをクリア
        pyautogui.hotkey('command', 'a')  # 全選択
        pyautogui.press('backspace')
        time.sleep(0.4)  # クリアが完了するのを待つ

        # 初回はクリップボードにコピーしてペースト
        pyperclip.copy(keyword)
        time.sleep(0.4)  # コピーが完了するのを待つ

        # ペーストを実行
        pyautogui.hotkey('command', 'v')
        time.sleep(0.4)  # ペーストが完了するのを待つ

        # # ペーストが正しく行われたか確認
        # pyautogui.hotkey('command', 'a')  # 全選択
        # pyautogui.hotkey('command', 'c')  # コピー
        # time.sleep(0.1)
        pasted = pyperclip.paste()

        if pasted != keyword:
            # ペーストに失敗した場合は直接入力でリトライ
            pyautogui.write(keyword, interval=0.01)
    else:
        # 2回目以降はバックスペースで1文字削除
        pyautogui.press('backspace')

    time.sleep(0.4)
    pyautogui.press('enter')

    # ランダムな待ち時間 (5~7秒)
    wait_time = random.randint(5, 7)
    time.sleep(wait_time)

if __name__ == "__main__":
    # 実行モードを選択して設定を適用
    mode, count = select_execution_mode()

    # プレフィックス文字を入力
    prefix_char = get_prefix_character()

    # 設定を適用（プレフィックス文字を含む）
    configure_settings(mode, prefix_char, count)

    print("検索ボックスの位置を取得します。")
    pos1, pos2 = get_positions()

    pyautogui.PAUSE = 0  # 各操作間の待機時間を0に設定

    # 現在のキーワード（設定されたキーワードを使用）
    current_keyword = FIXED_KEYWORD
    search_count = 0
    is_first_search = True

    while search_count < MAX_SEARCHES and current_keyword:
        # # 15分待機（4回に1回）
        # if search_count >= 4 and search_count % 4 == 0:
        #     print(f'15分待機中... ({search_count}/{max_searches})')
        #     wait_seconds = 60 * 15
        #     for remaining_seconds in range(wait_seconds, 0, -1):
        #         print(f"残り待機時間: {remaining_seconds - 1} 秒", end='\r')
        #         time.sleep(1)
        #     print('\n', end='')
        #     print("待機完了！")

        #     # 再開するかどうかを尋ねる
        #     if ask_to_resume():
        #         print("処理を再開します。")
        #         pyautogui.click(search_box_position)
        #     else:
        #         print("処理を中断します。")
        #         exit()

        # 検索を実行
        search_keyword(current_keyword, pos1, pos2, is_first_search)
        print(f"検索中 ({search_count + 1:02d}/{MAX_SEARCHES}): {current_keyword}")

        # 初回検索フラグをオフに
        is_first_search = False

        # キーワードの最後の1文字を削除（スペースが残らないように）
        current_keyword = current_keyword[:-1].strip()
        search_count += 1
