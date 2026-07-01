import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface AssumptionNodeData {
  label: string;
  isExplicit: boolean;
  confidence: number;
}

export function AssumptionNode({ data, selected }: NodeProps) {
  const nodeData = data as AssumptionNodeData;

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 bg-purple-50 border-purple-300 min-w-[200px]",
        selected && "ring-2 ring-purple-500"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold text-purple-600 uppercase">Assumption</span>
        <span className={cn(
          "text-xs px-1.5 py-0.5 rounded",
          nodeData.isExplicit ? "bg-purple-200 text-purple-800" : "bg-gray-200 text-gray-600"
        )}>
          {nodeData.isExplicit ? "Explicit" : "Implicit"}
        </span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-gray-500">Confidence:</span>
        <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-purple-500"
            style={{ width: `${(nodeData.confidence || 0.7) * 100}%` }}
          />
        </div>
        <span className="text-xs text-gray-600">{Math.round((nodeData.confidence || 0.7) * 100)}%</span>
      </div>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-purple-500" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-purple-500" />
    </div>
  );
}
