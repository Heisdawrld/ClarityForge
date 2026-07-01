import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface EvidenceNodeData {
  label: string;
  source: string;
  url?: string;
  relevance: number;
  polarity: "supporting" | "opposing" | "neutral";
}

const polarityColors = {
  supporting: "bg-green-50 border-green-300",
  opposing: "bg-red-50 border-red-300",
  neutral: "bg-gray-50 border-gray-300",
};

const polarityIcons = {
  supporting: "✅",
  opposing: "❌",
  neutral: "➖",
};

export function EvidenceNode({ data, selected }: NodeProps) {
  const nodeData = data as EvidenceNodeData;
  const polarity = nodeData.polarity || "neutral";

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 min-w-[200px]",
        polarityColors[polarity],
        selected && "ring-2 ring-offset-2 ring-gray-400"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold uppercase">{polarityIcons[polarity]} Evidence</span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      <div className="mt-2 flex items-center justify-between">
        <span className="text-xs text-gray-500 truncate max-w-[120px]">
          {nodeData.source || "Unknown source"}
        </span>
        <span className="text-xs text-gray-400">
          {Math.round((nodeData.relevance || 0.5) * 100)}% relevant
        </span>
      </div>
      {nodeData.url && (
        <a
          href={nodeData.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-blue-500 hover:underline mt-1 block"
        >
          🔗 View source
        </a>
      )}
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-gray-400" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-gray-400" />
    </div>
  );
}
