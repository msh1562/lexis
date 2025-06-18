"use client";

import { useEffect, useState } from "react";
import AuthGuard from "@/components/AuthGuard";
import { useAuth } from "@/context/AuthContext";
import BlockCard from "@/components/BlockCard";

interface Block {
  id: number;
  title: string;
  content: string;
  topic: string | null;
  source_url: string | null;
  trust_score: number;
  created_at: string;
}

interface History {
  id: number;
  user_id: number;
  block_id: number;
  action: string;
  created_at: string;
}

export default function FeedPage() {
  const { user } = useAuth();
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const load = async () => {
      setLoading(true);
      try {
        const hRes = await fetch(`/api/history?user_id=${user.id}`);
        if (!hRes.ok) return;
        const history: History[] = await hRes.json();
        if (history.length === 0) return;
        const latest = history[0];

        const blockRes = await fetch(`/api/block/${latest.block_id}`);
        if (!blockRes.ok) return;
        const focus: Block = await blockRes.json();

        const [topicRes, graphRes] = await Promise.all([
          focus.topic
            ? fetch(`/api/block?topic=${encodeURIComponent(focus.topic)}`)
            : Promise.resolve({ ok: false }),
          fetch(`/api/citation/graph/${latest.block_id}`),
        ]);

        const topicBlocks: Block[] = topicRes.ok ? await topicRes.json() : [];
        let citationBlocks: Block[] = [];
        if (graphRes.ok) {
          const graph = await graphRes.json();
          const ids: number[] = graph.blocks
            .map((b: { id: number }) => b.id)
            .filter((id: number) => id !== focus.id);
          const fetched = await Promise.all(
            ids.map((id) =>
              fetch(`/api/block/${id}`).then((r) => (r.ok ? r.json() : null))
            )
          );
          citationBlocks = fetched.filter(Boolean);
        }

        const map = new Map<number, Block>();
        [...citationBlocks, ...topicBlocks].forEach((b) => map.set(b.id, b));
        const sorted = Array.from(map.values()).sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setBlocks(sorted);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [user]);

  return (
    <AuthGuard>
      <div className="max-w-3xl mx-auto p-6 space-y-4">
        {loading ? (
          <p>불러오는 중...</p>
        ) : blocks.length === 0 ? (
          <p>추천할 블록이 없습니다.</p>
        ) : (
          blocks.map((b) => <BlockCard key={b.id} {...b} />)
        )}
      </div>
    </AuthGuard>
  );
}
