"use client";

export function PromptChips({ prompts, onSelect }: { prompts: string[]; onSelect: (prompt: string) => void }) {
  return (
    <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
      {prompts.map((prompt) => (
        <button
          key={prompt}
          type="button"
          onClick={() => onSelect(prompt)}
          className="rounded-full border border-white/10 bg-white/[0.05] px-4 py-2 text-sm text-white/66 transition hover:border-white/20 hover:bg-white/[0.1] hover:text-white"
        >
          {prompt}
        </button>
      ))}
    </div>
  );
}
