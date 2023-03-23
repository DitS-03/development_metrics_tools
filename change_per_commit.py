# -*- coding: utf-8 -*-

import subprocess
import matplotlib.pyplot as plt

# コミットログを取得
git_log = subprocess.check_output("git log --shortstat", shell=True, text=True)

# 変更行数を抽出してリストに追加
changes = []
for line in git_log.splitlines():
    if line.startswith(" "):
        # 変更行数を取得
        line = line.strip()
        if line.startswith("+") or line.startswith("-"):
            change = int(line.replace("+", "").replace("-", ""))
            changes.append(change)

# グラフを作成
plt.hist(changes, bins=50, range=(0, 100))
plt.title("Changes per Commit")
plt.xlabel("Number of changes")
plt.ylabel("Number of commits")
plt.show()
