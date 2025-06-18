"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  return (
    <header className="p-4 border-b mb-4 flex justify-between items-center">
      <Link href="/" className="font-bold">
        Lexis
      </Link>
      <div className="flex items-center gap-4">
        <Link href="/explore" className="text-sm hover:underline">
          탐색
        </Link>
        {user && (
          <Link href="/feed" className="text-sm hover:underline">
            추천
          </Link>
        )}
        {user && (
          <Link href="/book/new" className="text-sm hover:underline">
            새 책 만들기
          </Link>
        )}
        {user ? (
          <button
            onClick={logout}
            className="text-sm text-red-600 hover:underline"
          >
            로그아웃
          </button>
        ) : (
          <>
            <Link href="/login" className="text-sm hover:underline">
              로그인
            </Link>
            <Link href="/signup" className="text-sm hover:underline">
              회원가입
            </Link>
          </>
        )}
      </div>
    </header>
  );
}