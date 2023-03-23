import subprocess
import csv
from datetime import datetime

# コミットログを取得
git_log = subprocess.check_output("git log --shortstat", shell=True, text=True)

# CSVファイルに書き込むためのヘッダーを定義
header = ["Date", "Author", "file_changed", "insertions", "deletions"]

# コミット情報を格納するリストを初期化
commits = []

# コミット情報を解析してリストに追加
commit = {}
for line in git_log.splitlines():
    # コミットメッセージの解析
    if line.startswith("commit"):
        if commit:
            commits.append(commit)
            commit = {}
        commit["hash"] = line.split()[1]
    elif line.startswith("Author:"):
        commit["author"] = line.split()[1]
    elif line.startswith("Date:"):
        commit["date"] = datetime.strptime(line.split(
            "Date:")[1].strip(), "%a %b %d %H:%M:%S %Y %z")
    # ファイル変更情報の解析
    elif line.startswith(" "):
        line = line.strip()
        if "file changed," in line or "files changed," in line:
            commit["file_changed"] = int(line.split()[0])
        if ("insertion(+)," in line or "insertions(+)," in line) and ("deletion(-)" in line or "deletions(-)" in line):
            commit["insertions"] = int(line.split()[3])
            commit["deletions"] = int(line.split()[5])
        elif "insertion(+)" in line or "insertions(+)" in line:
            commit["insertions"] = int(line.split()[3])
            commit["deletions"] = 0
        elif "deletion(-)" in line or "deletions(-)" in line:
            commit["insertions"] = 0
            commit["deletions"] = int(line.split()[3])
if commit:
    commits.append(commit)

# CSVファイルに書き込み
with open("git_log.csv", mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for commit in commits:
        writer.writerow({
            "Date": commit["date"].strftime("%Y-%m-%d %H:%M:%S"),
            "Author": commit["author"],
            "file_changed": commit.get("file_changed", ""),
            "insertions": commit.get("insertions", ""),
            "deletions": commit.get("deletions", "")
        })
