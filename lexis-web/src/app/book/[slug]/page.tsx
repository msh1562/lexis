import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import TrustBadge from "@/components/TrustBadge";

interface Block {
  id: number;
  title: string;
  content: string;
  topic: string;
  trust_score: number;
  created_at: string;
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

interface Book {
  title: string;
  description: string | null;
  slug: string;
  blocks: Block[];
}

async function fetchBook(slug: string): Promise<Book | null> {
  try {
    const res = await fetch(`http://localhost:8000/api/book/${slug}`);
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function BookPage({ params }: { params: { slug: string } }) {
  const book = await fetchBook(params.slug);
  if (!book) return notFound();
  const votes = await Promise.all(book.blocks.map((b) => fetchTrust(b.id)));

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">{book.title}</h1>
        {book.description && <p className="text-gray-700 dark:text-gray-300">{book.description}</p>}
      </div>
      {book.blocks.map((b, i) => (
        <div key={b.id} className="border rounded-md p-4 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <h2 className="text-xl font-semibold">{b.title}</h2>
            <TrustBadge trust_score={b.trust_score} vote_count={votes[i] || 0} />
          </div>
          <ReactMarkdown className="prose dark:prose-invert mb-2">{b.content}</ReactMarkdown>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {new Date(b.created_at).toLocaleString()} | {b.topic}
          </div>
        </div>
      ))}
    </div>
  );
}