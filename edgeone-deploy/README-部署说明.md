# EdgeOne Pages 部署说明

本目录是「东阿阿胶 · 京东营销合规检测工具 v2.0」的云端部署产物。

## 目录结构

```
edgeone-deploy/
├── index.html                  # 静态页面（由 ../build-deploy.js 从 tools/合规检测工具.html 同步生成）
└── functions/
    └── api/
        └── deepseek.js         # 边缘函数，路由自动映射为 POST /api/deepseek
```

> 不要直接编辑 `index.html`。唯一源文件是 `../tools/合规检测工具.html`，
> 修改后在 `京东合规/` 目录执行 `node build-deploy.js` 重新生成。

## 架构

```
评委浏览器  ──►  EdgeOne Pages 静态托管（index.html + 词库）
                        │
                        └─► POST /api/deepseek（边缘函数）
                                    │
                                    └─► https://api.deepseek.com/chat/completions
```

边缘函数承担两件事：

1. **绕过 CORS** — DeepSeek 官方接口不返回 `Access-Control-Allow-Origin`，浏览器无法直连。
2. **托管演示 Key** — 从环境变量 `DEEPSEEK_API_KEY` 读取，访客无需自备 Key 即可体验。
   若访客在页面「⚙ API 设置」中填写了自己的 Key，则优先使用访客的 Key。

## 部署步骤

### 1. 创建 Pages 项目

EdgeOne 控制台 → Pages → 创建项目 → 选择「直接上传」或关联 Git 仓库。

关键配置：

| 配置项 | 值 |
|---|---|
| 输出目录 / 根目录 | `edgeone-deploy` |
| 构建命令 | 留空（无需构建） |
| 函数目录 | `functions`（默认约定，自动识别） |

### 2. 配置环境变量

项目设置 → 环境变量，新增：

| 变量名 | 值 |
|---|---|
| `DEEPSEEK_API_KEY` | `sk-...`（DeepSeek 平台创建的 API Key） |

> **安全建议**：为公开演示单独创建一张 Key，并只充少量额度（如 20 元），
> 与主账号 Key 隔离。公网暴露的演示 Key 存在被刷风险。

配置后需**重新部署**一次才会生效。

### 3. 验证

部署完成后拿到公网网址，按以下顺序自测：

1. 打开网址，页面正常渲染，右上角状态显示「演示额度」。
2. 选择产品类型 → 粘贴一段含违规词的文案 → 点「开始检测」→ 出现词库命中结果。
3. 点「🤖 AI 智能复核」→ 10~30 秒后返回语义风险 + 5 条改写文案。
4. **用手机流量（关掉 WiFi）再测一遍**，确认不是走本机代理。

## 本地开发

云端与本地共用同一份前端代码，接口路径都是 `/api/deepseek`：

```bash
# 可选：设置演示 Key，本地也能免配置直接用
export DEEPSEEK_API_KEY=sk-xxxx      # Windows: set DEEPSEEK_API_KEY=sk-xxxx

node proxy-server.js
# 浏览器打开 http://localhost:3456
```

`proxy-server.js` 与 `functions/api/deepseek.js` 的取 Key 逻辑一致：
**请求体 `api_key` > 环境变量 `DEEPSEEK_API_KEY`**。

## 故障排查

| 现象 | 原因 | 处理 |
|---|---|---|
| 点 AI 复核报 `no_api_key` | 环境变量未配置或未重新部署 | 配置 `DEEPSEEK_API_KEY` 后重新部署 |
| 402 演示额度已用尽 | Key 余额耗尽 | 充值，或提示访客自填 Key |
| 429 请求过于频繁 | 并发过高触发 DeepSeek 限流 | 稍后重试，或引导访客自填 Key |
| 404 `/api/deepseek` | 函数目录未识别 | 确认 `functions/api/deepseek.js` 在输出目录内且路径正确 |
| 页面能开但 AI 报 Failed to fetch | 用 `file://` 打开了本地文件 | 必须通过 http(s) 网址访问 |
