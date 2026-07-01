import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface QuestionNodeData {
  label: string;
  priority: "high" | "medium" | "low";
  category: string;
  answered?: boolean;
}

const priorityColors = {
  high: "bg-red-50 border-red-300 text-red-700",
  medium: "bg-yellow-50 border-yellow-300 text-yellow-700",
  low: "bg-blue-50 border-blue-300 text-blue-700",
};

const priorityBadgeColors = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-blue-100 text-blue-800",
};

export function QuestionNode({ data, selected }: NodeProps) {
  const nodeData = data as QuestionNodeData;
  const priority = nodeData.priority || "medium";

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 min-w-[200px]",
        priorityColors[priority],
        selected && "ring-2 ring-offset-2"
      )}
      style={{
        ...(priority === "high" && { borderColor: "#fca5a5", backgroundColor: "#fef2f2" }),
        ...(priority === "medium" && { borderColor: "#fcd34d", backgroundColor: "#fefce8" }),
        ...(priority === "low" && { borderColor: "#93c5fd", backgroundColor: "#eff6ff" }),
      }}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold uppercase">❓ Question</span>
        <span className={cn(
          "text-xs px-1.5 py-0.5 rounded",
          priorityBadgeColors[priority]
        )}>
          {priority} priority
        </span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-gray-500">Category:</span>
        <span className="text-xs text-gray-600">{nodeData.category || "General"}</span>
      </div>
      {nodeData.answered !== undefined && (
        <div className="mt-2 flex items-center gap-2">
          <span className={cn(
            "text-xs px-2 py-1 rounded",
            nodeData.answered ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"
          )}>
            {nodeData.answered ? "✅ Answered" : "⏳ Pending"}
          </span>
        </div>
      )}
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-yellow-500" />
    </div>
  );
}
