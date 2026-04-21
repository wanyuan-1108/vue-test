from __future__ import annotations

from copy import deepcopy

from app.schemas.design import DesignTokens, PromptAnalysis, StyleAnalysis, StyleDNA
from app.services.ai_client import AIClient
from app.services.generators.catalog import get_image_keywords, industry_label


def _tokens(
    primary: str,
    secondary: str,
    accent: str,
    background: str,
    surface: str,
    *,
    font: str,
    font_family: str,
    border_radius: str,
    button_style: str,
    layout: str,
    navbar_style: str,
    card_style: str,
    image_style: str,
    image_keywords: list[str],
    motion_style: str,
) -> DesignTokens:
    return DesignTokens(
        primary_color=primary,
        secondary_color=secondary,
        accent_color=accent,
        background=background,
        background_color=background,
        surface=surface,
        font=font,
        font_family=font_family,
        border_radius=border_radius,
        button_style=button_style,
        layout=layout,
        navbar_style=navbar_style,
        card_style=card_style,
        image_style=image_style,
        image_keywords=image_keywords,
        motion_style=motion_style,
    )


def _style_analysis(style_dna: StyleDNA) -> StyleAnalysis:
    return StyleAnalysis(
        brand_name=style_dna.brand_name,
        primary_color=style_dna.primary_color,
        secondary_color=style_dna.secondary_color,
        accent_color=style_dna.accent_color,
        background_color=style_dna.page_background,
        ui_style=style_dna.ui_style,
        layout=style_dna.layout_pattern,
        image_style=style_dna.image_style,
        image_keywords=style_dna.image_keywords,
        button_style=style_dna.button_style,
        font_family=style_dna.design_tokens.font_family,
        rationale=style_dna.reference_summary,
    )


def _clone(style_dna: StyleDNA) -> StyleDNA:
    return StyleDNA.model_validate(deepcopy(style_dna.model_dump()))


def _finalize(style_dna: StyleDNA) -> StyleDNA:
    style_dna.style_analysis = _style_analysis(style_dna)
    if not style_dna.design_tokens.image_keywords:
        style_dna.design_tokens.image_keywords = list(style_dna.image_keywords)
    return style_dna


def _brand_style(
    *,
    brand_name: str,
    industry_hint: str,
    reference_summary: str,
    visual_keywords: list[str],
    palette_rationale: str,
    palette: list[str],
    ui_style: str,
    typography_direction: str,
    font_style: str,
    layout_direction: str,
    layout_pattern: str,
    component_direction: str,
    button_style: str,
    imagery_direction: str,
    image_style: str,
    interaction_direction: str,
    motion_style: str,
    style_variant: str,
    hero_background: str,
    panel_background: str,
    card_background: str,
    border_color: str,
    primary_color: str,
    secondary_color: str,
    accent_color: str,
    text_color: str,
    muted_text_color: str,
    hero_foreground: str,
    card_foreground: str,
    nav_background: str,
    primary_button_text: str,
    page_background: str,
    image_keywords: list[str],
    font_family: str = "Noto Sans SC",
    radius: str = "20px",
) -> StyleDNA:
    return StyleDNA(
        source_mode="prompt_only",
        brand_name=brand_name,
        industry_hint=industry_hint,
        reference_summary=reference_summary,
        visual_keywords=visual_keywords,
        palette_rationale=palette_rationale,
        palette=palette,
        ui_style=ui_style,
        typography_direction=typography_direction,
        font_style=font_style,
        layout_direction=layout_direction,
        layout_pattern=layout_pattern,
        component_direction=component_direction,
        button_style=button_style,
        imagery_direction=imagery_direction,
        image_style=image_style,
        interaction_direction=interaction_direction,
        motion_style=motion_style,
        style_variant=style_variant,
        hero_background=hero_background,
        panel_background=panel_background,
        card_background=card_background,
        border_color=border_color,
        primary_color=primary_color,
        secondary_color=secondary_color,
        accent_color=accent_color,
        text_color=text_color,
        muted_text_color=muted_text_color,
        hero_foreground=hero_foreground,
        card_foreground=card_foreground,
        nav_background=nav_background,
        primary_button_text=primary_button_text,
        page_background=page_background,
        image_keywords=image_keywords,
        design_tokens=_tokens(
            primary_color,
            secondary_color,
            accent_color,
            page_background,
            card_background,
            font=font_style,
            font_family=font_family,
            border_radius=radius,
            button_style=button_style,
            layout=layout_pattern,
            navbar_style=layout_direction,
            card_style=component_direction,
            image_style=image_style,
            image_keywords=image_keywords,
            motion_style=motion_style,
        ),
    )


BRAND_PRESETS = {
    "mcdonalds": _brand_style(
        brand_name="McDonald's",
        industry_hint="burger_fast_food",
        reference_summary="识别到麦当劳风格，采用红黄品牌配色、快餐商业官网布局和高饱和食品视觉。",
        visual_keywords=["红黄品牌色", "商业快餐", "大横幅", "卡片式菜单", "强转化 CTA"],
        palette_rationale="以麦当劳经典红黄作为主视觉，白色用于留白和产品承托。",
        palette=["#DA291C", "#8F180F", "#FFC72C", "#FFFFFF"],
        ui_style="全球快餐品牌官网",
        typography_direction="粗体无衬线，强调醒目标题和价格信息",
        font_style="700 1rem/1.6 'Noto Sans SC', sans-serif",
        layout_direction="顶部品牌导航 + 大幅 Banner + 产品卡片 + 活动横幅 + 评价 + 转化表单",
        layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
        component_direction="高饱和商品卡片、强对比按钮、促销横幅模块",
        button_style="rounded yellow CTA",
        imagery_direction="高饱和食物近景、明亮商业拍摄、强调食欲与速度感",
        image_style="高饱和餐饮产品图",
        interaction_direction="按钮与卡片 hover 提升转化感",
        motion_style="hover lift + soft shadow + subtle scale",
        style_variant="playful_brand",
        hero_background="#FFF1E8",
        panel_background="rgba(255,255,255,0.88)",
        card_background="#FFFFFF",
        border_color="rgba(218,41,28,0.12)",
        primary_color="#DA291C",
        secondary_color="#8F180F",
        accent_color="#FFC72C",
        text_color="#2A160F",
        muted_text_color="#6B4C43",
        hero_foreground="#2A160F",
        card_foreground="#2A160F",
        nav_background="rgba(218,41,28,0.96)",
        primary_button_text="#572400",
        page_background="#FFF8F2",
        image_keywords=get_image_keywords("burger_fast_food") + ["fast food", "burger meal"],
        radius="18px",
    ),
    "starbucks": _brand_style(
        brand_name="Starbucks",
        industry_hint="coffee_brand",
        reference_summary="识别到星巴克风格，采用深绿与暖白配色，营造都市咖啡馆的精致生活方式。",
        visual_keywords=["深绿", "温暖木质", "精品咖啡", "生活方式", "门店氛围"],
        palette_rationale="主色采用深绿与米白，辅以咖啡棕提升温暖感。",
        palette=["#006241", "#1E3932", "#D4A373", "#F6F1EB"],
        ui_style="精品咖啡品牌官网",
        typography_direction="中文无衬线搭配精致留白，强化生活方式内容感",
        font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
        layout_direction="杂志感 Hero + 故事区 + 饮品网格 + 会员活动 + 评价",
        layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
        component_direction="咖啡卡片、故事卡、门店与会员促销模块",
        button_style="rounded green CTA",
        imagery_direction="暖调咖啡杯、门店环境、桌面静物与生活方式画面",
        image_style="精品咖啡生活方式图片",
        interaction_direction="缓和 hover 与卡片浮层",
        motion_style="soft fade + hover lift",
        style_variant="editorial_luxury",
        hero_background="#F5EEE6",
        panel_background="rgba(255,255,255,0.9)",
        card_background="#FFFFFF",
        border_color="rgba(0,98,65,0.12)",
        primary_color="#006241",
        secondary_color="#1E3932",
        accent_color="#D4A373",
        text_color="#1E2A28",
        muted_text_color="#61706D",
        hero_foreground="#1E2A28",
        card_foreground="#1E2A28",
        nav_background="rgba(255,255,255,0.88)",
        primary_button_text="#FFFFFF",
        page_background="#FAF7F2",
        image_keywords=get_image_keywords("coffee_brand") + ["coffee shop", "coffee beans"],
        radius="22px",
    ),
    "apple": _brand_style(
        brand_name="Apple",
        industry_hint="tech_product_brand",
        reference_summary="识别到 Apple 风格，采用克制的黑白灰、极简排版与大产品图。",
        visual_keywords=["极简", "科技产品", "黑白灰", "大留白", "硬件质感"],
        palette_rationale="以黑白灰为主，弱化装饰色，突出产品本身。",
        palette=["#111111", "#2D2D2D", "#8E8E93", "#F5F5F7"],
        ui_style="极简科技产品官网",
        typography_direction="大字号无衬线标题，留白充足，信息层级克制清晰",
        font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
        layout_direction="极简 Hero + 产品卖点 + 硬件矩阵 + 用户口碑",
        layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
        component_direction="浅色卡片、产品图主导、精简按钮与对比信息",
        button_style="rounded dark CTA",
        imagery_direction="设备特写、白底硬件图、工业设计细节",
        image_style="极简数码产品图片",
        interaction_direction="轻微浮动与遮罩渐变",
        motion_style="soft scale + fade",
        style_variant="minimal_product",
        hero_background="#F5F5F7",
        panel_background="rgba(255,255,255,0.96)",
        card_background="#FFFFFF",
        border_color="rgba(17,17,17,0.08)",
        primary_color="#111111",
        secondary_color="#2D2D2D",
        accent_color="#8E8E93",
        text_color="#111111",
        muted_text_color="#6E6E73",
        hero_foreground="#111111",
        card_foreground="#111111",
        nav_background="rgba(255,255,255,0.84)",
        primary_button_text="#FFFFFF",
        page_background="#FBFBFD",
        image_keywords=get_image_keywords("tech_product_brand") + ["apple style device"],
        radius="24px",
    ),
}


def _industry_fallback(analysis: PromptAnalysis) -> StyleDNA:
    industry = analysis.industry_hint or "brand"
    brand_name = analysis.brand_name or industry_label(industry)
    images = get_image_keywords(industry)

    if industry == "burger_fast_food":
        return _brand_style(
            brand_name=brand_name,
            industry_hint=industry,
            reference_summary="识别到汉堡快餐主题，采用红黄高对比配色与强视觉产品卡片布局。",
            visual_keywords=["快餐品牌", "热情红黄", "卡片菜单", "促销转化"],
            palette_rationale="红色增强食欲与速度感，黄色强化促销按钮和品牌识别。",
            palette=["#D62828", "#8F1D14", "#F9C74F", "#FFF8F0"],
            ui_style="汉堡快餐商业官网",
            typography_direction="粗体中文无衬线，强调标题、价格和活动信息",
            font_style="700 1rem/1.6 'Noto Sans SC', sans-serif",
            layout_direction="强促销导航 + 大 Banner + 产品网格 + 活动条幅 + 评价",
            layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
            component_direction="商品卡片配价格与按钮，促销模块强化优惠信息",
            button_style="rounded yellow CTA",
            imagery_direction="近景食品图片、明亮布光、真实套餐场景",
            image_style="高饱和快餐商品图",
            interaction_direction="卡片与按钮 hover 强反馈",
            motion_style="hover lift + shadow",
            style_variant="playful_brand",
            hero_background="#FFF2E2",
            panel_background="rgba(255,255,255,0.92)",
            card_background="#FFFFFF",
            border_color="rgba(214,40,40,0.12)",
            primary_color="#D62828",
            secondary_color="#8F1D14",
            accent_color="#F9C74F",
            text_color="#2F1C14",
            muted_text_color="#755B52",
            hero_foreground="#2F1C14",
            card_foreground="#2F1C14",
            nav_background="rgba(214,40,40,0.95)",
            primary_button_text="#512100",
            page_background="#FFF9F3",
            image_keywords=images + ["burger meal", "fast food combo"],
            radius="18px",
        )

    if industry == "coffee_brand":
        return _brand_style(
            brand_name=brand_name,
            industry_hint=industry,
            reference_summary="识别到咖啡品牌主题，采用咖啡棕、米白和精品生活方式视觉。",
            visual_keywords=["咖啡馆", "木质暖调", "精致生活", "门店氛围"],
            palette_rationale="以咖啡棕和奶油白构建舒适、治愈且现代的品牌感。",
            palette=["#6F4E37", "#3E2C23", "#DDB892", "#F8F4EE"],
            ui_style="精品咖啡品牌官网",
            typography_direction="细腻中文排版，强调温暖生活方式与产品细节",
            font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
            layout_direction="沉浸 Hero + 品牌故事 + 饮品产品墙 + 会员活动",
            layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
            component_direction="饮品卡片、故事卡与活动卡并置展示",
            button_style="rounded warm CTA",
            imagery_direction="咖啡杯、咖啡豆、门店与桌面生活方式图片",
            image_style="精品咖啡暖调图片",
            interaction_direction="柔和 hover 与轻量阴影",
            motion_style="soft fade + hover lift",
            style_variant="editorial_luxury",
            hero_background="#F5EFE7",
            panel_background="rgba(255,255,255,0.92)",
            card_background="#FFFFFF",
            border_color="rgba(111,78,55,0.12)",
            primary_color="#6F4E37",
            secondary_color="#3E2C23",
            accent_color="#DDB892",
            text_color="#2C221D",
            muted_text_color="#74645A",
            hero_foreground="#2C221D",
            card_foreground="#2C221D",
            nav_background="rgba(255,255,255,0.84)",
            primary_button_text="#FFFFFF",
            page_background="#FCF9F6",
            image_keywords=images + ["coffee shop", "coffee beans"],
            radius="22px",
        )

    if industry == "dessert_brand":
        return _brand_style(
            brand_name=brand_name,
            industry_hint=industry,
            reference_summary="识别到甜品品牌主题，采用奶油白、粉色和甜点产品图，强化高颜值体验。",
            visual_keywords=["高颜值", "甜品礼盒", "柔和粉色", "卡片商品"],
            palette_rationale="粉色与奶油白强化甜品品牌的轻甜与分享氛围。",
            palette=["#F28482", "#D96C75", "#F6BD60", "#FFF8F7"],
            ui_style="甜品品牌官网",
            typography_direction="柔和但清晰的中文无衬线排版",
            font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
            layout_direction="视觉首屏 + 精选甜品卡片 + 用户评价 + 节日活动",
            layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
            component_direction="大图甜品卡片、推荐标签与礼盒活动区",
            button_style="rounded bright CTA",
            imagery_direction="蛋糕、冰淇淋、甜甜圈等高颜值产品图",
            image_style="精致甜品商业图片",
            interaction_direction="轻微缩放与柔和阴影",
            motion_style="hover lift + gentle glow",
            style_variant="playful_brand",
            hero_background="#FFF5F5",
            panel_background="rgba(255,255,255,0.94)",
            card_background="#FFFFFF",
            border_color="rgba(242,132,130,0.12)",
            primary_color="#F28482",
            secondary_color="#D96C75",
            accent_color="#F6BD60",
            text_color="#3A2B2B",
            muted_text_color="#806B6B",
            hero_foreground="#3A2B2B",
            card_foreground="#3A2B2B",
            nav_background="rgba(255,255,255,0.9)",
            primary_button_text="#5A2A2A",
            page_background="#FFFDFB",
            image_keywords=images + ["dessert table", "cake shop"],
            radius="20px",
        )

    if industry == "fashion_brand":
        return _brand_style(
            brand_name=brand_name,
            industry_hint=industry,
            reference_summary="识别到时尚品牌主题，采用黑白灰与高级质感大图，强调 Lookbook 与穿搭感。",
            visual_keywords=["高级黑白灰", "时尚大片", "穿搭矩阵", "品牌态度"],
            palette_rationale="黑白灰强化品牌调性，暖灰用于提升质感与亲和力。",
            palette=["#111111", "#2E2E2E", "#D6C7B0", "#F7F3EE"],
            ui_style="时尚品牌官网",
            typography_direction="大标题排版与留白结合，营造编辑感",
            font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
            layout_direction="视觉大片 Hero + Lookbook + 商品矩阵 + 口碑展示",
            layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
            component_direction="大片卡片与穿搭组合卡片并置",
            button_style="rounded monochrome CTA",
            imagery_direction="服装穿搭大片、细节面料与模特场景图",
            image_style="时尚品牌大片",
            interaction_direction="卡片 hover 位移与浅描边",
            motion_style="hover raise + fade",
            style_variant="editorial_luxury",
            hero_background="#F4EFE8",
            panel_background="rgba(255,255,255,0.92)",
            card_background="#FFFFFF",
            border_color="rgba(17,17,17,0.08)",
            primary_color="#111111",
            secondary_color="#2E2E2E",
            accent_color="#D6C7B0",
            text_color="#1A1A1A",
            muted_text_color="#6B6B6B",
            hero_foreground="#1A1A1A",
            card_foreground="#1A1A1A",
            nav_background="rgba(255,255,255,0.84)",
            primary_button_text="#FFFFFF",
            page_background="#FCFAF7",
            image_keywords=images + ["fashion editorial", "lookbook"],
            radius="22px",
        )

    if industry == "tech_product_brand":
        return _brand_style(
            brand_name=brand_name,
            industry_hint=industry,
            reference_summary="识别到科技产品主题，采用深色科技背景、冷色高光与产品矩阵布局。",
            visual_keywords=["科技发光", "深色界面", "产品矩阵", "未来感"],
            palette_rationale="以深蓝和电光青作为科技高光，强化未来感和硬件质感。",
            palette=["#0B1020", "#151B32", "#76E5FF", "#F7FBFF"],
            ui_style="科技产品官网",
            typography_direction="干净有力的中文无衬线，强调参数与卖点层级",
            font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
            layout_direction="产品 Hero + 卖点网格 + 设备卡片 + 评价 + 联系入口",
            layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
            component_direction="玻璃质感卡片与参数模块组合",
            button_style="rounded cyan CTA",
            imagery_direction="数码设备、发光背景与产品渲染图",
            image_style="科技硬件产品图",
            interaction_direction="hover glow 与描边增强",
            motion_style="hover glow + subtle translate",
            style_variant="tech_glow",
            hero_background="#0E1428",
            panel_background="rgba(18,24,46,0.82)",
            card_background="rgba(20,27,50,0.9)",
            border_color="rgba(118,229,255,0.18)",
            primary_color="#4F7CFF",
            secondary_color="#151B32",
            accent_color="#76E5FF",
            text_color="#F6F8FF",
            muted_text_color="#95A0BF",
            hero_foreground="#F6F8FF",
            card_foreground="#F6F8FF",
            nav_background="rgba(10,14,27,0.82)",
            primary_button_text="#0B1020",
            page_background="#0B1020",
            image_keywords=images + ["tech device", "future product"],
            radius="24px",
        )

    return _brand_style(
        brand_name=brand_name,
        industry_hint="brand",
        reference_summary="未命中特定品牌预设，已基于品牌官网通用逻辑生成现代商业视觉系统。",
        visual_keywords=["现代品牌", "中文商业官网", "卡片布局", "清晰转化"],
        palette_rationale="使用偏现代的蓝紫色作为通用品牌主色，便于兼容多种主题。",
        palette=["#6D5EF8", "#2C2F58", "#6EE7F9", "#F5F7FF"],
        ui_style="现代品牌官网",
        typography_direction="中文无衬线，标题清晰，信息层级明确",
        font_style="600 1rem/1.7 'Noto Sans SC', sans-serif",
        layout_direction="大首屏 + 品牌介绍 + 产品卡片 + 推荐 + 评价 + 联系",
        layout_pattern="navbar + hero + about + products + highlights + testimonials + promo + contact + footer",
        component_direction="内容卡片与 CTA 组件平衡布局",
        button_style="rounded primary CTA",
        imagery_direction="高质量品牌相关配图与场景图",
        image_style="现代商业品牌图片",
        interaction_direction="柔和 hover 和阴影反馈",
        motion_style="hover lift + shadow",
        style_variant="clean_corporate",
        hero_background="#EEF2FF",
        panel_background="rgba(255,255,255,0.92)",
        card_background="#FFFFFF",
        border_color="rgba(109,94,248,0.12)",
        primary_color="#6D5EF8",
        secondary_color="#2C2F58",
        accent_color="#6EE7F9",
        text_color="#171A2D",
        muted_text_color="#667085",
        hero_foreground="#171A2D",
        card_foreground="#171A2D",
        nav_background="rgba(255,255,255,0.84)",
        primary_button_text="#FFFFFF",
        page_background="#F7F9FF",
        image_keywords=images or ["brand showcase", "marketing website"],
        radius="22px",
    )


def _merge_prompt_preferences(style_dna: StyleDNA, analysis: PromptAnalysis, prompt: str) -> StyleDNA:
    merged = _clone(style_dna)
    lowered = prompt.lower()

    if analysis.brand_name and not merged.brand_name:
        merged.brand_name = analysis.brand_name

    if "极简" in prompt and merged.style_variant != "minimal_product":
        merged.card_background = "#FFFFFF"
        merged.panel_background = "rgba(255,255,255,0.92)"
        merged.border_color = "rgba(17,17,17,0.08)"
        merged.motion_style = "soft hover lift"

    if "暗色" in prompt or "深色" in prompt:
        merged.page_background = "#0B1020"
        merged.hero_background = "#10182D"
        merged.text_color = "#F6F8FF"
        merged.card_foreground = "#F6F8FF"
        merged.hero_foreground = "#F6F8FF"
        merged.nav_background = "rgba(10,14,27,0.82)"
        if merged.style_variant == "clean_corporate":
            merged.style_variant = "tech_glow"

    if "高级" in prompt:
        merged.layout_direction = "杂志感大图布局 + 精细留白 + 高级卡片信息排布"
        merged.motion_style = "subtle hover lift + elegant fade"

    if any(word in lowered for word in ["红", "红色"]) and merged.primary_color.startswith("#6D"):
        merged.primary_color = "#D62828"
        merged.accent_color = "#F9C74F"

    merged.design_tokens = _tokens(
        merged.primary_color,
        merged.secondary_color,
        merged.accent_color,
        merged.page_background,
        merged.card_background,
        font=merged.font_style,
        font_family=merged.design_tokens.font_family or "Noto Sans SC",
        border_radius=merged.design_tokens.border_radius,
        button_style=merged.button_style,
        layout=merged.layout_pattern,
        navbar_style=merged.layout_direction,
        card_style=merged.component_direction,
        image_style=merged.image_style,
        image_keywords=merged.image_keywords,
        motion_style=merged.motion_style,
    )
    return merged


def build_style_dna(prompt: str, analysis: PromptAnalysis, ai_client: AIClient) -> StyleDNA:
    base = None
    if analysis.reference_brands:
        preset = BRAND_PRESETS.get(analysis.reference_brands[0])
        if preset:
            base = _clone(preset)
            base.source_mode = "brand_reference"

    if base is None:
        base = _industry_fallback(analysis)

    base.brand_name = analysis.brand_name or base.brand_name
    base.industry_hint = analysis.industry_hint or base.industry_hint

    merged = _merge_prompt_preferences(base, analysis, prompt)
    return _finalize(merged)
