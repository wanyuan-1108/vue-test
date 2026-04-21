from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class PromptAnalysis(BaseModel):
    site_type: str = Field(default="brand")
    style_keywords: List[str] = Field(default_factory=list)
    color_palette: List[str] = Field(default_factory=list)
    sections: List[str] = Field(default_factory=list)
    target_audience: str = Field(default="general")
    responsive_required: bool = True
    brand_tone: str = Field(default="modern")
    layout_preference: str = Field(default="editorial")
    special_notes: List[str] = Field(default_factory=list)
    reference_brands: List[str] = Field(default_factory=list)
    brand_name: str = Field(default="")
    industry_hint: str = Field(default="general")
    style_intent: str = Field(default="Create a polished marketing website")


class DesignTokens(BaseModel):
    primary_color: str = "#7C5CFC"
    secondary_color: str = "#30246F"
    accent_color: str = "#76E5FF"
    background: str = "#0B1020"
    background_color: str = "#0B1020"
    surface: str = "rgba(17, 23, 43, 0.92)"
    font: str = "Inter, bold sans-serif"
    font_family: str = "Noto Sans SC"
    border_radius: str = "24px"
    button_style: str = "rounded high-contrast CTA"
    layout: str = "hero + feature grid + content split + contact"
    navbar_style: str = "floating brand navbar"
    card_style: str = "layered cards with soft shadow"
    image_style: str = "high-quality editorial visuals"
    image_keywords: List[str] = Field(default_factory=list)
    motion_style: str = "hover lift and soft glow"


class StyleAnalysis(BaseModel):
    brand_name: str = ""
    primary_color: str = "#7C5CFC"
    secondary_color: str = "#30246F"
    accent_color: str = "#76E5FF"
    background_color: str = "#0B1020"
    ui_style: str = "现代商业官网"
    layout: str = "hero + content sections"
    image_style: str = "高质量品牌视觉"
    image_keywords: List[str] = Field(default_factory=list)
    button_style: str = "rounded CTA"
    font_family: str = "Noto Sans SC"
    rationale: str = ""


class UIStructure(BaseModel):
    layout_summary: str = ""
    navigation: List[str] = Field(default_factory=list)
    sections: List[Dict[str, str]] = Field(default_factory=list)
    experience_notes: List[str] = Field(default_factory=list)


class StyleDNA(BaseModel):
    source_mode: Literal["prompt_only", "brand_reference", "mixed"] = "prompt_only"
    brand_name: str = ""
    industry_hint: str = "general"
    reference_summary: str = ""
    visual_keywords: List[str] = Field(default_factory=list)
    palette_rationale: str = ""
    palette: List[str] = Field(default_factory=list)
    ui_style: str = ""
    typography_direction: str = ""
    font_style: str = ""
    layout_direction: str = ""
    layout_pattern: str = ""
    component_direction: str = ""
    button_style: str = ""
    imagery_direction: str = ""
    image_style: str = ""
    interaction_direction: str = ""
    motion_style: str = ""
    style_variant: Literal[
        "editorial_luxury",
        "playful_brand",
        "tech_glow",
        "minimal_product",
        "sport_energy",
        "clean_corporate",
    ] = "clean_corporate"
    hero_background: str = "#111111"
    panel_background: str = "rgba(255,255,255,0.05)"
    card_background: str = "rgba(255,255,255,0.08)"
    border_color: str = "rgba(255,255,255,0.12)"
    primary_color: str = "#7C5CFC"
    secondary_color: str = "#30246F"
    accent_color: str = "#76E5FF"
    text_color: str = "#F6F8FF"
    muted_text_color: str = "#95A0BF"
    hero_foreground: str = "#F6F8FF"
    card_foreground: str = "#F6F8FF"
    nav_background: str = "rgba(0,0,0,0.28)"
    primary_button_text: str = "#0B1020"
    page_background: str = "#0B1020"
    image_keywords: List[str] = Field(default_factory=list)
    style_analysis: StyleAnalysis = Field(default_factory=StyleAnalysis)
    design_tokens: DesignTokens = Field(default_factory=DesignTokens)


class SectionPlan(BaseModel):
    id: str
    type: str
    title: str
    subtitle: str
    body: str
    cta_label: Optional[str] = None
    cta_href: Optional[str] = None
    items: List[Dict[str, str]] = Field(default_factory=list)


class ThemeConfig(BaseModel):
    mode: Literal["dark", "light"] = "dark"
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text: str
    muted_text: str
    font_heading: str = "Inter"
    font_body: str = "Inter"
    radius: str = "1.5rem"
    shadow_style: str = "0 20px 80px rgba(0,0,0,0.35)"
    spacing: str = "spacious"
    style_variant: str = "clean_corporate"
    hero_background: str = "#111111"
    hero_foreground: str = "#F6F8FF"
    panel_background: str = "rgba(255,255,255,0.05)"
    card_background: str = "rgba(255,255,255,0.08)"
    card_foreground: str = "#F6F8FF"
    border_color: str = "rgba(255,255,255,0.12)"
    nav_background: str = "rgba(0,0,0,0.28)"
    primary_button_text: str = "#0B1020"
    font_display: str = "Inter"
    button_style: str = "rounded high-contrast CTA"
    layout_pattern: str = "hero + feature grid + content split + contact"
    image_style: str = "high-quality editorial visuals"
    motion_style: str = "hover lift and soft glow"
    design_tokens: DesignTokens = Field(default_factory=DesignTokens)


class PagePlan(BaseModel):
    site_name: str
    page_title: str
    seo_description: str
    navigation: List[str] = Field(default_factory=list)
    sections: List[SectionPlan] = Field(default_factory=list)
    footer_note: str = "Crafted by DesignGen"
    style_dna: Optional[StyleDNA] = None
    ui_structure: Optional[UIStructure] = None


class GeneratedWebsite(BaseModel):
    title: str = "AI Generated Website"
    summary: str = ""
    html: str
    css: str = ""
    javascript: str = ""


class GeneratedBundle(BaseModel):
    project_files: Dict[str, str]
    preview_files: Dict[str, str]
    entry_file: str = "index.html"
    preview_entry: str = "/index.html"


class GenerationLog(BaseModel):
    stage: str
    status: Literal["pending", "running", "completed", "failed"]
    detail: str
