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
    """実行モード（ブラウザ用/スマホ用）を選択させる"""
    print("実行モードを選択してください:")
    print("1: ブラウザ用")
    print("2: スマホ用")
    while True:
        choice = input("選択してください (1または2): ").strip()
        if choice == '1':
            return 'browser'
        elif choice == '2':
            return 'mobile'
        else:
            print("1または2で選択してください。")

def get_prefix_character():
    """検索キーワードの先頭に追加する1文字を入力させる"""
    while True:
        prefix = input("検索キーワードの先頭に追加する1文字を入力してください: ").strip()
        if len(prefix) == 1:
            return prefix
        else:
            print("1文字のみ入力してください。")

def configure_settings(mode, prefix_char):
    """選択されたモードに応じて設定を変更し、キーワードの先頭に文字を追加"""
    global MAX_SEARCHES, FIXED_KEYWORD
    if mode == 'browser':
        base_keyword = "vibe coding 開発"
        # 90ポイント
        MAX_SEARCHES = 30
        base_keyword2 = "............................."

        # # 180ポイント
        # MAX_SEARCHES = 60
        # base_keyword2 = "..........................................................."

        FIXED_KEYWORD = f"{prefix_char} {base_keyword} {base_keyword2}"
        print(f"ブラウザ用設定: 検索回数={MAX_SEARCHES}, キーワード='{FIXED_KEYWORD}'")
    elif mode == 'mobile':
        base_keyword = "vibe coding 開発"
        # 60ポイント
        MAX_SEARCHES = 20
        base_keyword2 = "..................."

        # # 120ポイント
        # MAX_SEARCHES = 40
        # base_keyword = "vibe coding 開発"
        # base_keyword2 = "......................................."

        FIXED_KEYWORD = f"{prefix_char} {base_keyword} {base_keyword2}"
        print(f"スマホ用設定: 検索回数={MAX_SEARCHES}, キーワード='{FIXED_KEYWORD}'")
    else:
        raise ValueError("無効なモードです")

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
        
        # 2回目以降のみ、1番後ろにカーソルを当てる
        pyautogui.press('end')
        time.sleep(0.4)

    if is_first_search:
        # 初回はフォームをクリア
        pyautogui.hotkey('command', 'a')  # 全選択
        pyautogui.press('backspace')
        time.sleep(0.3)  # クリアが完了するのを待つ

        # 初回はクリップボードにコピーしてペースト
        pyperclip.copy(keyword)
        time.sleep(0.3)  # コピーが完了するのを待つ

        # ペーストを実行
        pyautogui.hotkey('command', 'v')
        time.sleep(0.3)  # ペーストが完了するのを待つ

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

    time.sleep(0.3)
    pyautogui.press('enter')

    # ランダムな待ち時間 (5~7秒)
    wait_time = random.randint(5, 7)
    time.sleep(wait_time)

if __name__ == "__main__":
    # 実行モードを選択して設定を適用
    mode = select_execution_mode()

    # プレフィックス文字を入力
    prefix_char = get_prefix_character()

    # 設定を適用（プレフィックス文字を含む）
    configure_settings(mode, prefix_char)

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
