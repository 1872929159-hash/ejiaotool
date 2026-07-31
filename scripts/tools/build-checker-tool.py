"""
生成东阿阿胶合规检测工具HTML
读取词库JSON，生成嵌入词库的单文件HTML检测工具
"""
import json
import os

BASE_DIR = r"C:\Users\asus\WorkBuddy\京东合规"
LEXICON_PATH = os.path.join(BASE_DIR, "data", "final", "lexicon", "dong-e-ejiao-compliance-lexicon.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "tools", "合规检测工具.html")

with open(LEXICON_PATH, "r", encoding="utf-8") as f:
    lexicon = json.load(f)

lexicon_json = json.dumps(lexicon, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>东阿阿胶 · 京东营销合规检测工具 v1.0</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "Microsoft YaHei", "PingFang SC", sans-serif; background: #f5f5f7; color: #1d1d1f; line-height: 1.6; padding: 20px; }
  .container { max-width: 900px; margin: 0 auto; }
  .header { background: linear-gradient(135deg, #72243e, #993556); color: #fff; padding: 24px 32px; border-radius: 12px; margin-bottom: 20px; }
  .header h1 { font-size: 22px; font-weight: 500; }
  .header p { font-size: 13px; opacity: 0.9; margin-top: 6px; }
  .card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
  .step-label { font-size: 13px; font-weight: 500; color: #993556; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
  .step-num { background: #993556; color: #fff; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; }
  .product-types { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .pt-btn { padding: 16px; border: 2px solid #e0e0e0; border-radius: 10px; background: #fff; cursor: pointer; transition: all 0.2s; text-align: left; }
  .pt-btn:hover { border-color: #993556; }
  .pt-btn.active { border-color: #993556; background: #fbeaf0; }
  .pt-btn .pt-title { font-size: 14px; font-weight: 500; color: #1d1d1f; }
  .pt-btn .pt-desc { font-size: 11px; color: #6e6e73; margin-top: 4px; }
  .pt-btn.active .pt-title { color: #72243e; }
  .current-type { margin-top: 12px; padding: 10px 14px; background: #fbeaf0; border-radius: 8px; font-size: 13px; color: #72243e; }
  textarea { width: 100%; min-height: 120px; padding: 14px; border: 1.5px solid #d0d0d5; border-radius: 10px; font-size: 14px; font-family: inherit; resize: vertical; line-height: 1.6; }
  textarea:focus { outline: none; border-color: #993556; }
  .input-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
  .char-count { font-size: 12px; color: #6e6e73; }
  .btn-group { display: flex; gap: 10px; }
  .btn { padding: 10px 22px; border: none; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
  .btn-secondary { background: #f0f0f5; color: #6e6e73; }
  .btn-secondary:hover { background: #e0e0e5; }
  .btn-primary { background: #993556; color: #fff; }
  .btn-primary:hover { background: #72243e; }
  .btn-primary:disabled { background: #ccc; cursor: not-allowed; }
  .summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
  .summary-card { padding: 18px; border-radius: 10px; text-align: center; }
  .summary-card.red { background: #fceb eb; }
  .summary-card.red { background: #fceb eb; }
  .summary-card.red { background: #fceb eb; }
  .summary-card.red { background: #fceb eb; }
  .sc-red { background: #fceb eb; border: 1px solid #f7c1c1; }
  .sc-yellow { background: #faeeda; border: 1px solid #fac775; }
  .sc-green { background: #eaf3de; border: 1px solid #c0dd97; }
  .sc-num { font-size: 28px; font-weight: 500; }
  .sc-red .sc-num { color: #a32d2d; }
  .sc-yellow .sc-num { color: #854f0b; }
  .sc-green .sc-num { color: #3b6d11; }
  .sc-label { font-size: 12px; color: #6e6e73; margin-top: 4px; }
  .violation { border-radius: 10px; padding: 18px; margin-bottom: 12px; }
  .v-l1 { background: #fceb eb; border-left: 4px solid #e24b4a; }
  .v-l1 { background: #fceb eb; border-left: 4px solid #e24b4a; }
  .v-l1 { background: #fceb eb; border-left: 4px solid #e24b4a; }
  .v-l1 { background: #fceb eb; border-left: 4px solid #e24b4a; }
  .v-red { background: #fceb eb; border-left: 4px solid #e24b4a; }
  .v-yellow { background: #faeeda; border-left: 4px solid #ef9f27; }
  .v-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .v-word { font-size: 18px; font-weight: 500; }
  .v-red .v-word { color: #a32d2d; }
  .v-yellow .v-word { color: #854f0b; }
  .v-badge { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 500; }
  .v-red .v-badge { background: #e24b4a; color: #fff; }
  .v-yellow .v-badge { background: #ef9f27; color: #fff; }
  .v-field { margin-bottom: 8px; font-size: 13px; }
  .v-field-label { color: #6e6e73; min-width: 80px; display: inline-block; }
  .v-legal { background: #f5f5f7; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #444; margin: 8px 0; }
  .v-suggest { background: #e1f5ee; padding: 10px 14px; border-radius: 6px; margin-top: 8px; }
  .v-suggest-label { font-size: 12px; color: #0f6e56; font-weight: 500; margin-bottom: 4px; }
  .v-suggest-words { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
  .suggest-word { background: #fff; border: 1px solid #5dcaa5; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #085041; cursor: pointer; transition: all 0.15s; }
  .suggest-word:hover { background: #5dcaa5; color: #fff; }
  .suggest-word:active { transform: scale(0.95); }
  .copy-tip { font-size: 11px; color: #0f6e56; margin-top: 4px; }
  .v-note { background: #e6f1fb; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #0c447c; margin-top: 8px; }
  .v-whitelist { font-size: 11px; color: #6e6e73; margin-top: 6px; padding: 6px 10px; background: #f5f5f7; border-radius: 6px; }
  .preview { background: #f5f5f7; padding: 16px; border-radius: 8px; font-size: 14px; line-height: 1.8; white-space: pre-wrap; word-break: break-all; }
  .preview mark.red { background: #fceb eb; color: #a32d2d; font-weight: 500; padding: 2px 4px; border-radius: 3px; }
  .preview mark.yellow { background: #faeeda; color: #854f0b; font-weight: 500; padding: 2px 4px; border-radius: 3px; }
  .empty { text-align: center; padding: 40px; color: #6e6e73; font-size: 14px; }
  .footer { text-align: center; padding: 20px; color: #6e6e73; font-size: 12px; }
  .hidden { display: none; }
  @media (max-width: 600px) { .product-types { grid-template-columns: 1fr; } .summary { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>东阿阿胶 · 京东营销合规检测工具</h1>
    <p>v1.0 | 内置67条违规词库 | 支持阿胶块/口服液/阿胶糕/复方阿胶浆4类产品 | 本地运行，数据不上传</p>
  </div>

  <div class="card">
    <div class="step-label"><span class="step-num">1</span>选择产品类型（决定按哪类法规检查）</div>
    <div class="product-types" id="productTypes">
      <button class="pt-btn" data-type="tcm_herb" onclick="selectType('tcm_herb')">
        <div class="pt-title">阿胶块 / 阿胶珠</div>
        <div class="pt-desc">中药饮片/药材，按药典管理，可宣称补血滋阴等功效</div>
      </button>
      <button class="pt-btn" data-type="health_food" onclick="selectType('health_food')">
        <div class="pt-title">阿胶口服液 / 胶囊</div>
        <div class="pt-desc">蓝帽子保健食品，仅可宣称批文功能（增强免疫力/改善营养性贫血）</div>
      </button>
      <button class="pt-btn" data-type="regular_food" onclick="selectType('regular_food')">
        <div class="pt-title">阿胶糕 / 阿胶枣 / 阿胶粉</div>
        <div class="pt-desc">普通食品，不得宣称任何功效（最严格）</div>
      </button>
      <button class="pt-btn" data-type="otc_drug" onclick="selectType('otc_drug')">
        <div class="pt-title">复方阿胶浆</div>
        <div class="pt-desc">OTC药品，按说明书功能主治表述</div>
      </button>
    </div>
    <div class="current-type" id="currentType">请先选择产品类型 ↑</div>
  </div>

  <div class="card">
    <div class="step-label"><span class="step-num">2</span>粘贴你要检测的文案</div>
    <textarea id="inputText" placeholder="在这里粘贴商品标题、卖点、详情页文案、直播话术……任何营销文案都行&#10;&#10;例如：东阿阿胶糕，补血养颜，美容驻颜，最正宗的阿胶，百年传承工艺"></textarea>
    <div class="input-bar">
      <span class="char-count" id="charCount">0 字</span>
      <div class="btn-group">
        <button class="btn btn-secondary" onclick="clearAll()">清空</button>
        <button class="btn btn-primary" id="checkBtn" onclick="runCheck()" disabled>开始检测</button>
      </div>
    </div>
  </div>

  <div class="card hidden" id="resultCard">
    <div class="step-label"><span class="step-num">3</span>查看检测结果</div>
    <div class="summary" id="summary"></div>
    <div id="violationList"></div>
    <div id="previewSection" class="hidden" style="margin-top: 20px;">
      <div style="font-size:13px; color:#6e6e73; margin-bottom:8px;">标红后的文案预览（红色=必须改，黄色=需谨慎）：</div>
      <div class="preview" id="preview"></div>
    </div>
  </div>

  <div class="footer">
    东阿阿胶京东营销合规检测工具 v1.0 | 词库67条 | 本地运行无需联网<br>
    提示：工具仅作辅助参考，最终合规判定请以京东平台规则和法律法规为准
  </div>
</div>

<script>
const LEXICON = __LEXICON__;

let currentProductType = null;

const TYPE_NAMES = {
  tcm_herb: "阿胶块/珠（中药饮片）",
  health_food: "阿胶口服液/胶囊（蓝帽子保健食品）",
  regular_food: "阿胶糕/枣/粉（普通食品）",
  otc_drug: "复方阿胶浆（OTC药品）"
};

const CATEGORY_NAMES = {
  "ADV": "广告法极限词", "EFF": "功效宣称", "FMD": "食品药品界限词",
  "PLT": "京东平台规则", "EJ": "阿胶行业特有",
  "ADV-ABS": "广告法-绝对化用语", "ADV-EXT": "广告法-极限词", "ADV-EXC": "广告法-独家类",
  "ADV-AUTH": "广告法-权威类", "ADV-BRN": "广告法-品牌类", "ADV-LVL": "广告法-级别类",
  "ADV-ONE": "广告法-一类", "EFF-BLD": "功效-补血类", "EFF-BEA": "功效-美容类",
  "EFF-IMM": "功效-免疫类", "EFF-MED": "功效-医疗类", "FMD-DIS": "食药界限-疾病名称",
  "FMD-MED": "食药界限-医疗术语", "FMD-BND": "食药界限-边界模糊", "PLT-TAG": "平台-标签滥用",
  "PLT-DIV": "平台-导流违规", "PLT-MKT": "平台-营销违规", "PLT-DAT": "平台-数据违规",
  "PLT-PRI": "平台-价格违规", "PLT-QUA": "平台-资质违规", "EJ-ORI": "阿胶-正宗道地",
  "EJ-HIS": "阿胶-历史传承", "EJ-CMP": "阿胶-品质对比", "EJ-QUA": "阿胶-品质宣称",
  "FPM-FRD": "虚假-欺诈", "FPM-URG": "虚假-抢购心理", "FPM-FAL": "虚假-虚假宣传", "FPM-SUP": "虚假-迷信"
};

function selectType(type) {
  currentProductType = type;
  document.querySelectorAll('.pt-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.type === type);
  });
  document.getElementById('currentType').textContent = '当前选择：' + TYPE_NAMES[type];
  document.getElementById('checkBtn').disabled = false;
}

document.getElementById('inputText').addEventListener('input', function() {
  document.getElementById('charCount').textContent = this.value.length + ' 字';
});

function clearAll() {
  document.getElementById('inputText').value = '';
  document.getElementById('charCount').textContent = '0 字';
  document.getElementById('resultCard').classList.add('hidden');
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function getAlternatives(entry, productType) {
  const alt = entry.compliant_alternatives;
  if (!alt) return [];
  if (Array.isArray(alt)) return alt;
  if (typeof alt === 'object' && alt[productType]) return alt[productType];
  return [];
}

function runCheck() {
  const text = document.getElementById('inputText').value;
  if (!text.trim()) { alert('请先粘贴要检测的文案'); return; }
  if (!currentProductType) { alert('请先选择产品类型'); return; }

  const violations = [];
  const matchedRanges = [];

  LEXICON.entries.forEach(entry => {
    const matchWords = [entry.word];
    if (entry.variants && Array.isArray(entry.variants)) {
      matchWords.push(...entry.variants);
    }
    const ptr = entry.product_type_rules || {};
    const typeRule = ptr[currentProductType];
    if (!typeRule) return;
    const riskLevel = typeRule.risk_level;
    if (riskLevel !== 'L1' && riskLevel !== 'L2') return;

    const checked = new Set();
    const whitelistPhrases = ['改善营养性贫血', '营养性贫血'];
    matchWords.forEach(word => {
      if (checked.has(word)) return;
      checked.add(word);
      let idx = text.indexOf(word);
      while (idx !== -1) {
        let isWhitelisted = false;
        if (entry.white_list_contexts && entry.white_list_contexts.length > 0) {
          for (const phrase of whitelistPhrases) {
            const phraseIdx = text.indexOf(phrase);
            if (phraseIdx !== -1 && idx >= phraseIdx && idx + word.length <= phraseIdx + phrase.length) {
              isWhitelisted = true;
              break;
            }
          }
        }
        if (!isWhitelisted) {
          violations.push({
            word: word,
            mainWord: entry.word,
            riskLevel: riskLevel,
            category: entry.category_l2,
            description: entry.description || '',
            legalBasis: entry.legal_basis || [],
            note: typeRule.note || '',
            alternatives: getAlternatives(entry, currentProductType),
            whitelist: entry.white_list_contexts || [],
            position: idx,
            length: word.length,
            entryId: entry.id
          });
          matchedRanges.push({ start: idx, end: idx + word.length, risk: riskLevel, word: word });
        }
        idx = text.indexOf(word, idx + word.length);
      }
    });
  });

  violations.sort((a, b) => {
    if (a.riskLevel !== b.riskLevel) return a.riskLevel === 'L1' ? -1 : 1;
    return a.position - b.position;
  });

  const l1Count = violations.filter(v => v.riskLevel === 'L1').length;
  const l2Count = violations.filter(v => v.riskLevel === 'L2').length;

  renderSummary(l1Count, l2Count);
  renderViolations(violations);
  renderPreview(text, matchedRanges);

  document.getElementById('resultCard').classList.remove('hidden');
  document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
}

function renderSummary(l1, l2) {
  const html = `
    <div class="summary-card sc-red"><div class="sc-num">${l1}</div><div class="sc-label">红色高危（必须修改）</div></div>
    <div class="summary-card sc-yellow"><div class="sc-num">${l2}</div><div class="sc-label">黄色预警（需提供证明）</div></div>
    <div class="summary-card sc-green"><div class="sc-num">${l1 === 0 && l2 === 0 ? '✓' : '-'}</div><div class="sc-label">${l1 === 0 && l2 === 0 ? '可以发布' : '需修改后发布'}</div></div>
  `;
  document.getElementById('summary').innerHTML = html;
}

function renderViolations(violations) {
  if (violations.length === 0) {
    document.getElementById('violationList').innerHTML = '<div class="empty">未检测到违规词，文案可以发布。<br>注意：本工具仅检测已知违规词，新型表述请人工复核。</div>';
    return;
  }

  const html = violations.map((v, i) => {
    const isL1 = v.riskLevel === 'L1';
    const cls = isL1 ? 'v-red' : 'v-yellow';
    const badge = isL1 ? 'L1 拦截级' : 'L2 预警级';
    const catName = CATEGORY_NAMES[v.category] || v.category;

    let legalHtml = '';
    if (v.legalBasis && v.legalBasis.length > 0) {
      legalHtml = v.legalBasis.map(l => `<div class="v-legal">《${escapeHtml(l.law_name)}》${escapeHtml(l.article || '')}<br>${escapeHtml(l.content || '')}</div>`).join('');
    }

    let altHtml = '';
    if (v.alternatives && v.alternatives.length > 0) {
      const words = v.alternatives.map(a => `<span class="suggest-word" onclick="copyText('${escapeHtml(a).replace(/'/g,"\\'")}')">${escapeHtml(a)}</span>`).join('');
      altHtml = `<div class="v-suggest"><div class="v-suggest-label">建议替换为（点击可复制）：</div><div class="v-suggest-words">${words}</div><div class="copy-tip">点击任意建议词即可复制到剪贴板</div></div>`;
    } else {
      altHtml = `<div class="v-suggest" style="background:#f5f5f7;"><div class="v-suggest-label" style="color:#6e6e73;">暂无替换建议，建议直接删除该词</div></div>`;
    }

    let noteHtml = '';
    if (v.note) {
      noteHtml = `<div class="v-note">说明：${escapeHtml(v.note)}</div>`;
    }

    let whitelistHtml = '';
    if (v.whitelist && v.whitelist.length > 0) {
      whitelistHtml = `<div class="v-whitelist">白名单（以下情况可使用）：${v.whitelist.map(w => escapeHtml(w)).join('；')}</div>`;
    }

    const wordDisplay = v.word === v.mainWord ? escapeHtml(v.word) : `${escapeHtml(v.word)} <span style="font-size:12px;color:#6e6e73;">（属于"${escapeHtml(v.mainWord)}"的变体）</span>`;

    return `<div class="violation ${cls}">
      <div class="v-header">
        <span class="v-word">${wordDisplay}</span>
        <span class="v-badge">${badge}</span>
      </div>
      <div class="v-field"><span class="v-field-label">分类：</span>${escapeHtml(catName)}</div>
      <div class="v-field"><span class="v-field-label">原因：</span>${escapeHtml(v.description)}</div>
      ${legalHtml}
      ${noteHtml}
      ${altHtml}
      ${whitelistHtml}
    </div>`;
  }).join('');

  document.getElementById('violationList').innerHTML = html;
}

function renderPreview(text, ranges) {
  if (ranges.length === 0) {
    document.getElementById('previewSection').classList.add('hidden');
    return;
  }
  document.getElementById('previewSection').classList.remove('hidden');

  ranges.sort((a, b) => a.start - b.start);
  let html = '';
  let lastEnd = 0;
  const seen = new Set();
  const filtered = ranges.filter(r => {
    const key = r.start + '-' + r.end;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  filtered.forEach(r => {
    html += escapeHtml(text.substring(lastEnd, r.start));
    const cls = r.risk === 'L1' ? 'red' : 'yellow';
    html += `<mark class="${cls}">${escapeHtml(text.substring(r.start, r.end))}</mark>`;
    lastEnd = r.end;
  });
  html += escapeHtml(text.substring(lastEnd));
  document.getElementById('preview').innerHTML = html;
}

function copyText(text) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => showToast('已复制：' + text));
  } else {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); showToast('已复制：' + text); } catch(e) { showToast('复制失败，请手动复制'); }
    document.body.removeChild(ta);
  }
}

function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#0f6e56;color:#fff;padding:10px 24px;border-radius:8px;font-size:14px;z-index:9999;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  setTimeout(() => { toast.style.transition='opacity 0.5s'; toast.style.opacity='0'; }, 1500);
}
</script>
</body>
</html>
"""

html = html.replace("__LEXICON__", lexicon_json)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"已生成检测工具：{OUTPUT_PATH}")
print(f"文件大小：{os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")
print(f"嵌入词条数：{len(lexicon['entries'])}")
