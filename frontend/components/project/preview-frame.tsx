"use client";

import { useMemo } from "react";

const SCRIPT_BLOCK_RE = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;

const INLINE_SCRIPT_REPLACEMENTS: Array<readonly [RegExp, string]> = [
  [/\bwindow\.(?:top|parent)\??\.document\b/g, "document"],
  [/\b(?:top|parent)\??\.document\b/g, "document"],
  [/\bwindow\.(?:top|parent)\??\.location\b/g, "window.location"],
  [/\b(?:top|parent)\??\.location\b/g, "window.location"],
  [/\bwindow\.(?:top|parent)\??\.(scroll(?:To|By)?)\b/g, "window.$1"],
  [/\b(?:top|parent)\??\.(scroll(?:To|By)?)\b/g, "window.$1"],
];

const PREVIEW_GUARD_STYLE = `
html {
  height: auto !important;
  min-height: 100% !important;
  max-height: none !important;
  overflow: auto !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  overscroll-behavior-y: contain;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  height: auto !important;
  min-height: 100% !important;
  max-height: none !important;
  overflow: auto !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  overscroll-behavior-y: contain;
  -webkit-overflow-scrolling: touch;
}

body > main:first-child,
body > #root:first-child,
body > #app:first-child,
body > #__next:first-child,
#root,
#app,
#__next {
  height: auto !important;
  min-height: 100% !important;
  max-height: none !important;
  overflow: visible !important;
}

[data-preview-scroll-root] {
  height: auto !important;
  max-height: none !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  overscroll-behavior-y: contain;
  -webkit-overflow-scrolling: touch;
}

[id] {
  scroll-margin-top: 96px;
}
`;

const PREVIEW_GUARD_SCRIPT = `
(function () {
  var safeProtocols = /^(https?:|mailto:|tel:|\\/\\/)/i;
  var unsafeProtocols = /^\\s*javascript:/i;
  var rawOpen = typeof window.open === 'function' ? window.open.bind(window) : null;
  var preferredScrollRoot = null;

  function preventNavigation(event) {
    if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
    }
  }

  function stopEvent(event) {
    preventNavigation(event);
    if (event && typeof event.stopPropagation === 'function') {
      event.stopPropagation();
    }
    if (event && typeof event.stopImmediatePropagation === 'function') {
      event.stopImmediatePropagation();
    }
  }

  function findAnchor(target) {
    return target && typeof target.closest === 'function' ? target.closest('a[href]') : null;
  }

  function escapeAttribute(value) {
    return value.replace(/["\\\\]/g, '\\\\$&');
  }

  function getHashTarget(hash) {
    var rawId = (hash || '').replace(/^#/, '');
    if (!rawId) {
      return document.body || document.documentElement;
    }

    var decodedId = rawId;
    try {
      decodedId = decodeURIComponent(rawId);
    } catch (error) {}

    return (
      document.getElementById(decodedId) ||
      document.querySelector('[name="' + escapeAttribute(decodedId) + '"]')
    );
  }

  function normalizeAnchorTargets() {
    var anchors = document.querySelectorAll('a[href]');
    for (var index = 0; index < anchors.length; index += 1) {
      var anchor = anchors[index];
      var target = (anchor.getAttribute('target') || '').toLowerCase();

      if (target === '_top' || target === '_parent') {
        anchor.setAttribute('target', '_self');
      }

      if (target === '_blank') {
        var rel = anchor.getAttribute('rel') || '';
        if (!/\\bnoopener\\b/i.test(rel)) {
          rel = (rel + ' noopener noreferrer').trim();
        }
        anchor.setAttribute('rel', rel);
      }
    }
  }

  function openSafeWindow(url) {
    if (!rawOpen || typeof url !== 'string') {
      return null;
    }

    var nextUrl = url.trim();
    if (!nextUrl || unsafeProtocols.test(nextUrl) || !safeProtocols.test(nextUrl)) {
      return null;
    }

    return rawOpen(nextUrl, '_blank', 'noopener,noreferrer');
  }

  function isEditableElement(target) {
    if (!target || !(target instanceof Element)) {
      return false;
    }

    var tagName = target.tagName;
    return (
      tagName === 'INPUT' ||
      tagName === 'TEXTAREA' ||
      tagName === 'SELECT' ||
      target.isContentEditable
    );
  }

  function getScrollElement(element) {
    if (!element) {
      return null;
    }

    if (element === document.body || element === document.documentElement) {
      return document.scrollingElement || document.documentElement;
    }

    return element;
  }

  function getScrollableOverflow(element) {
    if (!element || !(element instanceof Element)) {
      return '';
    }

    var computedStyle = window.getComputedStyle(element);
    return computedStyle.overflowY || computedStyle.overflow || '';
  }

  function isScrollableElement(element) {
    var scrollElement = getScrollElement(element);
    if (!scrollElement) {
      return false;
    }

    if (scrollElement === document.scrollingElement) {
      return scrollElement.scrollHeight - window.innerHeight > 1;
    }

    if (!(scrollElement instanceof HTMLElement)) {
      return false;
    }

    return (
      scrollElement.scrollHeight - scrollElement.clientHeight > 1 &&
      /(auto|scroll|overlay)/i.test(getScrollableOverflow(scrollElement))
    );
  }

  function canScrollInDirection(element, deltaY) {
    var scrollElement = getScrollElement(element);
    if (!scrollElement) {
      return false;
    }

    var maxScrollTop = Math.max(0, scrollElement.scrollHeight - scrollElement.clientHeight);
    if (maxScrollTop <= 0) {
      return false;
    }

    if (deltaY < 0) {
      return scrollElement.scrollTop > 0;
    }

    if (deltaY > 0) {
      return scrollElement.scrollTop < maxScrollTop;
    }

    return true;
  }

  function findScrollableAncestor(target, deltaY) {
    var current = target instanceof Element ? target : null;

    while (current) {
      if (isScrollableElement(current) && canScrollInDirection(current, deltaY)) {
        return getScrollElement(current);
      }

      current = current.parentElement;
    }

    return null;
  }

  function findPreferredScrollRoot() {
    var documentScroller = document.scrollingElement || document.documentElement;
    var candidates = [documentScroller];
    var elements = document.querySelectorAll('main, section, article, div');

    for (var index = 0; index < elements.length; index += 1) {
      var element = elements[index];
      if (!(element instanceof HTMLElement)) {
        continue;
      }

      if (element.clientHeight < Math.max(240, window.innerHeight * 0.35)) {
        continue;
      }

      if (element.scrollHeight - element.clientHeight <= 24) {
        continue;
      }

      candidates.push(element);
    }

    var bestCandidate = documentScroller;
    var bestScore = documentScroller ? documentScroller.scrollHeight - documentScroller.clientHeight : -1;

    for (var candidateIndex = 0; candidateIndex < candidates.length; candidateIndex += 1) {
      var candidate = getScrollElement(candidates[candidateIndex]);
      if (!candidate) {
        continue;
      }

      var scrollRange = candidate.scrollHeight - candidate.clientHeight;
      if (scrollRange <= 24) {
        continue;
      }

      var sizeBonus = Math.min(candidate.clientHeight, window.innerHeight);
      var score = scrollRange * 4 + sizeBonus;
      if (score > bestScore) {
        bestCandidate = candidate;
        bestScore = score;
      }
    }

    return bestCandidate || documentScroller;
  }

  function normalizeScrollRoot() {
    preferredScrollRoot = findPreferredScrollRoot();

    if (!preferredScrollRoot || preferredScrollRoot === document.body || preferredScrollRoot === document.documentElement) {
      return;
    }

    if (preferredScrollRoot instanceof HTMLElement) {
      preferredScrollRoot.setAttribute('data-preview-scroll-root', 'true');
      preferredScrollRoot.style.height = 'auto';
      preferredScrollRoot.style.maxHeight = 'none';
      preferredScrollRoot.style.overflowX = 'hidden';
      preferredScrollRoot.style.overflowY = 'auto';
    }
  }

  function scrollInsideFrame(event) {
    if (!event || event.defaultPrevented || event.ctrlKey || event.deltaY === 0) {
      return;
    }

    if (isEditableElement(event.target)) {
      return;
    }

    var scrollRoot =
      findScrollableAncestor(event.target, event.deltaY) ||
      preferredScrollRoot ||
      findPreferredScrollRoot();

    var scrollElement = getScrollElement(scrollRoot);
    if (!scrollElement) {
      return;
    }

    var maxScrollTop = Math.max(0, scrollElement.scrollHeight - scrollElement.clientHeight);
    if (maxScrollTop <= 0) {
      return;
    }

    var nextScrollTop = Math.max(0, Math.min(scrollElement.scrollTop + event.deltaY, maxScrollTop));
    if (nextScrollTop === scrollElement.scrollTop && !canScrollInDirection(scrollElement, event.deltaY)) {
      preventNavigation(event);
      return;
    }

    scrollElement.scrollTop = nextScrollTop;
    preventNavigation(event);
  }

  document.addEventListener('click', function (event) {
    var anchor = findAnchor(event.target);
    if (!anchor) {
      return;
    }

    var href = (anchor.getAttribute('href') || '').trim();
    if (!href) {
      return;
    }

    if (unsafeProtocols.test(href)) {
      stopEvent(event);
      return;
    }

    if (href.charAt(0) === '#') {
      var target = getHashTarget(href);
      preventNavigation(event);

      if (!target) {
        return;
      }

      try {
        if (href !== '#') {
          window.history.replaceState(null, '', href);
        }
      } catch (error) {}

      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

    var targetAttr = (anchor.getAttribute('target') || '').toLowerCase();
    var isSafeAbsoluteUrl = safeProtocols.test(href);
    var shouldOpenSafely = targetAttr === '_blank' || isSafeAbsoluteUrl;
    var shouldBlockInFrame =
      targetAttr === '_top' ||
      targetAttr === '_parent' ||
      !isSafeAbsoluteUrl;

    if (!shouldBlockInFrame && !shouldOpenSafely) {
      return;
    }

    stopEvent(event);

    if (shouldOpenSafely) {
      openSafeWindow(href);
    }
  }, true);

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form || form.tagName !== 'FORM') {
      return;
    }

    preventNavigation(event);
  }, true);

  window.open = function (url, target, features) {
    if (typeof url !== 'string') {
      return null;
    }

    var nextUrl = url.trim();
    if (!rawOpen || !nextUrl || unsafeProtocols.test(nextUrl) || !safeProtocols.test(nextUrl)) {
      return null;
    }

    return rawOpen(nextUrl, target || '_blank', features || 'noopener,noreferrer');
  };

  window.addEventListener('error', function (event) {
    var message = event && typeof event.message === 'string' ? event.message : '';
    if (message.includes('Blocked a frame with origin') || message.includes('SecurityError')) {
      stopEvent(event);
      return true;
    }
    return undefined;
  }, true);

  window.addEventListener('unhandledrejection', function (event) {
    var reason = event && event.reason ? String(event.reason) : '';
    if (reason.includes('Blocked a frame with origin') || reason.includes('SecurityError')) {
      stopEvent(event);
    }
  });

  window.addEventListener('load', normalizeScrollRoot, { once: true });
  window.addEventListener('resize', normalizeScrollRoot);
  document.addEventListener('wheel', scrollInsideFrame, { passive: false, capture: true });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      normalizeAnchorTargets();
      normalizeScrollRoot();
    }, { once: true });
  } else {
    normalizeAnchorTargets();
    normalizeScrollRoot();
  }
})();
`;

function insertIntoHead(html: string, snippet: string) {
  if (/<\/head>/i.test(html)) {
    return html.replace(/<\/head>/i, `${snippet}</head>`);
  }

  return `${snippet}${html}`;
}

function sanitizeInlineScripts(previewHtml: string) {
  return previewHtml.replace(SCRIPT_BLOCK_RE, (match, attributes, scriptContent) => {
    const safeScriptContent = INLINE_SCRIPT_REPLACEMENTS.reduce(
      (nextScriptContent, [pattern, replacement]) => nextScriptContent.replace(pattern, replacement),
      scriptContent
    );

    return `<script${attributes}>${safeScriptContent}</script>`;
  });
}

function injectPreviewGuard(previewHtml: string) {
  const styleTag = `<style data-preview-guard="styles">${PREVIEW_GUARD_STYLE}</style>`;
  const scriptTag = `<script data-preview-guard="script">${PREVIEW_GUARD_SCRIPT}</script>`;
  const baseTag = '<base data-preview-guard="base" target="_self" />';
  const safePreviewHtml = sanitizeInlineScripts(previewHtml);

  return insertIntoHead(safePreviewHtml, `${baseTag}${styleTag}${scriptTag}`);
}

export function PreviewFrame({ previewHtml }: { previewHtml: string }) {
  const safePreviewHtml = useMemo(() => injectPreviewGuard(previewHtml), [previewHtml]);

  return (
    <div className="h-full min-h-0 overflow-hidden rounded-[30px] border border-white/12 bg-white shadow-[0_28px_80px_rgba(6,10,26,0.4)]">
      <iframe
        title="DesignGen 页面预览"
        srcDoc={safePreviewHtml}
        className="block h-full min-h-0 w-full border-0"
        sandbox="allow-scripts allow-forms allow-modals allow-popups"
        referrerPolicy="no-referrer"
        scrolling="yes"
      />
    </div>
  );
}
