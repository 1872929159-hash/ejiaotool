"""
生成词库和规则库的Markdown内容文件，用于后续插入Word文档
"""
import json
import os

BASE_DIR = r"C:\Users\asus\WorkBuddy\京东合规"
LEXICON_PATH = os.path.join(BASE_DIR, "data", "final", "lexicon", "dong-e-ejiao-compliance-lexicon.json")
RULES_PATH = os.path.join(BASE_DIR, "data", "final", "rules", "platform-rules-library.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed", "structured")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORY_NAMES = {
    "ADV": "广告法极限词", "EFF": "功效宣称分级词", "FMD": "食品药品界限词",
    "PLT": "京东平台规则词", "EJ": "阿胶行业特有风险词",
    "ADV-ABS": "绝对化用语", "ADV-EXT": "极限词语", "ADV-EXC": "独家类",
    "ADV-AUTH": "权威类", "ADV-BRN": "品牌类", "ADV-LVL": "级别类",
    "ADV-ONE": "一类", "EFF-BLD": "补血类", "EFF-BEA": "美容类",
    "EFF-IMM": "免疫类", "EFF-MED": "医疗类", "FMD-DIS": "疾病名称",
    "FMD-MED": "医疗术语", "FMD-BND": "边界模糊", "PLT-TAG": "标签滥用",
    "PLT-DIV": "导流违规", "PLT-MKT": "营销违规", "PLT-DAT": "数据违规",
    "PLT-PRI": "价格违规", "PLT-QUA": "资质违规", "EJ-ORI": "正宗道地",
    "EJ-HIS": "历史传承", "EJ-CMP": "品质对比", "EJ-QUA": "品质宣称",
    "FPM-FRD": "涉嫌欺诈", "FPM-URG": "抢购心理", "FPM-FAL": "虚假宣传", "FPM-SUP": "迷信用语"
}

TYPE_NAMES = {"tcm_herb": "中药饮片", "health_food": "保健食品", "regular_food": "普通食品", "otc_drug": "OTC药品"}
RISK_EMOJI = {"L0": "✅允许", "L1": "🔴禁止", "L2": "🟡预警", "L3": "🔵提醒"}


def get_alternatives_text(entry, product_type):
    alt = entry.get("compliant_alternatives")
    if not alt:
        return "—"
    if isinstance(alt, list):
        return "、".join(alt) if alt else "—"
    if isinstance(alt, dict):
        if product_type in alt and alt[product_type]:
            return "、".join(alt[product_type])
        all_vals = []
        for v in alt.values():
            if isinstance(v, list):
                all_vals.extend(v)
        return "、".join(all_vals[:3]) if all_vals else "—"
    return "—"


def generate_lexicon_markdown():
    with open(LEXICON_PATH, "r", encoding="utf-8") as f:
        lexicon = json.load(f)

    entries = lexicon["entries"]
    meta = lexicon["meta"]

    md = []
    md.append("# 东阿阿胶 · 京东营销合规词库")
    md.append("")
    md.append(f"> 版本 {meta['version']} | 创建日期 {meta['created_at'][:10]} | 词条总数 {meta['total_count']} 条")
    md.append("")
    md.append("---")
    md.append("")

    md.append("## 一、项目说明")
    md.append("")
    md.append("本词库针对东阿阿胶京东官方旗舰店营销场景，收录违禁词、敏感词及平台规则词。")
    md.append("")
    md.append("**核心特性**：同一词汇在不同产品类型下风险等级不同（`product_type_rules`字段）。")
    md.append("例如\"补血\"一词：中药饮片允许（药典记载）、保健食品禁止（需用批文功能\"改善营养性贫血\"）、普通食品绝对禁止。")
    md.append("")

    md.append("## 二、词库统计")
    md.append("")
    cat_counts = {}
    for e in entries:
        c = e.get("category_l1", "unknown")
        cat_counts[c] = cat_counts.get(c, 0) + 1
    md.append("| 一级分类 | 说明 | 词条数 |")
    md.append("| --- | --- | --- |")
    for cat in ["ADV", "EFF", "FMD", "PLT", "EJ"]:
        md.append(f"| {cat} | {CATEGORY_NAMES.get(cat, cat)} | {cat_counts.get(cat, 0)} |")
    md.append(f"| **合计** | | **{len(entries)}** |")
    md.append("")

    risk_counts = {}
    for e in entries:
        r = e.get("risk_level", "unknown")
        risk_counts[r] = risk_counts.get(r, 0) + 1
    md.append(f"- **L1 拦截级**（禁止使用，命中即违规）：{risk_counts.get('L1', 0)} 条")
    md.append(f"- **L2 预警级**（需提供资质/证据佐证）：{risk_counts.get('L2', 0)} 条")
    md.append("")

    md.append("## 三、风险等级说明")
    md.append("")
    md.append("| 等级 | 名称 | 处理策略 |")
    md.append("| --- | --- | --- |")
    md.append("| L0 | 允许 | 该产品类型下可使用，需确保符合具体法规要求 |")
    md.append("| L1 | 拦截级 | 禁止使用，命中即违规，必须修改 |")
    md.append("| L2 | 预警级 | 需提供资质/证据佐证，或需人工审核确认 |")
    md.append("| L3 | 提醒级 | 存在风险，建议优化表述（非强制拦截） |")
    md.append("")

    md.append("## 四、产品类型说明")
    md.append("")
    md.append("| 产品类型代码 | 产品类型 | 代表产品 | 允许功效 | 核心法规 |")
    md.append("| --- | --- | --- | --- | --- |")
    md.append("| tcm_herb | 中药饮片/药材 | 阿胶块、阿胶珠 | 补血滋阴、润燥、止血（药典） | 药品管理法 |")
    md.append("| health_food | 保健食品（蓝帽子） | 阿胶口服液、胶囊 | 增强免疫力、改善营养性贫血（蓝帽子批文） | 广告法第十八条 |")
    md.append("| regular_food | 普通食品 | 阿胶糕、阿胶枣、阿胶粉 | 无（不得宣称任何功效） | 食品安全法第七十三条 |")
    md.append("| otc_drug | OTC药品 | 复方阿胶浆 | 按说明书功能主治 | 药品广告审查发布标准 |")
    md.append("")

    md.append("## 五、分类体系")
    md.append("")
    md.append("| 一级分类 | 说明 |")
    md.append("| --- | --- |")
    md.append("| ADV | 广告法极限词（全产品类型禁止） |")
    md.append("| EFF | 功效宣称分级词（按产品类型差异化判定，核心模块） |")
    md.append("| FMD | 食品药品界限词（防止普通食品越界使用药品/医疗表述） |")
    md.append("| PLT | 京东平台规则词（标签滥用/导流/营销/数据/价格/资质违规） |")
    md.append("| EJ | 阿胶行业特有风险词（正宗道地/历史传承/品质对比/品质宣称） |")
    md.append("")

    md.append("## 六、词条明细")
    md.append("")

    for cat in ["ADV", "EFF", "FMD", "PLT", "EJ"]:
        cat_entries = [e for e in entries if e.get("category_l1") == cat]
        if not cat_entries:
            continue
        md.append(f"### {cat} - {CATEGORY_NAMES.get(cat, cat)}（{len(cat_entries)}条）")
        md.append("")

        l2_groups = {}
        for e in cat_entries:
            l2 = e.get("category_l2", "other")
            l2_groups.setdefault(l2, []).append(e)

        for l2 in sorted(l2_groups.keys()):
            l2_name = CATEGORY_NAMES.get(l2, l2)
            l2_entries = l2_groups[l2]
            md.append(f"#### {l2} - {l2_name}（{len(l2_entries)}条）")
            md.append("")
            md.append("| ID | 词汇 | 默认风险 | 中药饮片 | 保健食品 | 普通食品 | OTC药品 | 说明 | 合规替代词 |")
            md.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
            for e in l2_entries:
                eid = e["id"]
                word = e["word"]
                risk = e.get("risk_level", "")
                ptr = e.get("product_type_rules", {})
                r_tcm = RISK_EMOJI.get(ptr.get("tcm_herb", {}).get("risk_level", ""), "")
                r_hf = RISK_EMOJI.get(ptr.get("health_food", {}).get("risk_level", ""), "")
                r_rf = RISK_EMOJI.get(ptr.get("regular_food", {}).get("risk_level", ""), "")
                r_otc = RISK_EMOJI.get(ptr.get("otc_drug", {}).get("risk_level", ""), "")
                desc = e.get("description", "").replace("|", "/").replace("\n", " ")[:80]
                alt_text = get_alternatives_text(e, None).replace("|", "/")[:60]
                md.append(f"| {eid} | {word} | {risk} | {r_tcm} | {r_hf} | {r_rf} | {r_otc} | {desc} | {alt_text} |")
            md.append("")

        md.append("")

    md.append("## 七、详细字段说明（每条词条包含的字段）")
    md.append("")
    md.append("| 字段 | 说明 |")
    md.append("| --- | --- |")
    md.append("| id | 全局唯一ID，如 ADV-ABS-00001 |")
    md.append("| word | 违禁/敏感词汇原文 |")
    md.append("| pinyin | 拼音（用于谐音变体检测） |")
    md.append("| category_l1 | 一级分类（ADV/EFF/FMD/PLT/EJ） |")
    md.append("| category_l2 | 二级分类（如 EFF-BLD 补血类） |")
    md.append("| category_l3 | 三级分类（可选细分） |")
    md.append("| risk_level | 默认风险等级（L1/L2） |")
    md.append("| word_type | 词汇类型（word/phrase/pattern） |")
    md.append("| description | 违规说明 |")
    md.append("| product_type_rules | 核心字段：四种产品类型各自的风险等级和说明 |")
    md.append("| legal_basis | 法律法规依据 |")
    md.append("| platform_rule_basis | 京东平台规则依据 |")
    md.append("| white_list_contexts | 白名单上下文（该词可合法使用的场景） |")
    md.append("| variants | 变体词列表（同义/谐音/扩展） |")
    md.append("| compliant_alternatives | 合规替代词建议 |")
    md.append("| tags | 标签（如\"阿胶高频误用\"\"直播高风险\"） |")
    md.append("| applicable_categories | 适用商品类目 |")
    md.append("| exempt_categories | 豁免类目 |")
    md.append("| source | 数据来源信息 |")
    md.append("")

    md.append("---")
    md.append("")
    md.append(f"> 本词库由东阿阿胶京东合规项目生成 | 版本 {meta['version']} | {meta['last_updated'][:10]}")
    md.append("")

    output_path = os.path.join(OUTPUT_DIR, "lexicon_content.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"词库Markdown已生成：{output_path}（{len(md)}行）")
    return output_path


def generate_rules_markdown():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        rules_data = json.load(f)

    rules = rules_data["rules"]
    md = []
    md.append("# 东阿阿胶 · 京东营销合规平台规则库")
    md.append("")
    md.append(f"> 版本 {rules_data['meta']['version']} | 创建日期 {rules_data['meta']['created_at'][:10]} | 法规/规则数 {len(rules)} 部")
    md.append("")
    md.append("---")
    md.append("")

    md.append("## 一、说明")
    md.append("")
    md.append("本规则库收录与东阿阿胶京东营销合规相关的法律法规和京东平台规则条款，供词库词条的 `legal_basis` 和 `platform_rule_basis` 字段引用。")
    md.append("")
    md.append("- **legal（法律法规）**：国家颁布的法律法规条款")
    md.append("- **platform（平台规则）**：京东平台发布的规则细则")
    md.append("")

    md.append("## 二、规则清单")
    md.append("")
    md.append("| 规则ID | 类型 | 名称 | 生效日期 | 状态 |")
    md.append("| --- | --- | --- | --- | --- |")
    for r in rules:
        rid = r["rule_id"]
        rtype = "法律法规" if r["rule_type"] == "legal" else "平台规则"
        title = r["title"]
        eff = r.get("effective_date", "—") or "—"
        status = r.get("status", "")
        status_cn = {"effective": "有效", "superseded": "已替代", "repealed": "已废止"}.get(status, status)
        md.append(f"| {rid} | {rtype} | {title} | {eff} | {status_cn} |")
    md.append("")

    md.append("## 三、规则条款详情")
    md.append("")

    for i, r in enumerate(rules):
        rtype = "法律法规" if r["rule_type"] == "legal" else "京东平台规则"
        md.append(f"### {i+1}. {r['title']}")
        md.append("")
        md.append(f"- **规则ID**：{r['rule_id']}")
        md.append(f"- **类型**：{rtype}")
        if r.get("subtitle"):
            md.append(f"- **版本**：{r['subtitle']}")
        if r.get("issuer"):
            md.append(f"- **发布机构**：{r['issuer']}")
        if r.get("effective_date"):
            md.append(f"- **生效日期**：{r['effective_date']}")
        md.append(f"- **状态**：{r.get('status', '')}")
        md.append(f"- **来源URL**：{r.get('source_url', '—')}")
        md.append("")

        chapters = r.get("chapters", [])
        for ch in chapters:
            md.append(f"#### {ch.get('chapter_title', '')}")
            md.append("")
            sections = ch.get("sections", [])
            for s in sections:
                art_num = s.get("article_number", "")
                art_title = s.get("article_title", "")
                content = s.get("content", "")
                md.append(f"**{art_num} {art_title}**")
                md.append("")
                md.append(f"> {content}")
                md.append("")

                sub_items = s.get("sub_items", [])
                if sub_items:
                    md.append("子项：")
                    md.append("")
                    for si in sub_items:
                        label = si.get("item_label", "")
                        si_content = si.get("content", "")
                        md.append(f"- {label} {si_content}")
                    md.append("")

                if s.get("penalty_reference"):
                    md.append(f"*对应处罚条款：{s['penalty_reference']}*")
                    md.append("")

                rel_cats = s.get("related_lexicon_categories", [])
                if rel_cats:
                    cat_names = [CATEGORY_NAMES.get(c, c) for c in rel_cats]
                    md.append(f"*关联词库分类：{'、'.join(cat_names)}*")
                    md.append("")

        if r.get("penalty_summary"):
            md.append("#### 处罚概述")
            md.append("")
            md.append(f"> {r['penalty_summary']}")
            md.append("")

        if r.get("tags"):
            md.append(f"*标签：{'、'.join(r['tags'])}*")
            md.append("")

        md.append("---")
        md.append("")

    md.append(f"> 本规则库由东阿阿胶京东合规项目生成 | 版本 {rules_data['meta']['version']} | {rules_data['meta']['last_updated'][:10]}")
    md.append("")

    output_path = os.path.join(OUTPUT_DIR, "rules_content.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"规则库Markdown已生成：{output_path}（{len(md)}行）")
    return output_path


if __name__ == "__main__":
    lex_path = generate_lexicon_markdown()
    rules_path = generate_rules_markdown()
    print("\n生成完成！")
    print(f"  词库：{lex_path}")
    print(f"  规则库：{rules_path}")
