from __future__ import annotations

import re
from textwrap import dedent

from app.schemas.design import GeneratedBundle, GeneratedWebsite
from app.services.ai_client import AIClient


_HTML_TAG_RE = re.compile(r"<html[\s>]", re.IGNORECASE)
_HEAD_TAG_RE = re.compile(r"<head[\s>]", re.IGNORECASE)
_BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)
_HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
_TITLE_RE = re.compile(r"<title>.*?</title>", re.IGNORECASE | re.DOTALL)
_STYLESHEET_RE = re.compile(r"<link[^>]+href=[\"']styles\.css[\"'][^>]*>", re.IGNORECASE)
_SCRIPT_RE = re.compile(r"<script[^>]+src=[\"']script\.js[\"'][^>]*></script>", re.IGNORECASE)


class AIWebsiteGenerator:
    def __init__(self, ai_client: AIClient) -> None:
        self.ai_client = ai_client

    def generate(self, prompt: str) -> GeneratedWebsite:
        system_prompt = dedent(
            """
            你是一名资深网页前端设计师和工程师。
            你的任务是根据用户需求，直接生成可运行的完整静态网页代码。

            必须遵守：
            1. 直接输出 JSON，并严格符合给定 Schema。
            2. 生成三个字段：html、css、javascript。
            3. html 必须是完整的 index.html 文档，包含 <!doctype html>、<html>、<head>、<body>。
            4. html 必须引用 ./styles.css 和 ./script.js，不要内联大段 CSS/JS。
            5. 不要依赖 React、Vue、Tailwind、Bootstrap、npm 包或构建工具。
            6. 不要引用外部 CDN、外链图片、在线字体或第三方脚本。
            7. 页面必须响应式，具备完整布局、层次、配色、内容文案与基础交互。
            8. 可以使用纯 CSS、渐变、SVG、emoji、data URI 或占位内容来实现视觉效果。
            9. javascript 只能使用浏览器原生 API。
            10. 代码应清晰、现代、美观，并尽量贴合用户描述的品牌调性和功能诉求。
            11. 页面中的导航、标题、按钮、正文、介绍文案等默认全部使用简体中文输出；除非用户明确要求其他语言，否则不要输出英文页面文案。
            12. 导航栏点击后必须只在当前文档内部平滑定位到对应 section，不要跳转到外部页面，不要跨 iframe，不要跨窗口。
            13. 导航实现推荐使用 href="#section-id" 配合对应 section 的 id，并结合 html { scroll-behavior: smooth; }；也可以在当前 document 中使用 scrollIntoView。
            14. 如果使用 JavaScript 处理导航，只能操作当前 document，严禁使用 window.parent.document、parent.document、window.top.document、top.document。
            15. 如果导航栏是固定定位或 sticky，请处理锚点偏移，例如使用 scroll-margin-top 或等效方案，避免标题被导航遮挡。
            """
        ).strip()
        user_prompt = dedent(
            f"""
            用户需求：
            {prompt}

            请返回：
            - title：页面标题
            - summary：一句话概述你的页面方案
            - html：完整 HTML
            - css：完整 CSS
            - javascript：完整 JavaScript

            补充要求：
            - 默认生成中文网站内容
            - 页面文案请使用自然、简洁、产品化的简体中文
            - 页面导航必须支持在当前页面内部平滑滚动到对应 section
            - 不要生成任何跨 iframe、跨窗口、跨 document 访问代码
            """
        ).strip()
        website = self.ai_client.structured_json(system_prompt=system_prompt, user_prompt=user_prompt, schema=GeneratedWebsite)
        if website is None:
            raise ValueError("AI 未返回网页代码")
        return GeneratedWebsite(
            title=website.title.strip() or "AI 生成网站",
            summary=website.summary.strip(),
            html=self._normalize_html(website.html, website.title.strip() or "AI 生成网站"),
            css=website.css.strip(),
            javascript=website.javascript.strip(),
        )

    def to_bundle(self, website: GeneratedWebsite) -> GeneratedBundle:
        project_files = {
            "index.html": website.html,
            "styles.css": website.css,
            "script.js": website.javascript,
        }
        preview_files = {
            "/index.html": self._build_preview_html(website),
        }
        return GeneratedBundle(
            project_files=project_files,
            preview_files=preview_files,
            entry_file="index.html",
            preview_entry="/index.html",
        )

    def _normalize_html(self, html: str, title: str) -> str:
        document = html.strip()
        if not document:
            raise ValueError("AI 返回的 HTML 为空")

        if not _HTML_TAG_RE.search(document):
            document = dedent(
                f"""
                <!doctype html>
                <html lang="zh-CN">
                  <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>{title}</title>
                    <link rel="stylesheet" href="styles.css" />
                  </head>
                  <body>
                    {document}
                    <script src="script.js"></script>
                  </body>
                </html>
                """
            ).strip()
            return document

        if not _HEAD_TAG_RE.search(document):
            document = re.sub(
                r"<html([^>]*)>",
                rf"<html\1><head><meta charset=\"UTF-8\" /><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" /><title>{title}</title><link rel=\"stylesheet\" href=\"styles.css\" /></head>",
                document,
                count=1,
                flags=re.IGNORECASE,
            )

        if not _TITLE_RE.search(document):
            document = _HEAD_CLOSE_RE.sub(f"  <title>{title}</title>\n</head>", document, count=1)

        if not _STYLESHEET_RE.search(document):
            document = _HEAD_CLOSE_RE.sub('  <link rel="stylesheet" href="styles.css" />\n</head>', document, count=1)

        if not _SCRIPT_RE.search(document):
            if _BODY_CLOSE_RE.search(document):
                document = _BODY_CLOSE_RE.sub('  <script src="script.js"></script>\n</body>', document, count=1)
            else:
                document = f"{document}\n<script src=\"script.js\"></script>"

        if "<!doctype" not in document.lower():
            document = f"<!doctype html>\n{document}"

        return document

    def _build_preview_html(self, website: GeneratedWebsite) -> str:
        preview = website.html
        preview = _STYLESHEET_RE.sub("", preview)
        preview = _SCRIPT_RE.sub("", preview)

        style_tag = f"<style>\n{website.css}\n</style>" if website.css else ""
        script_tag = f"<script>\n{website.javascript}\n</script>" if website.javascript else ""

        if _HEAD_CLOSE_RE.search(preview):
            preview = _HEAD_CLOSE_RE.sub(f"{style_tag}\n</head>", preview, count=1)
        else:
            preview = f"{style_tag}\n{preview}"

        if _BODY_CLOSE_RE.search(preview):
            preview = _BODY_CLOSE_RE.sub(f"{script_tag}\n</body>", preview, count=1)
        else:
            preview = f"{preview}\n{script_tag}"

        return preview
