# Bing Search Automation

Bing検索を自動化するPythonスクリプト集

## 概要

このプロジェクトは、Bing検索を自動的に実行するためのスクリプトを提供します。ブラウザ用とスマホ用の2つのモードがあり、検索ボックスの位置ずれにも対応しています。

## ファイル構成

- `bing検索_文字削除.py` - PyAutoGUIを使用した検索自動化スクリプト（ブラウザ/スマホ対応）
- `bing検索forBrave.py` - Seleniumを使用したBrave Browser向け検索自動化スクリプト

## 必要な環境

- Python 3.x
- 必要なパッケージ:
  - pyautogui
  - pyperclip
  - selenium (Brave Browser版のみ)

## インストール

```bash
pip install pyautogui pyperclip selenium
```

## 使い方

### bing検索_文字削除.py

```bash
python bing検索_文字削除.py
```

1. 実行モード（ブラウザ用/スマホ用）を選択
2. 検索キーワードの先頭に追加する1文字を入力
3. 検索ボックスの位置を2回指定（初回位置とフォーカス後位置）
4. 自動的に検索が実行されます

### bing検索forBrave.py

Brave Browserをリモートデバッグモードで起動してから実行:

```bash
# Brave Browserをリモートデバッグモードで起動
/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222

# スクリプトを実行
python bing検索forBrave.py
```

## 機能

- 検索ボックスの動的な位置ずれに対応
- 初回検索と2回目以降で異なるクリック戦略を使用
- 最適化された待機時間で高速処理
- ブラウザ用とスマホ用で異なる検索回数設定

## ライセンス

MIT License
