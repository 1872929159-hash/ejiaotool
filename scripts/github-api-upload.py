import base64, json, urllib.request, sys, os

# 用法: python github-api-upload.py <local_file> <repo_path>
# 环境变量: GITHUB_TOKEN, GITHUB_REPO (格式: owner/repo)
# 示例: python github-api-upload.py C:\..\COLLABORATION.md COLLABORATION.md

TOKEN = os.environ.get("GITHUB_TOKEN", "your_token_here")
REPO = os.environ.get("GITHUB_REPO", "1872929159-hash/ejiaotool")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def upload_file(local_path, repo_path, commit_msg):
    url = f"https://api.github.com/repos/{REPO}/contents/{repo_path}"

    # 检查是否已存在（需要 SHA）
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as r:
            existing = json.loads(r.read().decode())
            existing_sha = existing.get("sha")
    except urllib.error.HTTPError:
        existing_sha = None

    with open(local_path, "rb") as f:
        content = f.read()

    data = {"message": commit_msg, "content": base64.b64encode(content).decode()}
    if existing_sha:
        data["sha"] = existing_sha

    req = urllib.request.Request(url, method="PUT", headers=HEADERS)
    req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read().decode())
        print(f"✅ {repo_path} ({len(content)} bytes) commit={result['commit']['sha'][:7]}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ {repo_path}: HTTP {e.code} - {e.read().decode()[:200]}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python github-api-upload.py <本地文件路径> <仓库内路径>")
        sys.exit(1)
    upload_file(sys.argv[1], sys.argv[2], f"更新 {sys.argv[2]}")
