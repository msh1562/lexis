"use client";

import { useState } from "react";

export default function QuoteButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(`> ${text}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="px-3 py-1 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 self-start"
    >
      {copied ? "복사됨" : "인용"}
    </button>
  );
}