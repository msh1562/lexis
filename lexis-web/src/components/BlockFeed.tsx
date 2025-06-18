"use client";

import { useEffect, useState } from "react";
import BlockCard from "./BlockCard";

export interface Block {
  id: number;
  title: string;
  content: string;
  topic: string | null;
  source_url: string | null;
  trust_score: number;
  created_at: string;
}

export default function BlockFeed({
  topic,
  sort,
}: {
  topic: string;
  sort: string;
}) {
  const [blocks, setBlocks] = useState<Block[]>([]);

  const loadBlocks = async (selected: string, order: string) => {
    const params = new URLSearchParams();
    if (selected && selected !== "all") {
      params.set("topic", selected);
    }
    if (order) {
      params.set("sort", order);
    }
    const url = `/api/block?${params.toString()}`;
    const res = await fetch(url);
    if (res.ok) {
      const data: Block[] = await res.json();
      setBlocks(data);
    }
  };

  useEffect(() => {
    loadBlocks(topic, sort);
  }, [topic, sort]);

  return (
    <div className="space-y-4">
      {blocks.map((b) => (
        <BlockCard
          key={b.id}
          id={b.id}
          title={b.title}
          content={b.content}
          source_url={b.source_url}
          trust_score={b.trust_score}
          created_at={b.created_at}
          topic={b.topic}
        />
      ))}
    </div>
  );
}
