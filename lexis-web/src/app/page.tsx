"use client";

import { useEffect, useState } from "react";
import LexifyEditor from "@/components/LexifyEditor";
import BlockFeed from "@/components/BlockFeed";

interface Block { topic: string | null }

export default function Home() {
  const [topics, setTopics] = useState<string[]>([]);
  const [selected, setSelected] = useState("all");

  const loadTopics = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/block`);
    if (res.ok) {
      const data: Block[] = await res.json();
      const unique = [...new Set(data.filter((b) => b.topic).map((b) => b.topic as string))];
      setTopics(unique);
    }
  };

  useEffect(() => {
    loadTopics();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      <LexifyEditor />
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setSelected("all")}
          className={`px-3 py-1 rounded-md text-sm border ${
            selected === "all" ? "bg-blue-600 text-white" : "bg-white dark:bg-gray-800"
          }`}
        >
          전체
        </button>
        {topics.map((topic) => (
          <button
            key={topic}
            onClick={() => setSelected(topic)}
            className={`px-3 py-1 rounded-md text-sm border ${
              selected === topic ? "bg-blue-600 text-white" : "bg-white dark:bg-gray-800"
            }`}
          >
            {topic}
          </button>
        ))}
      </div>
      <BlockFeed topic={selected} sort="newest" />
    </div>
  );
}