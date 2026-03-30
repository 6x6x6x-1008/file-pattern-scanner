# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import csv

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ファイルパターン検索ツール")
        self.root.geometry("550x450")

        self.folder_path = ""

        # フォルダ選択
        tk.Button(root, text="フォルダ選択", command=self.select_folder).pack(pady=5)
        self.label = tk.Label(root, text="未選択")
        self.label.pack()

        # 桁数入力
        tk.Label(root, text="抽出する数字の桁数（例：13）").pack()
        self.digit_entry = tk.Entry(root)
        self.digit_entry.insert(0, "13")
        self.digit_entry.pack()

        # 実行ボタン
        tk.Button(root, text="スキャン開始", command=self.run).pack(pady=10)

        # ログ
        self.log = tk.Text(root, height=15)
        self.log.pack()

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.label.config(text=path)

    def run(self):
        if not self.folder_path:
            messagebox.showerror("エラー", "フォルダを選択してください")
            return

        try:
            digit = int(self.digit_entry.get())
        except:
            messagebox.showerror("エラー", "桁数は数字で入力してください")
            return

        pattern = re.compile(rf"\d{{{digit}}}")

        results = []

        for root_dir, _, files in os.walk(self.folder_path):
            for file in files:
                matches = pattern.findall(file)
                for match in matches:
                    full_path = os.path.join(root_dir, file)
                    name, ext = os.path.splitext(file)

                    results.append({
                        "抽出結果": match,
                        "ファイル名": file,
                        "拡張子": ext,
                        "フルパス": full_path
                    })

                    self.log_msg(f"検出: {match} → {file}")

        if not results:
            self.log_msg("該当なし")
            messagebox.showinfo("完了", "該当データがありません")
            return

        output_path = "result.csv"

        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        self.log_msg(f"出力完了: {output_path}")
        messagebox.showinfo("完了", "スキャンが完了しました")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()