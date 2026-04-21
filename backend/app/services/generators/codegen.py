from __future__ import annotations

import json
from typing import Dict, List
from urllib.parse import quote_plus

from app.schemas.design import GeneratedBundle, PagePlan, SectionPlan, ThemeConfig


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _image_url(query: str, width: int = 1200, height: int = 800) -> str:
    safe_query = quote_plus((query or "brand website").strip())
    return f"https://source.unsplash.com/featured/{width}x{height}/?{safe_query}"


def _hero_query(page_plan: PagePlan) -> str:
    style_dna = page_plan.style_dna
    if style_dna and style_dna.image_keywords:
        return style_dna.image_keywords[0]
    return f"{page_plan.site_name} brand"


def _section_label(section_type: str) -> str:
    labels = {
        "hero": "品牌首屏",
        "about": "品牌故事",
        "products": "热门产品",
        "features": "特色推荐",
        "testimonials": "用户评价",
        "promo": "优惠活动",
        "contact": "联系我们",
        "footer": "页脚",
    }
    return labels.get(section_type, "内容模块")


def _theme_vars(theme: ThemeConfig) -> str:
    return f"""
:root {{
  --primary: {theme.primary};
  --secondary: {theme.secondary};
  --accent: {theme.accent};
  --background: {theme.background};
  --surface: {theme.surface};
  --text: {theme.text};
  --muted: {theme.muted_text};
  --hero-bg: {theme.hero_background};
  --hero-fg: {theme.hero_foreground};
  --card-bg: {theme.card_background};
  --card-fg: {theme.card_foreground};
  --border: {theme.border_color};
  --nav-bg: {theme.nav_background};
  --button-text: {theme.primary_button_text};
  --radius: {theme.radius};
  --shadow: {theme.shadow_style};
  --font-body: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
}}
""".strip()


def _build_css(theme: ThemeConfig) -> str:
    return """@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;800&display=swap');

__THEME_VARS__

* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  font-family: var(--font-body);
  background:
    radial-gradient(circle at top right, color-mix(in srgb, var(--accent) 16%, transparent), transparent 32%),
    linear-gradient(180deg, var(--background) 0%, color-mix(in srgb, var(--background) 92%, white) 100%);
  color: var(--text);
}}
a {{ color: inherit; text-decoration: none; }}
img {{ display: block; max-width: 100%; }}
.page-shell {{ min-height: 100vh; }}
.container {{ width: min(1200px, calc(100% - 32px)); margin: 0 auto; }}
.site-header {{ position: sticky; top: 0; z-index: 40; backdrop-filter: blur(18px); background: var(--nav-bg); border-bottom: 1px solid color-mix(in srgb, var(--border) 85%, transparent); }}
.header-inner {{ display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 18px 0; }}
.hero-section, .section-shell {{ scroll-margin-top: 96px; }}
.brand-mark {{ display: inline-flex; align-items: center; gap: 12px; font-weight: 800; color: var(--text); }}
.brand-dot {{ width: 14px; height: 14px; border-radius: 999px; background: linear-gradient(135deg, var(--primary), var(--accent)); box-shadow: 0 0 0 6px color-mix(in srgb, var(--primary) 12%, transparent); }}
.site-nav {{ display: flex; gap: 18px; flex-wrap: wrap; justify-content: flex-end; }}
.site-nav a {{ color: var(--muted); font-size: 14px; font-weight: 600; }}
.site-nav a:hover {{ color: var(--text); }}
.hero-section {{ padding: 48px 0 28px; }}
.hero-grid {{ display: grid; grid-template-columns: 1.06fr 0.94fr; gap: 28px; align-items: stretch; }}
.hero-copy, .hero-media {{ border-radius: calc(var(--radius) + 6px); overflow: hidden; box-shadow: var(--shadow); }}
.hero-copy {{ padding: 36px; background: linear-gradient(135deg, color-mix(in srgb, var(--hero-bg) 82%, white), color-mix(in srgb, var(--primary) 16%, var(--hero-bg))); color: var(--hero-fg); display: flex; flex-direction: column; justify-content: space-between; min-height: 520px; }}
.hero-copy h1 {{ margin: 14px 0 16px; font-size: clamp(2.3rem, 5vw, 4.6rem); line-height: 1.06; letter-spacing: -0.04em; }}
.hero-copy p {{ margin: 0; font-size: 16px; line-height: 1.9; color: color-mix(in srgb, var(--hero-fg) 86%, transparent); }}
.eyebrow {{ display: inline-flex; width: fit-content; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; background: color-mix(in srgb, var(--accent) 14%, white 32%); color: color-mix(in srgb, var(--text) 84%, var(--primary)); font-size: 12px; font-weight: 700; letter-spacing: 0.08em; }}
.action-row {{ display: flex; flex-wrap: wrap; gap: 14px; margin-top: 28px; }}
.primary-button, .secondary-button, .buy-button {{ border: none; display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 0 20px; border-radius: 999px; font-weight: 700; transition: transform .2s ease, box-shadow .2s ease; cursor: pointer; }}
.primary-button, .buy-button {{ background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 75%, var(--primary))); color: var(--button-text); box-shadow: 0 14px 30px color-mix(in srgb, var(--accent) 28%, transparent); }}
.secondary-button {{ background: color-mix(in srgb, var(--card-bg) 88%, transparent); color: var(--text); border: 1px solid var(--border); }}
.primary-button:hover, .secondary-button:hover, .buy-button:hover {{ transform: translateY(-2px); }}
.metric-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 32px; }}
.metric-card {{ padding: 18px; border-radius: 18px; background: color-mix(in srgb, var(--card-bg) 84%, transparent); border: 1px solid color-mix(in srgb, var(--border) 75%, transparent); }}
.metric-card span {{ display: block; color: var(--muted); font-size: 13px; margin-bottom: 6px; }}
.metric-card strong {{ font-size: 1.15rem; }}
.hero-media {{ position: relative; min-height: 520px; background: var(--card-bg); }}
.hero-media img {{ width: 100%; height: 100%; object-fit: cover; }}
.section-shell {{ padding: 18px 0 10px; }}
.section-card {{ border-radius: calc(var(--radius) + 4px); background: color-mix(in srgb, var(--surface) 90%, white 10%); border: 1px solid var(--border); box-shadow: var(--shadow); padding: 28px; }}
.section-head {{ display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 24px; flex-wrap: wrap; }}
.section-head h2 {{ margin: 12px 0 10px; font-size: clamp(1.6rem, 3vw, 2.5rem); line-height: 1.12; }}
.section-head p {{ margin: 0; max-width: 720px; color: var(--muted); line-height: 1.9; }}
.content-grid, .product-grid, .testimonial-grid, .contact-grid, .promo-grid {{ display: grid; gap: 18px; }}
.content-grid, .product-grid, .testimonial-grid, .contact-grid, .promo-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
.info-card, .promo-card, .testimonial-card, .contact-card, .product-card {{ border-radius: 22px; background: var(--card-bg); color: var(--card-fg); border: 1px solid var(--border); overflow: hidden; transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }}
.info-card:hover, .promo-card:hover, .testimonial-card:hover, .contact-card:hover, .product-card:hover {{ transform: translateY(-4px); box-shadow: 0 24px 60px color-mix(in srgb, var(--primary) 14%, transparent); border-color: color-mix(in srgb, var(--primary) 22%, var(--border)); }}
.info-card, .promo-card, .testimonial-card, .contact-card {{ padding: 22px; }}
.product-card img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }}
.product-card-body {{ padding: 20px; display: flex; flex-direction: column; gap: 12px; }}
.product-topline {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
.badge {{ display: inline-flex; width: fit-content; padding: 6px 10px; border-radius: 999px; background: color-mix(in srgb, var(--primary) 12%, white); color: var(--primary); font-size: 12px; font-weight: 700; }}
.meta {{ color: var(--muted); font-size: 13px; }}
.product-card h3, .info-card h3, .promo-card h3, .contact-card h3 {{ margin: 0; font-size: 1.2rem; }}
.product-card p, .info-card p, .promo-card p, .contact-card p, .testimonial-card p {{ margin: 0; color: var(--muted); line-height: 1.85; }}
.price-row {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 4px; }}
.price-tag {{ font-size: 1.35rem; font-weight: 800; color: var(--primary); }}
.promo-banner {{ background: linear-gradient(135deg, color-mix(in srgb, var(--primary) 10%, white), color-mix(in srgb, var(--accent) 20%, white)); color: var(--text); border-radius: calc(var(--radius) + 6px); padding: 30px; border: 1px solid color-mix(in srgb, var(--primary) 14%, transparent); box-shadow: var(--shadow); }}
.testimonial-card footer {{ margin-top: 14px; font-weight: 700; color: var(--text); }}
.site-footer {{ padding: 36px 0 56px; color: var(--muted); }}
.footer-card {{ border-top: 1px solid var(--border); padding-top: 22px; display: flex; gap: 16px; align-items: center; justify-content: space-between; flex-wrap: wrap; }}
@media (max-width: 1080px) { .hero-grid, .content-grid, .product-grid, .testimonial-grid, .contact-grid, .promo-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 780px) { .header-inner { flex-direction: column; align-items: flex-start; } .site-nav { justify-content: flex-start; } .hero-grid, .content-grid, .product-grid, .testimonial-grid, .contact-grid, .promo-grid, .metric-grid { grid-template-columns: 1fr; } .hero-copy, .hero-media { min-height: auto; } .hero-copy { padding: 28px; } .section-card, .promo-banner { padding: 22px; } .container { width: min(100% - 24px, 1200px); } }
""".replace("__THEME_VARS__", _theme_vars(theme)).replace("{{", "{").replace("}}", "}")


def _report_files(page_plan: PagePlan, theme: ThemeConfig) -> Dict[str, str]:
    style_analysis = page_plan.style_dna.style_analysis.model_dump() if page_plan.style_dna else {}
    design_tokens = theme.design_tokens.model_dump()
    ui_structure = page_plan.ui_structure.model_dump() if page_plan.ui_structure else {}
    return {
        "report/01-style-analysis.json": json.dumps(style_analysis, ensure_ascii=False, indent=2),
        "report/02-design-tokens.json": json.dumps(design_tokens, ensure_ascii=False, indent=2),
        "report/03-ui-structure.json": json.dumps(ui_structure, ensure_ascii=False, indent=2),
        "report/04-html-preview.html": _build_static_html(page_plan, theme),
        "report/05-css-preview.css": _build_static_css(theme),
    }

def _build_section_cards(section: SectionPlan) -> str:
    cards: List[str] = []
    for item in section.items:
        cards.append(
            f"""
            <article class="info-card">
              <span class="badge">{item.get('badge', _section_label(section.type))}</span>
              <h3>{item.get('title', '内容卡片')}</h3>
              <p>{item.get('description', '')}</p>
              <div class="meta">{item.get('meta', '')}</div>
            </article>
            """.strip()
        )
    return "\n".join(cards)


def _build_products_html(section: SectionPlan) -> str:
    cards: List[str] = []
    for item in section.items:
        query = item.get("image_query", item.get("title", "product"))
        cards.append(
            f"""
            <article class="product-card">
              <img data-query="{query}" alt="{item.get('title', '产品图片')}" />
              <div class="product-card-body">
                <div class="product-topline">
                  <span class="badge">{item.get('badge', '热门产品')}</span>
                  <span class="meta">{item.get('meta', '')}</span>
                </div>
                <h3>{item.get('title', '产品')}</h3>
                <p>{item.get('description', '')}</p>
                <div class="price-row">
                  <span class="price-tag">{item.get('price', '')}</span>
                  <a href="#contact" class="buy-button">立即购买</a>
                </div>
              </div>
            </article>
            """.strip()
        )
    return "\n".join(cards)


def _build_testimonials_html(section: SectionPlan) -> str:
    cards: List[str] = []
    for item in section.items:
        cards.append(
            f"""
            <blockquote class="testimonial-card">
              <p>“{item.get('quote', '')}”</p>
              <footer>{item.get('author', '')}</footer>
            </blockquote>
            """.strip()
        )
    return "\n".join(cards)


def _build_contact_html(section: SectionPlan) -> str:
    cards: List[str] = []
    for item in section.items:
        cards.append(
            f"""
            <article class="contact-card">
              <span class="badge">{item.get('meta', '联系信息')}</span>
              <h3>{item.get('title', '')}</h3>
              <p>{item.get('description', '')}</p>
            </article>
            """.strip()
        )
    return "\n".join(cards)


def _build_promo_html(section: SectionPlan) -> str:
    cards: List[str] = []
    for item in section.items:
        cards.append(
            f"""
            <article class="promo-card">
              <h3>{item.get('title', '')}</h3>
              <p>{item.get('description', '')}</p>
            </article>
            """.strip()
        )
    return "\n".join(cards)


def _build_static_section(section: SectionPlan) -> str:
    heading = f"""
    <div class="section-head">
      <div>
        <span class="eyebrow">{_section_label(section.type)}</span>
        <h2>{section.title}</h2>
      </div>
      <p>{section.subtitle} {section.body}</p>
    </div>
    """.strip()

    if section.type in {"about", "features"}:
        content = f'<div class="content-grid">{_build_section_cards(section)}</div>'
    elif section.type == "products":
        content = f'<div class="product-grid">{_build_products_html(section)}</div>'
    elif section.type == "testimonials":
        content = f'<div class="testimonial-grid">{_build_testimonials_html(section)}</div>'
    elif section.type == "promo":
        content = f'<div class="promo-banner"><div class="promo-grid">{_build_promo_html(section)}</div></div>'
    elif section.type == "contact":
        content = f'<div class="contact-grid">{_build_contact_html(section)}</div>'
    else:
        content = f'<div class="content-grid">{_build_section_cards(section)}</div>'

    return f'<section id="{section.id}" class="section-shell"><div class="container"><div class="section-card">{heading}{content}</div></div></section>'


def _build_static_html(page_plan: PagePlan, theme: ThemeConfig) -> str:
    hero = next((section for section in page_plan.sections if section.type == "hero"), None)
    hero_metrics = ""
    if hero:
        hero_metrics = "\n".join(
            [f'<div class="metric-card"><span>{item.get("label", "")}</span><strong>{item.get("value", "")}</strong></div>' for item in hero.items]
        )
    other_sections = [section for section in page_plan.sections if section.type not in {"hero", "footer"}]
    section_html = "\n".join(_build_static_section(section) for section in other_sections)
    nav_html = "".join(f'<a href="#{section.id}">{section.title}</a>' for section in other_sections)
    hero_html = ""
    if hero:
        hero_html = f"""
        <section id="hero" class="hero-section">
          <div class="container">
            <div class="hero-grid">
              <div class="hero-copy">
                <div>
                  <span class="eyebrow">品牌首屏</span>
                  <h1>{hero.title}</h1>
                  <p>{hero.subtitle} {hero.body}</p>
                  <div class="action-row">
                    <a href="{hero.cta_href or '#products'}" class="primary-button">{hero.cta_label or '立即查看'}</a>
                    <a href="#promo" class="secondary-button">查看活动</a>
                  </div>
                </div>
                <div class="metric-grid">{hero_metrics}</div>
              </div>
              <div class="hero-media">
                <img data-query="{_hero_query(page_plan)}" alt="品牌主视觉" />
              </div>
            </div>
          </div>
        </section>
        """.strip()

    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{page_plan.page_title}</title>
    <meta name="description" content="{page_plan.seo_description}" />
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="page-shell">
      <header class="site-header">
        <div class="container header-inner">
          <a href="#hero" class="brand-mark"><span class="brand-dot"></span><span>{page_plan.site_name}</span></a>
          <nav class="site-nav">{nav_html}<a href="#contact">联系我们</a></nav>
        </div>
      </header>
      {hero_html}
      {section_html}
      <footer class="site-footer">
        <div class="container footer-card">
          <strong>{page_plan.site_name}</strong>
          <span>{page_plan.footer_note}</span>
        </div>
      </footer>
    </main>
    <script src="./script.js"></script>
  </body>
</html>
"""


def _build_static_css(theme: ThemeConfig) -> str:
    return _build_css(theme)


def _build_static_script() -> str:
    return """const buildImage = (query, width = 1200, height = 800) => {
  const safeQuery = encodeURIComponent((query || 'brand website').trim());
  return `https://source.unsplash.com/featured/${width}x${height}/?${safeQuery}`;
};

document.querySelectorAll('img[data-query]').forEach((img) => {
  const query = img.getAttribute('data-query') || 'brand website';
  const width = img.closest('.product-card') ? 800 : 1400;
  const height = img.closest('.product-card') ? 600 : 900;
  img.src = buildImage(query, width, height);
});

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const href = link.getAttribute('href') || '';
    if (!href || href === '#') return;
    const target = document.getElementById(href.slice(1));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (window.location.hash !== href) {
      history.replaceState(null, '', href);
    }
  });
});
"""

def _build_preview_files(page_plan: PagePlan, theme: ThemeConfig) -> Dict[str, str]:
    sections = [section.model_dump() for section in page_plan.sections]
    preview_payload = {
        "siteName": page_plan.site_name,
        "footerNote": page_plan.footer_note,
        "sections": sections,
        "heroQuery": _hero_query(page_plan),
    }
    return {
        "/App.tsx": f"""import './styles.css';

const siteData = {_json(preview_payload)};
const imageUrl = (query: string, width = 1200, height = 800) => `https://source.unsplash.com/featured/${{width}}x${{height}}/?${{encodeURIComponent(query || 'brand website')}}`;

type Item = Record<string, string>;
type Section = {{ id: string; type: string; title: string; subtitle: string; body: string; cta_label?: string; cta_href?: string; items: Item[] }};

function Header() {{
  const targets = siteData.sections.filter((section: Section) => section.type !== 'hero' && section.type !== 'footer');
  return (
    <header className="site-header">
      <div className="container header-inner">
        <a href="#hero" className="brand-mark"><span className="brand-dot"></span><span>{{siteData.siteName}}</span></a>
        <nav className="site-nav">
          {{targets.map((section: Section) => (
            <a key={{section.id}} href={{`#${{section.id}}`}}>{{section.title}}</a>
          ))}}
          <a href="#contact">联系我们</a>
        </nav>
      </div>
    </header>
  );
}}

function Hero({{ section }}: {{ section: Section }}) {{
  return (
    <section id="hero" className="hero-section">
      <div className="container">
        <div className="hero-grid">
          <div className="hero-copy">
            <div>
              <span className="eyebrow">品牌首屏</span>
              <h1>{{section.title}}</h1>
              <p>{{section.subtitle}} {{section.body}}</p>
              <div className="action-row">
                <a href={{section.cta_href || '#products'}} className="primary-button">{{section.cta_label || '立即查看'}}</a>
                <a href="#promo" className="secondary-button">查看活动</a>
              </div>
            </div>
            <div className="metric-grid">
              {{section.items.map((item) => (
                <div key={{item.label}} className="metric-card">
                  <span>{{item.label}}</span>
                  <strong>{{item.value}}</strong>
                </div>
              ))}}
            </div>
          </div>
          <div className="hero-media">
            <img src={{imageUrl(siteData.heroQuery, 1400, 900)}} alt="品牌主视觉" />
          </div>
        </div>
      </div>
    </section>
  );
}}

function GenericSection({{ section }}: {{ section: Section }}) {{
  let content = null;
  if (section.type === 'products') {{
    content = (
      <div className="product-grid">
        {{section.items.map((item) => (
          <article key={{item.title}} className="product-card">
            <img src={{imageUrl(item.image_query || item.title, 800, 600)}} alt={{item.title}} />
            <div className="product-card-body">
              <div className="product-topline">
                <span className="badge">{{item.badge || '热门产品'}}</span>
                <span className="meta">{{item.meta || ''}}</span>
              </div>
              <h3>{{item.title}}</h3>
              <p>{{item.description}}</p>
              <div className="price-row">
                <span className="price-tag">{{item.price}}</span>
                <a href="#contact" className="buy-button">立即购买</a>
              </div>
            </div>
          </article>
        ))}}
      </div>
    );
  }} else if (section.type === 'testimonials') {{
    content = (
      <div className="testimonial-grid">
        {{section.items.map((item) => (
          <blockquote key={{item.author}} className="testimonial-card">
            <p>“{{item.quote}}”</p>
            <footer>{{item.author}}</footer>
          </blockquote>
        ))}}
      </div>
    );
  }} else if (section.type === 'promo') {{
    content = (
      <div className="promo-banner">
        <div className="promo-grid">
          {{section.items.map((item) => (
            <article key={{item.title}} className="promo-card">
              <h3>{{item.title}}</h3>
              <p>{{item.description}}</p>
            </article>
          ))}}
        </div>
      </div>
    );
  }} else if (section.type === 'contact') {{
    content = (
      <div className="contact-grid">
        {{section.items.map((item) => (
          <article key={{item.title}} className="contact-card">
            <span className="badge">{{item.meta || '联系信息'}}</span>
            <h3>{{item.title}}</h3>
            <p>{{item.description}}</p>
          </article>
        ))}}
      </div>
    );
  }} else {{
    content = (
      <div className="content-grid">
        {{section.items.map((item) => (
          <article key={{item.title}} className="info-card">
            <span className="badge">{{item.badge || '内容模块'}}</span>
            <h3>{{item.title}}</h3>
            <p>{{item.description}}</p>
            <div className="meta">{{item.meta || ''}}</div>
          </article>
        ))}}
      </div>
    );
  }}

  return (
    <section id={{section.id}} className="section-shell">
      <div className="container">
        <div className="section-card">
          <div className="section-head">
            <div>
              <span className="eyebrow">{{section.title}}</span>
              <h2>{{section.title}}</h2>
            </div>
            <p>{{section.subtitle}} {{section.body}}</p>
          </div>
          {{content}}
        </div>
      </div>
    </section>
  );
}}

export default function App() {{
  const hero = siteData.sections.find((section: Section) => section.type === 'hero');
  const rest = siteData.sections.filter((section: Section) => !['hero', 'footer'].includes(section.type));
  return (
    <main className="page-shell">
      <Header />
      {{hero ? <Hero section={{hero}} /> : null}}
      {{rest.map((section: Section) => <GenericSection key={{section.id}} section={{section}} />)}}
      <footer className="site-footer">
        <div className="container footer-card">
          <strong>{{siteData.siteName}}</strong>
          <span>{{siteData.footerNote}}</span>
        </div>
      </footer>
    </main>
  );
}}
""",
        "/styles.css": _build_css(theme),
    }


def _build_site_data(page_plan: PagePlan) -> str:
    payload = {
        "siteName": page_plan.site_name,
        "footerNote": page_plan.footer_note,
        "navigation": page_plan.navigation,
        "heroQuery": _hero_query(page_plan),
        "sections": [section.model_dump() for section in page_plan.sections],
    }
    return f"export const siteData = {_json(payload)} as const;\n"

def _build_next_page() -> str:
    return """import { GeneratedSite } from '@/components/generated-site';

export default function Page() {
  return <GeneratedSite />;
}
"""


def _build_next_layout(page_plan: PagePlan) -> str:
    return f"""import type {{ Metadata }} from 'next';
import './globals.css';

export const metadata: Metadata = {{
  title: {json.dumps(page_plan.page_title, ensure_ascii=False)},
  description: {json.dumps(page_plan.seo_description, ensure_ascii=False)},
}};

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
  return (
    <html lang="zh-CN">
      <body>{{children}}</body>
    </html>
  );
}}
"""


def _build_next_globals(theme: ThemeConfig) -> str:
    return f"""@tailwind base;
@tailwind components;
@tailwind utilities;

{_build_css(theme)}
"""


def _build_header_component() -> str:
    return """import { siteData } from '@/lib/site-data';

export function SiteHeader() {
  const targets = siteData.sections.filter((section) => section.type !== 'hero' && section.type !== 'footer');
  return (
    <header className="site-header">
      <div className="container header-inner">
        <a href="#hero" className="brand-mark"><span className="brand-dot"></span><span>{siteData.siteName}</span></a>
        <nav className="site-nav">
          {targets.map((section) => <a key={section.id} href={`#${section.id}`}>{section.title}</a>)}
          <a href="#contact">联系我们</a>
        </nav>
      </div>
    </header>
  );
}
"""


def _build_footer_component() -> str:
    return """import { siteData } from '@/lib/site-data';

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="container footer-card">
        <strong>{siteData.siteName}</strong>
        <span>{siteData.footerNote}</span>
      </div>
    </footer>
  );
}
"""


def _build_hero_component() -> str:
    return """type HeroItem = { label?: string; value?: string };

type HeroSectionProps = {
  title: string;
  subtitle: string;
  body: string;
  ctaLabel?: string;
  ctaHref?: string;
  heroImage: string;
  items: HeroItem[];
};

export function HeroSection({ title, subtitle, body, ctaLabel, ctaHref, heroImage, items }: HeroSectionProps) {
  return (
    <section id="hero" className="hero-section">
      <div className="container">
        <div className="hero-grid">
          <div className="hero-copy">
            <div>
              <span className="eyebrow">品牌首屏</span>
              <h1>{title}</h1>
              <p>{subtitle} {body}</p>
              <div className="action-row">
                <a href={ctaHref || '#products'} className="primary-button">{ctaLabel || '立即查看'}</a>
                <a href="#promo" className="secondary-button">查看活动</a>
              </div>
            </div>
            <div className="metric-grid">{items.map((item) => <div key={item.label} className="metric-card"><span>{item.label}</span><strong>{item.value}</strong></div>)}</div>
          </div>
          <div className="hero-media"><img src={heroImage} alt="品牌主视觉" /></div>
        </div>
      </div>
    </section>
  );
}
"""


def _build_product_component() -> str:
    return """type ProductItem = { title?: string; description?: string; price?: string; image_query?: string; badge?: string; meta?: string; };
type ProductSectionProps = { id: string; title: string; subtitle: string; body: string; items: ProductItem[]; };
const imageUrl = (query?: string, width = 800, height = 600) => `https://source.unsplash.com/featured/${width}x${height}/?${encodeURIComponent(query || 'product showcase')}`;
export function ProductSection({ id, title, subtitle, body, items }: ProductSectionProps) {
  return (
    <section id={id} className="section-shell"><div className="container"><div className="section-card"><div className="section-head"><div><span className="eyebrow">热门产品</span><h2>{title}</h2></div><p>{subtitle} {body}</p></div><div className="product-grid">{items.map((item) => <article key={item.title} className="product-card"><img src={imageUrl(item.image_query || item.title)} alt={item.title || '产品图片'} /><div className="product-card-body"><div className="product-topline"><span className="badge">{item.badge || '热门产品'}</span><span className="meta">{item.meta || ''}</span></div><h3>{item.title}</h3><p>{item.description}</p><div className="price-row"><span className="price-tag">{item.price}</span><a href="#contact" className="buy-button">立即购买</a></div></div></article>)}</div></div></div></section>
  );
}
"""


def _build_content_component() -> str:
    return """type ContentItem = Record<string, string | undefined>;
type ContentSectionProps = { id: string; type: string; title: string; subtitle: string; body: string; items: ContentItem[]; };
export function ContentSection({ id, type, title, subtitle, body, items }: ContentSectionProps) {
  const renderBody = () => {
    if (type === 'testimonials') return <div className="testimonial-grid">{items.map((item) => <blockquote key={item.author} className="testimonial-card"><p>“{item.quote}”</p><footer>{item.author}</footer></blockquote>)}</div>;
    if (type === 'promo') return <div className="promo-banner"><div className="promo-grid">{items.map((item) => <article key={item.title} className="promo-card"><h3>{item.title}</h3><p>{item.description}</p></article>)}</div></div>;
    if (type === 'contact') return <div className="contact-grid">{items.map((item) => <article key={item.title} className="contact-card"><span className="badge">{item.meta || '联系信息'}</span><h3>{item.title}</h3><p>{item.description}</p></article>)}</div>;
    return <div className="content-grid">{items.map((item) => <article key={item.title} className="info-card"><span className="badge">{item.badge || '内容模块'}</span><h3>{item.title}</h3><p>{item.description}</p><div className="meta">{item.meta || ''}</div></article>)}</div>;
  };
  return <section id={id} className="section-shell"><div className="container"><div className="section-card"><div className="section-head"><div><span className="eyebrow">{title}</span><h2>{title}</h2></div><p>{subtitle} {body}</p></div>{renderBody()}</div></div></section>;
}
"""


def _build_generated_site() -> str:
    return """import { ContentSection } from '@/components/content-section';
import { HeroSection } from '@/components/hero-section';
import { ProductSection } from '@/components/product-section';
import { SiteFooter } from '@/components/site-footer';
import { SiteHeader } from '@/components/site-header';
import { siteData } from '@/lib/site-data';
const heroImage = `https://source.unsplash.com/featured/1400x900/?${encodeURIComponent(siteData.heroQuery || 'brand website')}`;
export function GeneratedSite() {
  const hero = siteData.sections.find((section) => section.type === 'hero');
  const rest = siteData.sections.filter((section) => !['hero', 'footer'].includes(section.type));
  return <main className="page-shell"><SiteHeader />{hero ? <HeroSection title={hero.title} subtitle={hero.subtitle} body={hero.body} ctaLabel={hero.cta_label} ctaHref={hero.cta_href} heroImage={heroImage} items={hero.items} /> : null}{rest.map((section) => section.type === 'products' ? <ProductSection key={section.id} id={section.id} title={section.title} subtitle={section.subtitle} body={section.body} items={section.items} /> : <ContentSection key={section.id} id={section.id} type={section.type} title={section.title} subtitle={section.subtitle} body={section.body} items={section.items} />)}<SiteFooter /></main>;
}
"""


def generate_bundle(page_plan: PagePlan, theme: ThemeConfig) -> GeneratedBundle:
    project_files: Dict[str, str] = {}
    project_files.update(_report_files(page_plan, theme))
    project_files["app/page.tsx"] = _build_next_page()
    project_files["app/layout.tsx"] = _build_next_layout(page_plan)
    project_files["app/globals.css"] = _build_next_globals(theme)
    project_files["components/site-header.tsx"] = _build_header_component()
    project_files["components/site-footer.tsx"] = _build_footer_component()
    project_files["components/hero-section.tsx"] = _build_hero_component()
    project_files["components/product-section.tsx"] = _build_product_component()
    project_files["components/content-section.tsx"] = _build_content_component()
    project_files["components/generated-site.tsx"] = _build_generated_site()
    project_files["lib/site-data.ts"] = _build_site_data(page_plan)
    project_files["next-env.d.ts"] = '/// <reference types="next" />\n/// <reference types="next/image-types/global" />\n'
    project_files["tailwind.config.ts"] = "import type { Config } from 'tailwindcss';\nconst config: Config = { content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'], theme: { extend: {} }, plugins: [] };\nexport default config;\n"
    project_files["postcss.config.js"] = "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };\n"
    project_files["tsconfig.json"] = "{\n  \"compilerOptions\": {\n    \"target\": \"ES2017\",\n    \"lib\": [\"dom\", \"dom.iterable\", \"esnext\"],\n    \"allowJs\": true,\n    \"skipLibCheck\": true,\n    \"strict\": true,\n    \"noEmit\": true,\n    \"esModuleInterop\": true,\n    \"module\": \"esnext\",\n    \"moduleResolution\": \"bundler\",\n    \"resolveJsonModule\": true,\n    \"isolatedModules\": true,\n    \"jsx\": \"preserve\",\n    \"incremental\": true,\n    \"baseUrl\": \".\",\n    \"paths\": { \"@/*\": [\"./*\"] }\n  },\n  \"include\": [\"next-env.d.ts\", \"**/*.ts\", \"**/*.tsx\"],\n  \"exclude\": [\"node_modules\"]\n}\n"
    project_files["next.config.mjs"] = "/** @type {import('next').NextConfig} */\nconst nextConfig = {};\nexport default nextConfig;\n"
    project_files["package.json"] = "{\n  \"name\": \"designgen-export\",\n  \"private\": true,\n  \"version\": \"0.1.0\",\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\", \"start\": \"next start\" },\n  \"dependencies\": { \"next\": \"14.2.25\", \"react\": \"18.3.1\", \"react-dom\": \"18.3.1\" },\n  \"devDependencies\": { \"autoprefixer\": \"10.4.20\", \"postcss\": \"8.5.1\", \"tailwindcss\": \"3.4.17\", \"typescript\": \"5.7.3\" }\n}\n"
    project_files["static/index.html"] = _build_static_html(page_plan, theme)
    project_files["static/styles.css"] = _build_static_css(theme)
    project_files["static/script.js"] = _build_static_script()
    project_files["README.md"] = f"# {page_plan.site_name}\n\n由 DesignGen 自动生成。\n\n## 运行方式\n\n```bash\nnpm install\nnpm run dev\n```\n\n## 页面说明\n\n- 中文品牌官网结构\n- 产品图片与内容按行业自动匹配\n- 包含品牌故事、产品展示、特色推荐、用户评价、优惠活动和联系入口\n"
    preview_files = _build_preview_files(page_plan, theme)
    return GeneratedBundle(project_files=project_files, preview_files=preview_files)


def validate_bundle(bundle: GeneratedBundle) -> GeneratedBundle:
    required_project_files = {
        "report/01-style-analysis.json", "report/02-design-tokens.json", "report/03-ui-structure.json", "report/04-html-preview.html", "report/05-css-preview.css",
        "app/page.tsx", "app/layout.tsx", "app/globals.css", "components/generated-site.tsx", "components/product-section.tsx", "lib/site-data.ts", "package.json", "static/index.html", "static/script.js",
    }
    required_preview_files = {"/App.tsx", "/styles.css"}
    missing_project = required_project_files - bundle.project_files.keys()
    missing_preview = required_preview_files - bundle.preview_files.keys()
    if missing_project or missing_preview:
        raise ValueError(f"Bundle missing files: {sorted(missing_project | missing_preview)}")
    return bundle
