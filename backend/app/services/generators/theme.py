from app.schemas.design import PromptAnalysis, StyleDNA, ThemeConfig
from app.services.ai_client import AIClient


def build_theme(analysis: PromptAnalysis, style_dna: StyleDNA, ai_client: AIClient) -> ThemeConfig:
    mode = "light" if style_dna.style_variant in {"minimal_product", "playful_brand"} else "dark"

    return ThemeConfig(
        mode=mode,
        primary=style_dna.primary_color,
        secondary=style_dna.secondary_color,
        accent=style_dna.accent_color,
        background=style_dna.page_background,
        surface=style_dna.design_tokens.surface,
        text="#151515" if mode == "light" and style_dna.text_color.lower() in {"#151515", "#1d1d1f"} else style_dna.text_color,
        muted_text="#6E6E73" if style_dna.style_variant == "minimal_product" else style_dna.muted_text_color,
        font_heading="Inter",
        font_body="Inter",
        radius=style_dna.design_tokens.border_radius,
        shadow_style="0 24px 80px rgba(0,0,0,0.18)" if mode == "light" else "0 20px 80px rgba(0,0,0,0.35)",
        spacing="spacious",
        style_variant=style_dna.style_variant,
        hero_background=style_dna.hero_background,
        hero_foreground=style_dna.hero_foreground,
        panel_background=style_dna.panel_background,
        card_background=style_dna.card_background,
        card_foreground=style_dna.card_foreground,
        border_color=style_dna.border_color,
        nav_background=style_dna.nav_background,
        primary_button_text=style_dna.primary_button_text,
        font_display=style_dna.font_style or style_dna.design_tokens.font,
        button_style=style_dna.button_style or style_dna.design_tokens.button_style,
        layout_pattern=style_dna.layout_pattern or style_dna.design_tokens.layout,
        image_style=style_dna.image_style or style_dna.design_tokens.image_style,
        motion_style=style_dna.motion_style or style_dna.design_tokens.motion_style,
        design_tokens=style_dna.design_tokens,
    )
