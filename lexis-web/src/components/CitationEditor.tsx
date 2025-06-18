"use client";

import { useState, useEffect } from "react";

interface Block {
  id: number;
  title: string;
}

export interface CitationInfo {
  id: number;
  title: string;
  reason: string;
}

interface Props {
  citations: CitationInfo[];
  onChange: (cits: CitationInfo[]) => void;
}

export default function CitationEditor({ citations, onChange }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Block[]>([]);
  const [selected, setSelected] = useState<Block | null>(null);
  const [reason, setReason] = useState("");

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }
    const t = setTimeout(async () => {
      const res = await fetch(`/api/block/search?q=${encodeURIComponent(query)}`);
      if (res.ok) {
        setResults(await res.json());
      }
    }, 300);
    return () => clearTimeout(t);
  }, [query]);

  const addCitation = () => {
    if (!selected) return;
    onChange([...citations, { id: selected.id, title: selected.title, reason }]);
    setQuery("");
    setResults([]);
    setSelected(null);
    setReason("");
  };

  const removeCitation = (id: number) => {
    onChange(citations.filter((c) => c.id !== id));
  };

  return (
    <div className="space-y-2 mt-4">
      <h3 className="font-semibold">인용 추가</h3>
      <input
        className="w-full border p-2 rounded-md"
        placeholder="블록 검색"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {results.length > 0 && (
        <ul className="border rounded-md max-h-40 overflow-y-auto divide-y">
          {results.map((b) => (
            <li key={b.id}>
              <button
                type="button"
                onClick={() => {
                  setSelected(b);
                  setQuery(b.title);
                  setResults([]);
                }}
                className="block w-full text-left p-2 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {b.title}
              </button>
            </li>
          ))}
        </ul>
      )}
      {selected && (
        <div className="space-y-2">
          <input
            className="w-full border p-2 rounded-md"
            placeholder="이유 입력"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
          <button
            type="button"
            onClick={addCitation}
            className="px-3 py-1 bg-blue-600 text-white rounded-md"
          >
            추가
          </button>
        </div>
      )}
      {citations.length > 0 && (
        <ul className="space-y-1">
          {citations.map((c) => (
            <li
              key={c.id}
              className="flex justify-between items-center border rounded-md p-2"
            >
              <span className="text-sm">
                {c.title}
                {c.reason && ` - ${c.reason}`}
              </span>
              <button
                type="button"
                onClick={() => removeCitation(c.id)}
                className="text-red-500 text-xs"
              >
                삭제
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}