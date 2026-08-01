# 多人协作上手指南

> 本文档写给参与「东阿阿胶·京东营销合规检测工具」完善工作的同事。
> 你不需要懂编程，只需要会「对 WorkBuddy 说话」和「用 GitHub Desktop 点几下按钮」。
> **仓库地址**：`https://github.com/1872929159-hash/ejiaotool`

---

## 一、这个项目是什么

一个网页工具：粘贴营销文案 → 自动检测 763 条违禁/敏感词 → AI 复核并给出合规改写建议。覆盖京东/抖音/小红书等多平台。

核心源码：`tools/合规检测工具.html`（953KB，词库内嵌）、部署文件：`edgeone-deploy/index.html`。

---

## 二、协作模式

```
你对 WorkBuddy 说要改什么
  → WorkBuddy 帮你改 tools/合规检测工具.html
  → GitHub Desktop 提交/推送到你的 feature 分支
  → 在 GitHub 网页发 Pull Request
  → 负责人合并到 main
  → EdgeOne 自动检测到 main 有更新，30-90 秒内公网自动部署
  → 所有人刷新浏览器即可看到彼此改动
```

> **"实时"体现在哪**：合并后几十秒公网即更新，所有人刷新即见。不需要谁手动"发布"。

---

## 三、一次性环境准备（每人只做一次）

| 软件 | 下载 | 用途 |
|------|------|------|
| **GitHub Desktop** | https://desktop.github.com | 管代码，点按钮即可（不用敲命令） |
| **Node.js**（LTS 版） | https://nodejs.org | 本地预览（可选，不装也行） |
| **WorkBuddy 桌面版** | 已安装可跳过 | 你指挥它改代码 |

**拿到代码**：
1. 让负责人把你加为 GitHub 协作者 → 打开邀请链接接受
2. 打开 GitHub Desktop → Clone → 搜 `1872929159-hash/ejiaotool`
3. 验证：进仓库目录 → 双击 `start.bat` → 浏览器看到检测工具页面

---

## 四、日常协作流程

```
① 同步最新代码   →  GitHub Desktop 点 "Fetch origin" + "Pull"
② 开自己的分支   →  对 WorkBuddy 说："从 main 开 feature/我的名字-改了什么"
③ 改代码         →  对 WorkBuddy 说需求，它在本地改 tools/合规检测工具.html
④ 本地看效果     →  双击 start.bat，刷新 localhost:3456 确认
⑤ 推送 + 发 PR   →  对 WorkBuddy 说"提交并推送"，然后去 GitHub 网页发 Pull Request
```

负责人合并后，等 30-90 秒，刷新公网即见新效果。

---

## 五、公网预览地址

> （EdgeOne Git 关联部署后的稳定地址，由负责人填）
>
> 公网地址：`https://ejiaotool-dpm52u6g99x2.edgeone.cool`
>
> 📖 **协同办公指导手册**（发给同事看）：`https://ejiaotool-dpm52u6g99x2.edgeone.cool/guide/`
>
> ⚡ EdgeOne Git 关联自动部署：push main 后 30-90 秒更新。

---

## 六、分支约定

- **main**：全团队唯一主干，合并后自动部署公网。**约定不可直接 push，必须走 Pull Request 合并。**
- **feature/名字-功能**：每人每次改一个功能开一个。如 `feature/zhangsan-改按钮颜色`。
- **开改前一定先 Pull**：否则合并必冲突。
- **一次只改一个功能**：改完合并再开下一个。

---

## 七、单文件分区约定（降低撞车）

整个网站就一个文件 `tools/合规检测工具.html`，约定 5 区，PR 标题注明：

| 区 | 内容 | 示例 |
|----|------|------|
| A 区 | 样式 / CSS | 改按钮颜色 |
| B 区 | 词库数据（763条，一般别动） | 加新违禁词 |
| C 区 | 检测逻辑 | 调匹配规则 |
| D 区 | AI 复核逻辑 | 改提示词 |
| E 区 | UI 文案 / HTML 结构 | 改标题文字 |

不同区同时改基本不冲突，同区冲突让 WorkBuddy 帮处理。

---

## 八、给 WorkBuddy 的话术

| 想做什么 | 说 |
|---------|-----|
| 改配色 | "把检测按钮颜色改成 #993556，清空按钮改成灰色" |
| 改文案 | "把顶部标题改成'多平台营销合规检测'" |
| 加功能 | "在结果下面加导出报告按钮，点击下载 txt" |
| 提交 | "提交改动，消息写'调整按钮配色'，推送到我的 feature 分支" |
| 同步 | "pull main 最新代码" |

---

## 九、常见问题

**Q：双击 start.bat 没反应？**
A：没装 Node.js 或装了没重启。不装也行，纯靠公网看效果。

**Q：合并冲突怎么办？**
A：对 WorkBuddy 说"帮我解决合并冲突"。

**Q：改完看不到公网更新？**
A：确认已合并到 main → 等 30-90 秒 → 浏览器 Ctrl+F5 强制刷新。

**Q：不小心改坏了？**
A：只要没合并到 main 就没事——删掉自己的分支重来即可。main 不进坏代码。

**Q：GitHub Desktop push 失败（网络问题）？**
A：找负责人用 GitHub API 脚本上传（已备好）。日常建议换个网络环境或用手机热点。

**Q：词库加新词？**
A：B 区，单独开分支 + 单独 PR，和负责人确认。

---

## 十、负责人备忘

- [x] 创建 GitHub 私有仓库：`https://github.com/1872929159-hash/ejiaotool`
- [ ] 加同事：https://github.com/1872929159-hash/ejiaotool/settings/access → Add people
- [x] EdgeOne 关联 Git：项目名 `ejiaotool`，关联此仓库 main 分支，输出 `edgeone-deploy`，构建留空，函数 `functions`
- [ ] EdgeOne 配环境变量：`DEEPSEEK_API_KEY` = DeepSeek Key → 点「保存并部署」
- [ ] 拿到公网地址后，填回本文档第五节，并重新跑 `node build-deploy.js` + 推仓库
- [ ] 发本文档 + 公网地址给所有同事
- [ ] push 失败时用 GitHub API 走上传：脚本已存在仓库内 `scripts/github-api-upload.py`（按需调用）
