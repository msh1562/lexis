"use client";

import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";

export default function ViewHistory({ blockId }: { blockId: number }) {
  const { user, token } = useAuth();

  useEffect(() => {
    if (!user) return;

    fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/history/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        user_id: user.id,
        block_id: blockId,
        action: "view",
      }),
    }).catch(() => {});
  }, [user, token, blockId]);

  return null;
}