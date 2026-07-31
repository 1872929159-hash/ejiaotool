/**
 * EdgeOne Pages 边缘函数 · DeepSeek API 代理
 *
 * 路由：POST /api/deepseek
 *
 * 作用：
 *   1. 绕过浏览器 CORS 限制（DeepSeek 官方接口不返回 Access-Control-Allow-Origin）
 *   2. 托管演示用 API Key（读取环境变量 DEEPSEEK_API_KEY），评委无需自备 Key 即可体验
 *   3. 允许用户传入自有 Key 覆盖演示 Key（请求体 api_key 字段）
 *
 * 环境变量：
 *   DEEPSEEK_API_KEY — 演示用 DeepSeek API Key，在 EdgeOne Pages 控制台配置
 */

const DEEPSEEK_API = 'https://api.deepseek.com/chat/completions';
const TIMEOUT_MS = 60000;

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function jsonResponse(obj, status) {
  return new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8' }, CORS_HEADERS),
  });
}

function errorResponse(message, type, status) {
  return jsonResponse({ error: { message: message, type: type } }, status);
}

/**
 * 从多种运行时读取演示 Key，兼容 EdgeOne / Cloudflare / Node。
 */
function readDemoKey(env) {
  const candidates = [];
  if (env && typeof env === 'object') candidates.push(env.DEEPSEEK_API_KEY);
  if (typeof globalThis !== 'undefined') candidates.push(globalThis.DEEPSEEK_API_KEY);
  if (typeof process !== 'undefined' && process && process.env) candidates.push(process.env.DEEPSEEK_API_KEY);
  for (let i = 0; i < candidates.length; i++) {
    const v = candidates[i];
    if (typeof v === 'string' && v.trim()) return v.trim();
  }
  return '';
}

async function handle(request, env) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (request.method !== 'POST') {
    return errorResponse('仅支持 POST 请求', 'method_not_allowed', 405);
  }

  let payload;
  try {
    payload = await request.json();
  } catch (e) {
    return errorResponse('请求体不是合法 JSON', 'bad_request', 400);
  }
  if (!payload || typeof payload !== 'object') {
    return errorResponse('请求体格式错误', 'bad_request', 400);
  }

  // 用户自带 Key 优先，否则回落到服务端演示 Key
  const userKey = typeof payload.api_key === 'string' ? payload.api_key.trim() : '';
  delete payload.api_key;

  const apiKey = userKey || readDemoKey(env);
  if (!apiKey) {
    return errorResponse(
      '服务端未配置演示 API Key，且您也未填写自有 Key。请点击右上角「⚙ API 设置」填入自己的 DeepSeek API Key。',
      'no_api_key',
      400
    );
  }

  // 基本参数兜底，防止前端漏传导致上游 400
  if (!payload.model) payload.model = 'deepseek-chat';

  const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
  let timer = null;
  if (controller) {
    timer = setTimeout(function () { controller.abort(); }, TIMEOUT_MS);
  }

  try {
    const upstream = await fetch(DEEPSEEK_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey,
      },
      body: JSON.stringify(payload),
      signal: controller ? controller.signal : undefined,
    });

    const text = await upstream.text();
    // 原样透传上游状态码与响应体，前端已有 401/402/429 分支处理
    return new Response(text, {
      status: upstream.status,
      headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8' }, CORS_HEADERS),
    });
  } catch (e) {
    const msg = e && e.name === 'AbortError'
      ? 'DeepSeek 请求超时（60 秒），请稍后重试。'
      : '无法连接 DeepSeek 服务：' + String((e && e.message) || e);
    return errorResponse(msg, 'upstream_error', 502);
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// EdgeOne Pages / Cloudflare Pages Functions 入口
export function onRequest(context) {
  return handle(context.request, context.env);
}

// 通用 Fetch Handler 入口（Workers / Deno / 其他边缘运行时）
export default {
  fetch: function (request, env) {
    return handle(request, env);
  },
};
