import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface AlternativeNodeData {
  label: string;
  perspective: string;
  reasoning: string;
  strength: number;
}

export function AlternativeNode({ data, selected }: NodeProps) {
  const nodeData = data as AlternativeNodeData;

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 bg-teal-50 border-teal-300 min-w-[220px]",
        selected && "ring-2 ring-teal-500"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold text-teal-600 uppercase">Alternative</span>
        <span className="text-xs px-1.5 py-0.5 rounded bg-teal-200 text-teal-800">
          Steelman
        </span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      {nodeData.perspective && (
        <p className="text-xs text-teal-600 mt-1 italic">
          From: {nodeData.perspective}
        </p>
      )}
      {nodeData.reasoning && (
        <p className="text-xs text-gray-600 mt-2 line-clamp-2">{nodeData.reasoning}</p>
      )}
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-gray-500">Strength:</span>
        <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-teal-500"
            style={{ width: `${(nodeData.strength || 0.5) * 100}%` }}
          />
        </div>
        <span className="text-xs text-gray-600">{Math.round((nodeData.strength || 0.5) * 100)}%</span>
      </div>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-teal-500" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-teal-500" />
    </div>
  );
}
