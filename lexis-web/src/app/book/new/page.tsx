"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

interface Block {
  id: number;
  title: string;
  content: string;
  topic: string;
  trust_score: number;
  created_at: string;
}

export default function NewBookPage() {
  const { user, token } = useAuth();
  const router = useRouter();
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/block`)
      .then((res) => res.json())
      .then(setBlocks);
  }, []);

  if (!user) {
    return <p className="text-center mt-4">로그인 후 이용 가능합니다.</p>;
  }

  const toggle = (id: number) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id]
    );
  };

  const handleCreate = async () => {
    if (!title || selected.length === 0) return;
    setSaving(true);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/block`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, description, block_ids: selected }),
    });
    if (res.ok) {
      const data = await res.json();
      router.push(`/book/${data.slug}`);
    } else {
      alert("생성 실패");
    }
    setSaving(false);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <input
        className="w-full p-2 border rounded-md"
        placeholder="제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="w-full p-2 border rounded-md min-h-[100px]"
        placeholder="설명"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <div className="space-y-2">
        {blocks.map((b) => (
          <label key={b.id} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={selected.includes(b.id)}
              onChange={() => toggle(b.id)}
            />
            <span>{b.title}</span>
          </label>
        ))}
      </div>
      <button
        onClick={handleCreate}
        disabled={saving || !title || selected.length === 0}
        className="px-4 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50"
      >
        {saving ? "생성 중..." : "LexisBook 생성"}
      </button>
    </div>
  );
}