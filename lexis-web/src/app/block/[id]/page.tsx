import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import TrustBadge from "@/components/TrustBadge";
import QuoteButton from "@/components/QuoteButton";
import LexisMap from "@/components/LexisMap";
import ViewHistory from "@/components/ViewHistory";

interface Block {
  id: number;
  title: string;
  content: string;
  created_at: string;
  trust_score: number;
  source_url?: string | null;
}

async function fetchBlock(id: string): Promise<Block | null> {
  try {
    const res = await fetch(`http://localhost:8000/api/block/${id}`);
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

async function fetchSummary(text: string): Promise<string> {
  try {
    const res = await fetch("http://localhost:8000/api/lexify/summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) return "";
    const data = await res.json();
    return data.summary;
  } catch {
    return "";
  }
}

async function fetchTrust(blockId: number): Promise<number> {
  try {
    const res = await fetch(`http://localhost:8000/api/trust/${blockId}`);
    if (!res.ok) return 0;
    const data = await res.json();
    return data.trust + data.distrust;
  } catch {
    return 0;
  }
}

export default async function BlockPage({
  params,
}: {
  params: { id: string };
}) {
  const block = await fetchBlock(params.id);
  if (!block) return notFound();
  const summary = await fetchSummary(block.content);
  const votes = await fetchTrust(block.id);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <ViewHistory blockId={block.id} />
      <div className="flex justify-between items-start">
        <h1 className="text-3xl font-bold">{block.title}</h1>
        <div className="ml-4">
          <TrustBadge trust_score={block.trust_score} vote_count={votes} />
        </div>
      </div>
      {block.source_url && (
        <a
          href={block.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-blue-600 dark:text-blue-400 underline"
        >
          원문 링크
        </a>
      )}
      <ReactMarkdown className="prose dark:prose-invert">
        {block.content}
      </ReactMarkdown>
      {summary && (
        <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-md">
          <h2 className="font-semibold mb-2">요약</h2>
          <p className="text-sm whitespace-pre-wrap">{summary}</p>
        </div>
      )}
      <QuoteButton text={block.content} />
      <a
        href={`/?to_block_id=${block.id}`}
        className="inline-block px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
      >
        이 블록을 인용해서 새로운 글 쓰기
      </a>
      <div>
        <h2 className="font-semibold mt-6 mb-2">인용 흐름</h2>
        <LexisMap blockId={block.id} />
      </div>
      <div className="text-sm text-gray-500 dark:text-gray-400 text-right">
        {new Date(block.created_at).toLocaleString()}
      </div>
    </div>
  );
}