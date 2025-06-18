"use client";

import { useEffect, useState } from "react";
import BlockFeed from "@/components/BlockFeed";
import TopicTree, { TopicNode } from "@/components/TopicTree";

function buildTree(list: TopicNode[]): TopicNode[] {
  const map = new Map<number, TopicNode & { children: TopicNode[] }>();
  list.forEach((n) => map.set(n.id, { ...n, children: [] }));
  const roots: TopicNode[] = [];
  map.forEach((node) => {
    if (node.parent_id) {
      const parent = map.get(node.parent_id);
      if (parent) parent.children.push(node);
    } else {
      roots.push(node);
    }
  });
  return roots;
}

export default function ExplorePage() {
  const [topics, setTopics] = useState<TopicNode[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [sort, setSort] = useState<string>("newest");

  useEffect(() => {
    fetch("/api/topic")
      .then((res) => (res.ok ? res.json() : []))
      .then((data: TopicNode[]) => setTopics(buildTree(data)));
  }, []);

  return (
    <div className="flex p-6 gap-6">
      <div className="w-1/3 max-w-xs border-r pr-4 overflow-y-auto">
        <TopicTree nodes={topics} onSelect={setSelected} selected={selected} />
      </div>
      <div className="flex-1">
        <div className="flex justify-end mb-4">
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="border rounded px-2 py-1 text-sm dark:bg-gray-700"
          >
            <option value="newest">최신순</option>
            <option value="oldest">오래된순</option>
            <option value="trust">신뢰도순</option>
          </select>
        </div>
        <BlockFeed topic={selected} sort={sort} />
      </div>
    </div>
  );
}