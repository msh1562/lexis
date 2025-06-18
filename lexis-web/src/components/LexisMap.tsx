"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const ForceGraph2D = dynamic(
  () => import("react-force-graph").then((m) => m.ForceGraph2D),
  { ssr: false }
);

interface BlockNode {
  id: number;
  title: string;
}

interface CitationEdge {
  from_block_id: number;
  to_block_id: number;
  type: "quote" | "refute" | "extend";
}

interface GraphResponse {
  blocks: BlockNode[];
  citations: CitationEdge[];
}

interface NodeData {
  id: number;
  title: string;
  root?: boolean;
}

interface LinkData {
  source: number;
  target: number;
  type: CitationEdge["type"];
}

export default function LexisMap({ blockId }: { blockId: number }) {
  const [nodes, setNodes] = useState<NodeData[]>([]);
  const [links, setLinks] = useState<LinkData[]>([]);

  useEffect(() => {
    fetch(`/api/citation/graph/${blockId}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((res: GraphResponse | null) => {
        if (res) {
          setNodes(
            res.blocks.map((b) => ({ id: b.id, title: b.title, root: b.id === blockId }))
          );
          setLinks(
            res.citations.map((c) => ({
              source: c.from_block_id,
              target: c.to_block_id,
              type: c.type,
            }))
          );
        }
      });
  }, [blockId]);

  return (
    <div className="w-full h-96 border rounded-md">
      <ForceGraph2D
        graphData={{ nodes, links }}
        nodeId="id"
        nodeLabel={(node: NodeData) => node.title}
        nodeRelSize={4}
        nodeColor={(node: NodeData) => (node.root ? "#f59e0b" : "#3b82f6")}
        linkColor={(link: LinkData) => {
          switch (link.type) {
            case "refute":
              return "#ef4444";
            case "extend":
              return "#10b981";
            default:
              return "#64748b";
          }
        }}
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={1}
      />
    </div>
  );
}