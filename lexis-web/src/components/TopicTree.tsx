"use client";

export interface TopicNode {
  id: number;
  name: string;
  parent_id: number | null;
  children?: TopicNode[];
}

interface ItemProps {
  node: TopicNode;
  level: number;
  onSelect: (name: string) => void;
  selected: string;
}

function TopicItem({ node, level, onSelect, selected }: ItemProps) {
  return (
    <li>
      <button
        onClick={() => onSelect(node.name)}
        className={`block w-full text-left px-2 py-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 ${
          selected === node.name ? "bg-blue-500 text-white" : ""
        }`}
        style={{ paddingLeft: level * 16 }}
      >
        {node.name}
      </button>
      {node.children && node.children.length > 0 && (
        <ul className="mt-1">
          {node.children.map((child) => (
            <TopicItem
              key={child.id}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selected={selected}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

export default function TopicTree({
  nodes,
  onSelect,
  selected,
}: {
  nodes: TopicNode[];
  onSelect: (name: string) => void;
  selected: string;
}) {
  return (
    <ul className="space-y-1">
      {nodes.map((n) => (
        <TopicItem
          key={n.id}
          node={n}
          level={0}
          onSelect={onSelect}
          selected={selected}
        />
      ))}
    </ul>
  );
}