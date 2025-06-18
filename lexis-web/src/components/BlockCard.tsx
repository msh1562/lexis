"use client";
import { useEffect, useState } from "react";
import TrustBadge from "./TrustBadge";

export interface BlockCardProps {
  id: number;
  title: string;
  content: string;
  topic?: string | null;
  /** URL of the original source when available */
  source_url?: string | null;
  trust_score: number;
  created_at: string;
}

export default function BlockCard({
  id,
  title,
  content,
  topic,
  source_url,
  trust_score,
  created_at,
}: BlockCardProps) {
  const [votes, setVotes] = useState(0);

  useEffect(() => {
    const loadVotes = async () => {
      const res = await fetch(`/api/trust/${id}`);
      if (res.ok) {
        const data = await res.json();
        setVotes(data.trust + data.distrust);
      }
    };
    loadVotes();
  }, [id]);
  return (
    <div className="border rounded-md p-4 bg-white dark:bg-gray-800 shadow-sm flex flex-col gap-2">
      <div className="flex justify-between items-start">
        <h2 className="text-lg font-semibold">{title}</h2>
        {topic && (
          <span className="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-700 rounded-full">
            {topic}
          </span>
        )}
      </div>
      <p className="text-sm whitespace-pre-wrap flex-grow text-gray-700 dark:text-gray-300">
        {content}
      </p>
      {source_url && (
        <a
          href={source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-blue-600 dark:text-blue-400 underline self-end"
        >
          원문 보기
        </a>
      )}
      <div className="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
        <span>{new Date(created_at).toLocaleString()}</span>
        <TrustBadge trust_score={trust_score} vote_count={votes} />
      </div>
    </div>
  );
}