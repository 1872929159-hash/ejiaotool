/**
 * 构建 EdgeOne Pages 部署产物
 *
 * 作用：把唯一源文件 tools/合规检测工具.html 同步到 edgeone-deploy/index.html，
 *      避免本地版与云端版代码走样。
 *
 * 用法：node build-deploy.js
 */

const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, 'tools', '合规检测工具.html');
const OUT_DIR = path.join(__dirname, 'edgeone-deploy');
const OUT = path.join(OUT_DIR, 'index.html');

if (!fs.existsSync(SRC)) {
  console.error('[build] 源文件不存在:', SRC);
  process.exit(1);
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const html = fs.readFileSync(SRC, 'utf-8');
fs.writeFileSync(OUT, html, 'utf-8');

const kb = (Buffer.byteLength(html, 'utf-8') / 1024).toFixed(1);
console.log('[build] 已生成:', OUT, `(${kb} KB)`);
console.log('[build] 边缘函数:', path.join(OUT_DIR, 'functions', 'api', 'deepseek.js'));
console.log('[build] 部署时请将「输出目录」设为 edgeone-deploy，并配置环境变量 DEEPSEEK_API_KEY');
