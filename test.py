import yt_dlp
import tkinter as tk
from threading import Thread

# 進捗情報を処理するフック関数
def my_hook(d):
    if d['status'] == 'downloading':
        progress_var.set(f"ダウンロード中: {d['_percent_str']} 完了, ETA: {d['eta']} 秒")
        root.update_idletasks()

# ダウンロードを別のスレッドで実行する関数
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# yt-dlpの設定オプション
ydl_opts = {
    'format': 'best',          # 最高のフォーマットを選択
    'progress_hooks': [my_hook],  # プログレスフックを指定
}

root = tk.Tk()
root.title('yt-dlpダウンロードマネージャ')

# 進捗情報表示用の変数
progress_var = tk.StringVar()

# ダウンロード進捗表示用のEntry
progress_entry = tk.Entry(root, textvariable=progress_var, width=50)
progress_entry.pack()

# ダウンロード実行ボタン
download_button = tk.Button(root, text='ダウンロード開始', command=lambda: Thread(target=download_video, args=(url_entry.get(),)).start())
download_button.pack()

# ユーザーがURLを入力できるようにするEntryウィジェット
url_var = tk.StringVar()
url_entry = tk.Entry(root, textvariable=url_var, width=50)
url_entry.pack()

# GUIアプリケーションをスタート
root.mainloop()
