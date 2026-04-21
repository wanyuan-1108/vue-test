"use client";

import dynamic from "next/dynamic";


const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });


export function CodeEditor({ fileName, code }: { fileName: string; code: string }) {
  const language = fileName.endsWith(".css") ? "css" : fileName.endsWith(".js") ? "javascript" : "html";

  return (
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
      }}
    />
  );
}
