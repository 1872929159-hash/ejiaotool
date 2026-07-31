/**
 * 合规检测工具 · DeepSeek 本地代理服务器
 *
 * 解决浏览器 CORS 限制：浏览器无法直接跨域调用 DeepSeek API，
 * 本代理在本地转发请求，API Key 仅在本机内存中传递，不外泄。
 *
 * 用法：
 *   node proxy-server.js
 *   然后浏览器打开 http://localhost:3456
 *
 * 依赖：无（纯 Node.js 内置模块）
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3456;
const DEEPSEEK_API = 'https://api.deepseek.com/chat/completions';

// MIME 类型映射
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

// 静态文件服务
function serveStatic(req, res, filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not Found');
      return;
    }
    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache'
    });
    res.end(data);
  });
}

// DeepSeek API 代理
function proxyDeepSeek(req, res) {
  let body = '';
  req.on('data', chunk => { body += chunk; });
  req.on('end', () => {
    let parsed;
    try {
      parsed = JSON.parse(body);
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: { message: 'Invalid JSON body', type: 'bad_request' } }));
      return;
    }

    // 从请求体中取出 api_key（HTML 端放在 body 里，不走 header 避免 CORS preflight）
    // 用户自带 Key 优先；未填写时回落到环境变量 DEEPSEEK_API_KEY（与云端边缘函数行为一致）
    const apiKey = (parsed.api_key && String(parsed.api_key).trim())
      || (process.env.DEEPSEEK_API_KEY && String(process.env.DEEPSEEK_API_KEY).trim())
      || '';
    if (!apiKey) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: { message: '未提供 API Key：请在页面「⚙ API 设置」中填入自己的 DeepSeek API Key，或启动服务前设置环境变量 DEEPSEEK_API_KEY。', type: 'no_api_key' } }));
      return;
    }

    // 构造发给 DeepSeek 的请求（去掉 api_key 字段，改用 Bearer header）
    delete parsed.api_key;
    const proxyBody = JSON.stringify(parsed);

    const options = new url.URL(DEEPSEEK_API);
    const proxyReq = https.request({
      hostname: options.hostname,
      port: 443,
      path: options.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey,
        'Content-Length': Buffer.byteLength(proxyBody)
      }
    }, (proxyRes) => {
      let data = '';
      proxyRes.on('data', chunk => { data += chunk; });
      proxyRes.on('end', () => {
        // 直接透传 DeepSeek 的状态码和响应
        res.writeHead(proxyRes.statusCode, {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        });
        res.end(data);
      });
    });

    proxyReq.on('error', (e) => {
      console.error('[Proxy] DeepSeek 连接失败:', e.message);
      if (!res.headersSent) {
        res.writeHead(502, { 'Content-Type': 'application/json' });
      }
      res.end(JSON.stringify({ error: { message: '无法连接 DeepSeek 服务: ' + e.message, type: 'proxy_error' } }));
    });

    // 60 秒超时保护
    proxyReq.setTimeout(60000, () => {
      console.error('[Proxy] DeepSeek 请求超时 (60s)');
      proxyReq.destroy();
      if (!res.headersSent) {
        res.writeHead(504, { 'Content-Type': 'application/json' });
      }
      res.end(JSON.stringify({ error: { message: 'DeepSeek 请求超时（60秒），请稍后重试', type: 'timeout' } }));
    });

    proxyReq.write(proxyBody);
    proxyReq.end();

    console.log(`[Proxy] ${new Date().toLocaleTimeString()} → DeepSeek (model: ${parsed.model || 'unknown'})`);
  });
}

// 主服务器
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  // 解码百分号编码的路径（支持中文文件名），否则 fs.readFile 会找不到字面为 "%E5%AE%88..." 的文件
  const pathname = decodeURIComponent(parsedUrl.pathname);

  // DeepSeek API 代理端点
  if (pathname === '/api/deepseek' && req.method === 'POST') {
    proxyDeepSeek(req, res);
    return;
  }

  // CORS preflight（可选，保险起见）
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end();
    return;
  }

  // 静态文件：默认返回合规检测工具.html
  let filePath;
  if (pathname === '/' || pathname === '/index.html') {
    filePath = __dirname + '/tools/合规检测工具.html';
  } else {
    filePath = __dirname + pathname;
  }

  serveStatic(req, res, filePath);
});

// 全局防崩溃：捕获未处理异常，打印日志但不退出进程
process.on('uncaughtException', (err) => {
  console.error('[Proxy] 未捕获异常（进程不退出）:', err.message || err);
  console.error(err.stack || '');
});
process.on('unhandledRejection', (reason) => {
  console.error('[Proxy] 未处理的 Promise 拒绝:', reason);
});

// server 级别错误处理（防止某个请求出错拖垮整个服务）
server.on('error', (err) => {
  console.error('[Proxy] Server 错误:', err.message);
});

server.listen(PORT, () => {
  console.log('');
  console.log('========================================');
  console.log('  合规检测工具 · 本地代理服务已启动');
  console.log('========================================');
  console.log(`  地址: http://localhost:${PORT}`);
  console.log(`  代理: /api/deepseek → DeepSeek API`);
  console.log('');
  console.log('  按 Ctrl+C 停止服务');
  console.log('========================================\n');
});
