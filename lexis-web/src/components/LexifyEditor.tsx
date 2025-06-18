"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import AuthGuard from "@/components/AuthGuard";
import { useAuth } from "@/context/AuthContext";
import CitationEditor, { CitationInfo } from "@/components/CitationEditor";

const TOPICS = ["정치", "경제", "사회", "기술", "스포츠", "기타"];

export default function LexifyEditor() {
  const { token } = useAuth();
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [topic, setTopic] = useState(TOPICS[0]);
  const [citations, setCitations] = useState<CitationInfo[]>([]);
  const params = useSearchParams();

  useEffect(() => {
    const id = params.get("to_block_id") || params.get("cite");
    if (id) {
      fetch(`/api/block/${id}`)
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          if (data) {
            setText(`> ${data.content}\n\n`);
            setCitations([{ id: data.id, title: data.title, reason: "" }]);
          }
        });
    }
  }, [params]);

  const handleSummarize = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const res = await fetch("/api/lexify/summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (res.ok) {
        const data = await res.json();
        setSummary(data.summary);
      } else {
        setSummary("요약 중 오류가 발생했습니다.");
      }
    } catch {
      setSummary("요약 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <AuthGuard>
      <div className="w-full max-w-2xl flex flex-col gap-4">
      <select
        className="border p-2 rounded-md"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      >
        {TOPICS.map((t) => (
          <option key={t} value={t}>
            {t}
          </option>
        ))}
      </select>
      <textarea
        className="w-full min-h-[200px] p-4 border rounded-md focus:outline-none focus:ring"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="마크다운을 입력하세요..."
      />
      <button
        className="self-end px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        onClick={handleSummarize}
        disabled={loading}
      >
        {loading ? "요약 중..." : "요약 추천"}
      </button>
      {summary && (
        <div className="mt-4 p-4 border rounded-md bg-gray-50 dark:bg-gray-900 whitespace-pre-wrap">
          {summary}
        </div>
      )}
      <CitationEditor citations={citations} onChange={setCitations} />
      {summary && (
        <button
          className="self-end px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
          onClick={async () => {
            if (!text) return;
            setSaving(true);
            const firstLine = text.split("\n")[0];
            try {
              const res = await fetch("/api/block", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                  title: firstLine,
                  content: text,
                  topic,
                  trust_score: 0.9,
                  citation_ids: citations.map((c) => c.id),
                }),
              });
              if (res.ok) {
                const newBlock = await res.json();
                for (const c of citations) {
                  await fetch("/api/citation", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                      from_block_id: newBlock.id,
                      to_block_id: c.id,
                      type: "quote",
                      reason: c.reason || null,
                    }),
                  });
                }
                alert("저장 완료");
              }
            } finally {
              setSaving(false);
            }
          }}
          disabled={saving}
        >
          {saving ? "저장 중..." : "블록 저장"}
        </button>
      )}
      </div>
    </AuthGuard>
  );
}