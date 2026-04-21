"use client";

import dynamic from "next/dynamic";
import type { ReactNode } from "react";
import { Component } from "react";


const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => <CodeFallback code="正在加载代码编辑器..." />,
});


function CodeFallback({ code }: { code: string }) {
  return (
    <pre className="h-full overflow-auto bg-slate-950 p-5 font-mono text-[13px] leading-6 text-slate-200">
      <code>{code}</code>
    </pre>
  );
}


class CodeErrorBoundary extends Component<{ children: ReactNode; code: string }, { hasError: boolean }> {
  constructor(props: { children: ReactNode; code: string }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch() {}

  render() {
    if (this.state.hasError) {
      return <CodeFallback code={this.props.code} />;
    }

    return this.props.children;
  }
}


export function CodeViewer({ fileName, code }: { fileName: string; code: string }) {
  const language = fileName.endsWith(".css") ? "css" : fileName.endsWith(".js") ? "javascript" : "html";

  return (
    <CodeErrorBoundary code={code}>
      <MonacoEditor
        height="100%"
        defaultLanguage={language}
        language={language}
        theme="vs-dark"
        value={code}
        options={{
          readOnly: true,
          minimap: { enabled: false },
          fontSize: 14,
          scrollBeyondLastLine: false,
          wordWrap: "on",
          lineNumbersMinChars: 3,
          automaticLayout: true,
        }}
      />
    </CodeErrorBoundary>
  );
}
