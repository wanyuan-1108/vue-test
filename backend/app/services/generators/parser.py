from __future__ import annotations

import re
from typing import List

from app.schemas.design import PromptAnalysis
from app.services.ai_client import AIClient
from app.services.generators.catalog import infer_industry, industry_label


SECTION_KEYWORDS = {
    "hero": ["hero", "首页", "首屏", "横幅", "banner"],
    "about": ["about", "品牌故事", "关于", "介绍"],
    "products": ["product", "产品", "菜单", "商品", "作品"],
    "features": ["feature", "亮点", "卖点", "优势", "推荐"],
    "testimonials": ["testimonial", "评价", "口碑", "用户评价"],
    "promo": ["promo", "促销", "优惠", "活动", "campaign"],
    "contact": ["contact", "联系", "咨询", "表单", "预约"],
    "footer": ["footer", "页脚"],
}


STYLE_HINTS = {
    "极简": "minimal",
    "高级": "premium",
    "年轻": "youthful",
    "科技": "tech",
    "未来": "futuristic",
    "暖": "warm",
    "暗色": "dark",
    "童趣": "playful",
    "活力": "energetic",
    "商业": "commercial",
    "官网": "official",
}


KNOWN_BRANDS = {
    "麦当劳": "mcdonalds",
    "mcdonald": "mcdonalds",
    "mcdonalds": "mcdonalds",
    "星巴克": "starbucks",
    "starbucks": "starbucks",
    "苹果": "apple",
    "apple": "apple",
    "耐克": "nike",
    "nike": "nike",
    "特斯拉": "tesla",
    "tesla": "tesla",
}


BRAND_DISPLAY_NAMES = {
    "mcdonalds": "McDonald's",
    "starbucks": "Starbucks",
    "apple": "Apple",
    "nike": "Nike",
    "tesla": "Tesla",
}


COLOR_HINTS = {
    "burger_fast_food": ["品牌红", "明亮黄", "纯白"],
    "coffee_brand": ["咖啡棕", "奶油米", "深木色"],
    "dessert_brand": ["奶油白", "樱花粉", "可可棕"],
    "fashion_brand": ["高级黑", "米白", "暖灰"],
    "tech_product_brand": ["深海军蓝", "电光蓝", "银灰"],
    "restaurant_brand": ["炭黑", "香槟金", "暖白"],
    "brand": ["深灰", "紫色", "青蓝"],
}


def _match_sections(prompt: str) -> List[str]:
    lowered = prompt.lower()
    sections: List[str] = []
    for section_id, keywords in SECTION_KEYWORDS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            sections.append(section_id)
    return sections


def _extract_reference_brands(prompt: str) -> List[str]:
    lowered = prompt.lower()
    results: List[str] = []
    for alias, brand_key in KNOWN_BRANDS.items():
        if alias.lower() in lowered and brand_key not in results:
            results.append(brand_key)
    return results


def _extract_brand_name(prompt: str, reference_brands: List[str]) -> str:
    if reference_brands:
        brand_key = reference_brands[0]
        return BRAND_DISPLAY_NAMES.get(brand_key, brand_key)

    patterns = [
        r"生成(?:一个)?(.+?)(?:官网|网站|品牌官网|品牌网站)",
        r"帮我生成(.+?)(?:官网|网站|网页)",
        r"(.+?)官网风格",
        r"(.+?)风格的网站",
        r"(.+?)品牌官网",
    ]
    for pattern in patterns:
        matched = re.findall(pattern, prompt)
        if not matched:
            continue
        candidate = matched[0].strip(" ，。、“”‘’\t\n")
        candidate = re.sub(r"^(一个|一套|一个像|一个类似)", "", candidate).strip()
        if candidate and candidate not in {"网站", "官网", "网页", "品牌", "品牌风格"}:
            return candidate
    return ""


def _infer_site_type(prompt: str, industry_hint: str) -> str:
    lowered = prompt.lower()
    if industry_hint in {"burger_fast_food", "coffee_brand", "dessert_brand", "fashion_brand", "restaurant_brand"}:
        return "brand_site"
    if industry_hint == "tech_product_brand":
        return "product_brand_site"
    if any(word in lowered for word in ["saas", "平台", "dashboard", "软件"]):
        return "saas"
    return "brand_site"


def _infer_audience(prompt: str, industry_hint: str) -> str:
    if any(word in prompt for word in ["年轻", "年轻人"]):
        return "年轻消费者"
    if industry_hint == "burger_fast_food":
        return "年轻家庭与大众消费者"
    if industry_hint == "coffee_brand":
        return "都市白领与精品咖啡爱好者"
    if industry_hint == "dessert_brand":
        return "年轻女性与社交分享人群"
    if industry_hint == "fashion_brand":
        return "时尚消费者与潮流人群"
    if industry_hint == "tech_product_brand":
        return "数码爱好者与品质用户"
    return "现代中文互联网用户"


def _infer_brand_tone(prompt: str, industry_hint: str) -> str:
    if "高级" in prompt:
        return "高级感、质感、专业可信"
    if industry_hint == "burger_fast_food":
        return "高饱和、热情、商业转化导向"
    if industry_hint == "coffee_brand":
        return "温暖、治愈、精致生活方式"
    if industry_hint == "dessert_brand":
        return "甜美、精致、轻松分享"
    if industry_hint == "fashion_brand":
        return "现代、利落、品牌感强"
    if industry_hint == "tech_product_brand":
        return "科技、克制、未来感"
    return "现代、清晰、品牌表达明确"


def _infer_layout_preference(prompt: str, industry_hint: str) -> str:
    if industry_hint == "burger_fast_food":
        return "大 Banner + 产品网格 + 促销横幅 + 卡片式菜单"
    if industry_hint == "coffee_brand":
        return "沉浸式首屏 + 品牌故事 + 饮品卡片 + 门店转化"
    if industry_hint == "dessert_brand":
        return "视觉主图 + 精选甜品 + 用户评价 + 活动区"
    if industry_hint == "fashion_brand":
        return "大图导向 + Lookbook 展示 + 产品矩阵 + 品牌故事"
    if industry_hint == "tech_product_brand":
        return "产品首屏 + 核心卖点 + 设备矩阵 + 用户口碑"
    if "高级" in prompt:
        return "非对称杂志感布局"
    return "均衡栅格商业布局"


def _derive_default_sections(industry_hint: str, prompt: str) -> List[str]:
    explicit = _match_sections(prompt)
    base = ["hero", "about", "products", "features", "testimonials", "promo", "contact", "footer"]
    if explicit:
        merged: List[str] = []
        for section in base:
            if section in explicit or section in {"hero", "products", "contact", "footer"}:
                merged.append(section)
        for section in explicit:
            if section not in merged:
                merged.append(section)
        if "footer" not in merged:
            merged.append("footer")
        return merged

    if industry_hint in {
        "burger_fast_food",
        "coffee_brand",
        "dessert_brand",
        "fashion_brand",
        "tech_product_brand",
        "restaurant_brand",
    }:
        return base

    return base


def _infer_special_notes(prompt: str, industry_hint: str) -> List[str]:
    notes: List[str] = ["默认生成中文文案与中文导航", "优先保证响应式与移动端体验"]
    notes.append(f"优先贴合{industry_label(industry_hint)}的行业视觉与内容结构")
    if industry_hint in {"burger_fast_food", "coffee_brand", "dessert_brand", "restaurant_brand"}:
        notes.append("自动生成与行业匹配的商品卡片、价格和图片关键词")
    if "表单" in prompt or "联系" in prompt:
        notes.append("联系与转化模块需要保持清晰、可行动")
    return notes


def _extract_color_palette(prompt: str, industry_hint: str) -> List[str]:
    color_terms = re.findall(r"[\u4e00-\u9fa5A-Za-z#0-9]{1,12}(?:色|色调|配色)", prompt)
    if color_terms:
        return color_terms[:4]
    return COLOR_HINTS.get(industry_hint, COLOR_HINTS["brand"])


def _build_local_analysis(prompt: str) -> PromptAnalysis:
    reference_brands = _extract_reference_brands(prompt)
    industry_hint = infer_industry(prompt, reference_brands)
    brand_name = _extract_brand_name(prompt, reference_brands)
    style_keywords = [value for key, value in STYLE_HINTS.items() if key in prompt] or ["modern", "commercial"]

    return PromptAnalysis(
        site_type=_infer_site_type(prompt, industry_hint),
        style_keywords=style_keywords,
        color_palette=_extract_color_palette(prompt, industry_hint),
        sections=_derive_default_sections(industry_hint, prompt),
        target_audience=_infer_audience(prompt, industry_hint),
        responsive_required=True,
        brand_tone=_infer_brand_tone(prompt, industry_hint),
        layout_preference=_infer_layout_preference(prompt, industry_hint),
        special_notes=_infer_special_notes(prompt, industry_hint),
        reference_brands=reference_brands,
        brand_name=brand_name,
        industry_hint=industry_hint,
        style_intent="先识别品牌或行业风格，再生成中文 Design Tokens、结构化页面规划和一次性组装代码。",
    )


def _merge_analysis(remote: PromptAnalysis, local: PromptAnalysis) -> PromptAnalysis:
    remote.reference_brands = remote.reference_brands or local.reference_brands
    remote.industry_hint = remote.industry_hint or local.industry_hint
    remote.brand_name = remote.brand_name or local.brand_name
    remote.sections = remote.sections or local.sections
    remote.color_palette = remote.color_palette or local.color_palette
    remote.style_keywords = remote.style_keywords or local.style_keywords
    remote.target_audience = remote.target_audience or local.target_audience
    remote.brand_tone = remote.brand_tone or local.brand_tone
    remote.layout_preference = remote.layout_preference or local.layout_preference
    remote.special_notes = remote.special_notes or local.special_notes
    remote.site_type = remote.site_type or local.site_type
    remote.responsive_required = True
    return remote


def analyze_prompt(prompt: str, ai_client: AIClient) -> PromptAnalysis:
    local = _build_local_analysis(prompt)

    if not ai_client.has_credentials:
        return local

    try:
        remote = ai_client.structured_json(
            system_prompt=(
                "你是网页需求分析器。请先理解用户提到的品牌风格或行业主题，输出结构化 JSON，语言保持中文。"
            ),
            user_prompt=(
                f"用户需求：{prompt}\n"
                "请重点识别品牌名称、行业类型、页面模块、目标用户、布局偏好、配色方向和风格关键词。"
            ),
            schema=PromptAnalysis,
        )
        if remote:
            return _merge_analysis(remote, local)
    except Exception:
        return local

    return local
