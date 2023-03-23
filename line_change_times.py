import subprocess

# リポジトリのパス
repo_path = "-"

# 取得する期間のコミットハッシュ値
start_commit = "-"
end_commit = "-"

# 更新された行を格納するセット
updated_lines = set()

# コミット間で変更されたファイルと行を取得
git_diff_cmd = f"git diff {start_commit} {end_commit} --stat"
diff_output = subprocess.check_output(
    git_diff_cmd.split(), cwd=repo_path).decode("utf-8")

# 変更されたファイルを取得
changed_files = diff_output.split("\n")[:-1]
changed_files = [line.split("|")[0].strip() for line in changed_files]

# 各ファイルの変更された行を取得
for file in changed_files:
    git_blame_cmd = f"git blame {start_commit}..{end_commit} --line-porcelain -- {file}"
    blame_output = subprocess.check_output(
        git_blame_cmd.split(), cwd=repo_path).decode("utf-8")
    
    print (blame_output)

    # 各行のコミットハッシュ値を取得
    blame_lines = blame_output.split("\n")[:-1]
    commit_hashes = [line.split()[0] for line in blame_lines]

    # 各行が複数のコミットで更新されたかどうかを判定
    for line, commit_hash in enumerate(commit_hashes):
        if commit_hashes.count(commit_hash) > 1:
            updated_lines.add(f"{file}: {line+1}")

# 更新された行を出力
for line in updated_lines:
    print(line)
