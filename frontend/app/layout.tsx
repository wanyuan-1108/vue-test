import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "DesignGen · AI 网页生成器",
  description: "DesignGen 是一个 AI 网页生成平台，帮助你快速生成、预览并下载网站源码。",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
