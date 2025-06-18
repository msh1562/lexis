"use client";
import React from "react";

export interface TrustBadgeProps {
  trust_score: number;
  vote_count: number;
}

export default function TrustBadge({ trust_score, vote_count }: TrustBadgeProps) {
  let color = "bg-gray-300";
  if (trust_score >= 0.8) {
    color = "bg-green-500";
  } else if (trust_score >= 0.5) {
    color = "bg-yellow-500";
  } else {
    color = "bg-red-500";
  }

  return (
    <div className="flex items-center gap-2 w-32">
      <div className="flex-1 h-2 bg-gray-200 rounded overflow-hidden">
        <div
          className={`h-full ${color}`}
          style={{ width: `${Math.round(trust_score * 100)}%` }}
        />
      </div>
      <span className="text-xs whitespace-nowrap text-gray-700 dark:text-gray-200">
        {Math.round(trust_score * 100)}% ({vote_count})
      </span>
    </div>
  );
}