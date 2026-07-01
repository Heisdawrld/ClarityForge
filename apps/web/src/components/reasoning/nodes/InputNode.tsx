import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface InputNodeData {
  label: string;
  description?: string;
}

export function InputNode({ data, selected }: NodeProps) {
  const nodeData = data as InputNodeData;

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 bg-blue-50 border-blue-300 min-w-[200px]",
        selected && "ring-2 ring-blue-500"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold text-blue-600 uppercase">Input</span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      {nodeData.description && (
        <p className="text-xs text-gray-500 mt-1">{nodeData.description}</p>
      )}
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-blue-500"
      />
    </div>
  );
}
