from __future__ import annotations

from app.schemas.design import PagePlan, PromptAnalysis, SectionPlan, StyleDNA, UIStructure
from app.services.ai_client import AIClient
from app.services.generators.catalog import get_featured_products, get_products, industry_label


def _site_name(analysis: PromptAnalysis, style_dna: StyleDNA) -> str:
    if analysis.brand_name:
        return analysis.brand_name
    if style_dna.brand_name:
        return style_dna.brand_name
    return industry_label(analysis.industry_hint)


def _navigation(industry_hint: str) -> list[str]:
    if industry_hint in {"burger_fast_food", "coffee_brand", "dessert_brand", "restaurant_brand"}:
        return ["首页", "品牌故事", "热门产品", "特色推荐", "优惠活动", "用户评价", "联系我们"]
    return ["首页", "品牌介绍", "产品展示", "特色推荐", "用户评价", "优惠活动", "联系我们"]


def _hero_section(site_name: str, analysis: PromptAnalysis, style_dna: StyleDNA) -> SectionPlan:
    highlight_map = {
        "burger_fast_food": "现点现做、热卖套餐与高饱和品牌视觉",
        "coffee_brand": "精品饮品、门店氛围与都市生活方式",
        "dessert_brand": "高颜值甜品、节日礼盒与轻社交分享",
        "fashion_brand": "新品穿搭、品牌态度与视觉大片",
        "tech_product_brand": "核心科技、硬件设计与产品生态",
        "restaurant_brand": "主厨招牌、氛围感空间与精致菜品",
    }
    headline = f"让 {site_name} 的品牌视觉一眼被记住"
    subtitle = highlight_map.get(analysis.industry_hint, "通过统一设计语言、中文内容结构和真实产品展示，快速搭建高完成度品牌官网。")
    metrics = [
        {"label": "品牌识别", "value": "更鲜明"},
        {"label": "页面结构", "value": "更完整"},
        {"label": "移动体验", "value": "已适配"},
    ]
    return SectionPlan(
        id="hero",
        type="hero",
        title=headline,
        subtitle=subtitle,
        body=f"围绕{style_dna.ui_style}和“{analysis.brand_tone}”的品牌语气，强化首屏视觉、转化按钮与产品氛围。",
        cta_label="查看热门产品",
        cta_href="#products",
        items=metrics,
    )


def _about_section(site_name: str, analysis: PromptAnalysis, style_dna: StyleDNA) -> SectionPlan:
    body_map = {
        "burger_fast_food": f"{site_name} 以高辨识度品牌色、经典快餐组合和高效门店体验建立消费者记忆。页面通过大横幅、产品卡片与优惠活动强化商业转化。",
        "coffee_brand": f"{site_name} 强调咖啡风味、门店空间与生活方式表达。页面在品牌故事中融入温暖材质感和精致留白，突出都市咖啡体验。",
        "dessert_brand": f"{site_name} 通过高颜值甜品、节日礼盒和轻松分享氛围构建品牌情绪，让产品展示区更具吸引力与真实感。",
        "fashion_brand": f"{site_name} 通过品牌态度、穿搭场景和主推单品打造完整的时尚官网表达，兼顾视觉冲击与购买动机。",
        "tech_product_brand": f"{site_name} 以产品力为核心，通过卖点拆解、硬件矩阵和用户反馈建立科技品牌可信度。",
        "restaurant_brand": f"{site_name} 以主厨招牌菜、空间氛围和季节内容塑造精致餐饮体验，使页面更接近真实商业官网。",
    }
    items = [
        {"title": "品牌定位", "description": analysis.brand_tone, "badge": "品牌气质", "meta": analysis.target_audience},
        {"title": "页面布局", "description": analysis.layout_preference, "badge": "布局策略", "meta": "首页结构完整"},
        {"title": "视觉方向", "description": style_dna.reference_summary, "badge": "风格分析", "meta": style_dna.ui_style},
    ]
    return SectionPlan(
        id="about",
        type="about",
        title="品牌故事与视觉定位",
        subtitle=f"围绕 {site_name} 的品牌识别系统进行统一表达。",
        body=body_map.get(analysis.industry_hint, f"页面将围绕 {site_name} 的行业特征、目标用户和视觉语言生成中文商业官网内容。"),
        items=items,
    )


def _products_section(analysis: PromptAnalysis) -> SectionPlan:
    items = []
    for product in get_products(analysis.industry_hint):
        items.append(
            {
                "title": product["name"],
                "description": product["description"],
                "price": product["price"],
                "image_query": product["image_query"],
                "badge": product.get("tag", "热门产品"),
                "meta": product.get("meta", "品牌精选"),
            }
        )
    return SectionPlan(
        id="products",
        type="products",
        title="热门产品",
        subtitle="根据行业主题自动匹配真实商品内容与图片关键词。",
        body="每张产品卡片均包含图片、名称、卖点描述、示例价格与转化按钮，保证页面更接近真实商业官网。",
        cta_label="立即下单",
        cta_href="#contact",
        items=items,
    )


def _features_section(analysis: PromptAnalysis) -> SectionPlan:
    featured = get_featured_products(analysis.industry_hint)
    items = []
    for product in featured:
        items.append(
            {
                "title": product["name"],
                "description": f"聚焦 {product['name']} 的核心吸引力与品牌卖点，强化首页的推荐感和购买动机。",
                "badge": "特色推荐",
                "meta": product.get("tag", "精选内容"),
            }
        )
    if not items:
        items = [
            {"title": "品牌亮点一", "description": "强调品牌识别与视觉统一性。", "badge": "亮点", "meta": "视觉系统"},
            {"title": "品牌亮点二", "description": "突出真实产品与内容层级。", "badge": "亮点", "meta": "内容策略"},
            {"title": "品牌亮点三", "description": "优化响应式布局和转化路径。", "badge": "亮点", "meta": "用户体验"},
        ]
    return SectionPlan(
        id="features",
        type="features",
        title="特色推荐",
        subtitle="将行业标签、品牌风格和主推产品整合为高识别度内容模块。",
        body="这一部分承接首屏氛围，帮助用户快速理解品牌主张、爆款单品和购买理由。",
        items=items,
    )


def _testimonials_section(site_name: str, analysis: PromptAnalysis) -> SectionPlan:
    audience = analysis.target_audience or "目标用户"
    items = [
        {"quote": f"页面里的产品展示和图片很贴合 {industry_label(analysis.industry_hint)} 的真实场景，品牌感一下就出来了。", "author": "用户评价 · 林女士"},
        {"quote": f"从首屏到优惠活动再到产品卡片，整体结构很像成熟商业官网，特别适合吸引 {audience}。", "author": "用户评价 · 陈先生"},
        {"quote": f"{site_name} 的视觉语言、中文文案和转化路径很统一，看起来比普通模板更可信。", "author": "用户评价 · 张女士"},
    ]
    return SectionPlan(
        id="testimonials",
        type="testimonials",
        title="用户评价",
        subtitle="用真实感中文评价强化品牌信任与商业氛围。",
        body="评价区用于补强品牌可信度，让页面不仅有视觉冲击，也有口碑支撑。",
        items=items,
    )


def _promo_section(analysis: PromptAnalysis) -> SectionPlan:
    promo_map = {
        "burger_fast_food": [
            {"title": "超值双人套餐", "description": "热门汉堡 + 薯条 + 饮品组合，强化下单动机。"},
            {"title": "限时加价购", "description": "通过小食与饮品加购提升客单价与页面真实感。"},
            {"title": "到店优惠提醒", "description": "适合与门店活动、会员权益形成联动。"},
        ],
        "coffee_brand": [
            {"title": "第二杯半价", "description": "适合在会员活动和下午茶场景中强化转化。"},
            {"title": "新品风味季", "description": "结合冷萃、特调等内容制造新鲜感。"},
            {"title": "门店限定活动", "description": "通过城市门店内容增强品牌在地体验。"},
        ],
    }
    items = promo_map.get(
        analysis.industry_hint,
        [
            {"title": "品牌限时活动", "description": "通过时间限定机制强化页面行动召唤。"},
            {"title": "新客专享权益", "description": "适合在官网场景中承接注册、咨询或购买转化。"},
            {"title": "精选内容推荐", "description": "结合主推产品和品牌亮点提升浏览深度。"},
        ],
    )
    return SectionPlan(
        id="promo",
        type="promo",
        title="优惠活动",
        subtitle="通过横幅式促销内容强化转化氛围与页面节奏。",
        body="活动区与产品展示区相互呼应，使页面既有品牌感，也有明确的商业目标。",
        cta_label="领取优惠",
        cta_href="#contact",
        items=items,
    )


def _contact_section(site_name: str, analysis: PromptAnalysis) -> SectionPlan:
    items = [
        {"title": "联系电话", "description": "400-800-2026", "meta": "工作日 09:00 - 21:00"},
        {"title": "商务合作", "description": f"hello@{site_name.lower().replace(' ', '')}.com" if site_name else "hello@designgen.ai", "meta": "欢迎咨询合作"},
        {"title": "品牌地址", "description": "上海市徐汇区品牌创意中心 8F", "meta": "支持到店体验 / 商务洽谈"},
    ]
    return SectionPlan(
        id="contact",
        type="contact",
        title="联系我们",
        subtitle="保留清晰的咨询与转化入口，兼顾品牌展示与业务承接。",
        body=f"无论是了解 {site_name} 的产品、活动还是合作方式，都可以通过这里快速建立联系。",
        cta_label="提交咨询",
        cta_href="#contact",
        items=items,
    )


def _footer_section(site_name: str) -> SectionPlan:
    return SectionPlan(
        id="footer",
        type="footer",
        title="页脚",
        subtitle="",
        body=f"© 2026 {site_name} · 由 DesignGen 自动生成",
        items=[],
    )


def _build_ui_structure(navigation: list[str], sections: list[SectionPlan], style_dna: StyleDNA) -> UIStructure:
    return UIStructure(
        layout_summary=style_dna.layout_pattern,
        navigation=navigation,
        sections=[
            {"id": section.id, "title": section.title, "type": section.type, "summary": section.subtitle}
            for section in sections
        ],
        experience_notes=[
            "顶部导航固定品牌入口与关键模块锚点",
            "首屏强调品牌风格、CTA 和主题相关主视觉图片",
            "产品区使用卡片网格展示商品图片、价格和购买按钮",
            "优惠活动与评价区提高真实商业官网的完整度与可信度",
            "整体默认适配中文排版和响应式布局",
        ],
    )


def plan_page(analysis: PromptAnalysis, style_dna: StyleDNA, ai_client: AIClient) -> PagePlan:
    site_name = _site_name(analysis, style_dna)
    navigation = _navigation(analysis.industry_hint)
    sections = [
        _hero_section(site_name, analysis, style_dna),
        _about_section(site_name, analysis, style_dna),
        _products_section(analysis),
        _features_section(analysis),
        _testimonials_section(site_name, analysis),
        _promo_section(analysis),
        _contact_section(site_name, analysis),
        _footer_section(site_name),
    ]

    ui_structure = _build_ui_structure(navigation, sections, style_dna)
    return PagePlan(
        site_name=site_name,
        page_title=f"{site_name} | 中文品牌官网",
        seo_description=f"{site_name} 的中文品牌官网，包含品牌故事、产品展示、特色推荐、优惠活动和联系入口。",
        navigation=navigation,
        sections=sections,
        footer_note=f"© 2026 {site_name} · DesignGen",
        style_dna=style_dna,
        ui_structure=ui_structure,
    )
