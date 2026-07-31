import os, re, json, collections, openpyxl
try:
    from pypinyin import lazy_pinyin
    def get_py(w): return "".join(lazy_pinyin(w))
except Exception:
    def get_py(w): return ""

BASE = r"C:\Users\asus\WorkBuddy\2026-07-31-09-39-30\京东合规"
KB = os.path.join(BASE, "data", "raw", "third-party", "守正胶香知识库")
LEX = os.path.join(BASE, "data", "final", "lexicon", "dong-e-ejiao-compliance-lexicon.json")
OUT = os.path.join(BASE, "data", "final", "lexicon", "dong-e-ejiao-compliance-lexicon.multi-platform.json")

with open(LEX, encoding="utf-8") as f:
    existing = json.load(f)
existing_entries = existing["entries"]

xp = os.path.join(KB, "敏感词总表.xlsx")
wb = openpyxl.load_workbook(xp, read_only=True, data_only=True)

def col_idx(ws, name):
    hdr = [c.value for c in ws[1]]
    return hdr.index(name) if name in hdr else 0

ws5 = wb["Sheet5-综合汇总表"]
rows = list(ws5.iter_rows(values_only=True))
I = {h: i for i, h in enumerate(rows[0])}

# Sheet8 variants, Sheet9 whitelist keyed by 词条ID
def load_map(sheet_name, key_col="词条ID"):
    ws = wb[sheet_name]
    k = col_idx(ws, key_col)
    m = {}
    for r in ws.iter_rows(values_only=True):
        if r is None or r[k] is None:
            continue
        vid = str(r[k]).strip()
        vals = [str(r[c]).strip() for c in range(len(r)) if c != k and r[c] and str(r[c]).strip()]
        if vals:
            m[vid] = vals
    return m

variants_map = load_map("Sheet8-变体与谐音识别")
whitelist_map = load_map("Sheet9-安全表述与白名单")

RISK = {"红": "L1", "橙": "L2", "黄": "L3"}
PROD_MAP = {"P1药品": "otc_drug", "P2保健食品": "health_food", "P3普通食品": "regular_food",
            "P3食品": "regular_food", "中药饮片": "tcm_herb"}
ALL_PROD = ["tcm_herb", "health_food", "regular_food", "otc_drug"]

PLAT_ALIAS = {
    "天猫淘宝": ["天猫", "淘宝"], "淘宝": ["淘宝"], "天猫": ["天猫"], "抖音": ["抖音"],
    "抖音直播": ["抖音", "直播"], "快手": ["快手"], "小红书": ["小红书"], "微信": ["微信"],
    "微信公众号": ["微信公众号"], "视频号": ["微信视频号"], "微信视频号": ["微信视频号"],
    "微信小店": ["微信小店"], "直播渠道": ["直播"], "电商平台": ["电商"], "社媒渠道": ["社媒"],
    "私域渠道": ["私域"], "线下渠道": ["线下"], "图片/视频": ["图片", "视频"], "视频渠道": ["视频"],
    "全部渠道": ["全部"],
}
PLAT_PREFIX = {"抖音": "抖音", "快手": "快手", "小红书": "小红书", "微信视频号": "微信视频号",
               "微信小店": "微信小店", "阿里妈妈": "阿里妈妈", "天猫": "天猫", "淘宝": "淘宝", "微信": "微信"}

def parse_platforms(chan, l2):
    plats = set()
    if chan:
        for part in re.split(r"[；;、/，,\s]+", chan):
            part = part.strip()
            if not part:
                continue
            plats.update(PLAT_ALIAS.get(part, [part]))
    m = re.match(r"^([一-龥A-Za-z]+?)\s*(?:[/／]\s*[一-龥A-Za-z]+?)?\s*[-—]", l2 or "")
    if m:
        pref = m.group(1).strip()
        if pref in PLAT_PREFIX:
            plats.add(PLAT_PREFIX[pref])
    return sorted(plats)

def parse_prod_rules(prod, risk):
    if not prod or "全部" in prod:
        return {p: {"risk_level": risk, "note": prod or "全部产品类别"} for p in ALL_PROD}
    rules = {}
    for key, code in PROD_MAP.items():
        if key in prod:
            rules[code] = {"risk_level": risk, "note": prod}
    if not rules:
        return {p: {"risk_level": risk, "note": prod} for p in ALL_PROD}
    return rules

def norm(w):
    return re.sub(r"\s+", "", str(w)).lower()

new_entries = []
seen = set()
for r in rows[1:]:
    if not r or r[0] is None:
        continue
    raw_id = str(r[I["词条ID"]]).strip()
    word = str(r[I["敏感词或表述"]]).strip()
    if not word:
        continue
    nw = norm(word)
    if nw in seen:
        continue
    seen.add(nw)
    l1 = str(r[I["一级分类"]]).strip()
    l2 = str(r[I["二级分类"]]).strip()
    risk = RISK.get(str(r[I["风险等级"]]).strip(), "L2")
    prod = str(r[I["适用产品类别"]]).strip()
    chan = str(r[I["适用渠道"]]).strip()
    basis = str(r[I["违规依据"]]).strip()
    example = str(r[I["违规示例"]]).strip()
    alt = str(r[I["合规替换建议"]]).strip()
    action = str(r[I["审核动作"]]).strip()
    src = str(r[I["来源"]]).strip()
    date = str(r[I["更新日期"]]).strip()
    status = str(r[I["状态"]]).strip()
    variants = variants_map.get(raw_id, [])
    whitelist = whitelist_map.get(raw_id, [])
    plats = parse_platforms(chan, l2)
    alts = [a.strip() for a in re.split(r"[；;]", alt) if a.strip() and "禁止" not in a and "删除" not in a][:5]
    entry = {
        "id": "SG-" + raw_id,
        "word": word,
        "pinyin": get_py(word),
        "category_l1": l1,
        "category_l2": l2,
        "category_l3": None,
        "risk_level": risk,
        "word_type": "phrase" if len(word) > 1 else "word",
        "description": (l2 + "：" + example) if example else l2,
        "legal_basis": [{"law_name": basis, "article": "", "content": example, "source_url": ""}] if basis else [],
        "platform_rule_basis": [{"platform": p, "rule": l2} for p in plats if p not in ("全部",)],
        "white_list_contexts": whitelist,
        "variants": variants,
        "variant_types": [],
        "tags": [l2] + (["全部渠道"] if "全部" in chan else [chan]),
        "applicable_categories": [c for k, c in PROD_MAP.items() if k in prod] if "全部" not in prod else ALL_PROD,
        "exempt_categories": [],
        "compliant_alternatives": alts,
        "detection_pattern": word,
        "detection_mode": "exact",
        "platforms": plats or ["全部"],
        "review_action": action,
        "source": {"type": "kb", "name": src or "守正胶香知识库", "original_id": raw_id, "collected_date": date},
        "status": "active" if status == "在用" else "inactive",
        "created_at": date or "2026-07-31",
        "updated_at": date or "2026-07-31",
        "version": "1.0.0",
        "product_type_rules": parse_prod_rules(prod, risk),
    }
    new_entries.append(entry)

# enrich existing entries with uniform fields
# 原有 67 条以《广告法》绝对化用语/功效宣称等通用合规词为主，应全平台适用 → 标 ["全部"]
for e in existing_entries:
    e.setdefault("platforms", ["全部"])
    e.setdefault("detection_mode", "exact")
    e.setdefault("detection_pattern", e.get("word", ""))
    e.setdefault("status", "active")
    e.setdefault("created_at", "2026-07-30")
    e.setdefault("updated_at", "2026-07-30")
    e.setdefault("version", "1.0.0")
    e.setdefault("applicable_categories", ALL_PROD)
    e.setdefault("white_list_contexts", [])
    e.setdefault("platform_rule_basis", [])
    e.setdefault("variant_types", [])
    e.setdefault("source", {"type": "manual", "name": "东阿阿胶京东词库"})

existing_norm = {norm(e["word"]): e for e in existing_entries}
merged = list(existing_entries)
added = 0
for e in new_entries:
    if norm(e["word"]) in existing_norm:
        continue
    merged.append(e)
    added += 1

out = {
    "meta": {
        "project": "东阿阿胶营销合规多平台词库",
        "version": "2.0.0",
        "created_at": "2026-07-31T00:00:00Z",
        "last_updated": "2026-07-31T00:00:00Z",
        "schema_version": "1.0.0",
        "description": "在京东阿胶67条词库基础上，融合守正胶香知识库（敏感词总表763条）形成的多平台营销合规词库，覆盖京东/抖音/小红书/微信视频号/微信小店/淘宝/天猫/快手/阿里妈妈等渠道，保留product_type_rules差异化判定并新增platforms平台维度。",
        "product_types": existing.get("meta", {}).get("product_types", {}),
        "platforms": ["全部", "京东", "抖音", "小红书", "微信视频号", "微信小店", "淘宝", "天猫", "快手", "阿里妈妈", "直播", "电商", "社媒", "私域"],
        "stats": {"existing": len(existing_entries), "from_kb_deduped": len(new_entries),
                  "added_new": added, "total": len(merged)},
    },
    "entries": merged,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("existing:", len(existing_entries))
print("from_kb_deduped:", len(new_entries))
print("added_new:", added)
print("TOTAL:", len(merged))
pc = collections.Counter()
for e in merged:
    for p in e.get("platforms", []):
        pc[p] += 1
print("platform coverage:", dict(pc.most_common()))
print("risk dist:", dict(collections.Counter(e["risk_level"] for e in merged)))
