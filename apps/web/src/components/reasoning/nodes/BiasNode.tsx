import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface BiasNodeData {
  label: string;
  biasType: string;
  severity: "low" | "medium" | "high";
  mitigation: string;
}

const severityColors = {
  low: "bg-yellow-50 border-yellow-300 text-yellow-600",
  medium: "bg-orange-50 border-orange-300 text-orange-600",
  high: "bg-red-50 border-red-300 text-red-600",
};

export function BiasNode({ data, selected }: NodeProps) {
  const nodeData = data as BiasNodeData;
  const severity = nodeData.severity || "medium";

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 min-w-[220px]",
        severityColors[severity],
        selected && "ring-2 ring-offset-2"
      )}
      style={{ 
        backgroundColor: severity === "low" ? "#fefce8" : severity === "medium" ? "#fff7ed" : "#fef2f2",
        borderColor: severity === "low" ? "#fcd34d" : severity === "medium" ? "#fb923c" : "#f87171",
        ...(selected && { ringColor: severity === "low" ? "#eab308" : severity === "medium" ? "#ea580c" : "#dc2626" })
      }}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold uppercase">⚠️ Bias</span>
        <span className="text-xs px-1.5 py-0.5 rounded bg-white/50">
          {nodeData.biasType || "Cognitive"}
        </span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      {nodeData.mitigation && (
        <p className="text-xs text-gray-600 mt-2 p-2 bg-white/50 rounded">
          💡 {nodeData.mitigation}
        </p>
      )}
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-orange-500" />
    </div>
  );
}
