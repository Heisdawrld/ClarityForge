import { Handle, Position, NodeProps } from "@xyflow/react";
import { cn } from "@/lib/utils";

interface ConclusionNodeData {
  label: string;
  confidence: number;
  keyPoints: string[];
}

export function ConclusionNode({ data, selected }: NodeProps) {
  const nodeData = data as ConclusionNodeData;
  const confidence = nodeData.confidence || 0.7;

  return (
    <div
      className={cn(
        "px-4 py-3 rounded-lg border-2 bg-indigo-50 border-indigo-300 min-w-[240px]",
        selected && "ring-2 ring-indigo-500"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xs font-semibold text-indigo-600 uppercase">Conclusion</span>
        <span className="text-xs px-1.5 py-0.5 rounded bg-indigo-200 text-indigo-800">
          Final
        </span>
      </div>
      <p className="text-sm font-medium text-gray-800">{nodeData.label}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-xs text-gray-500">Confidence:</span>
        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={cn(
              "h-full transition-all",
              confidence >= 0.8 ? "bg-green-500" : confidence >= 0.5 ? "bg-yellow-500" : "bg-red-500"
            )}
            style={{ width: `${confidence * 100}%` }}
          />
        </div>
        <span className="text-xs text-gray-600 font-medium">{Math.round(confidence * 100)}%</span>
      </div>
      {nodeData.keyPoints && nodeData.keyPoints.length > 0 && (
        <div className="mt-3 pt-2 border-t border-indigo-200">
          <span className="text-xs font-semibold text-indigo-600">Key Points:</span>
          <ul className="mt-1 space-y-1">
            {nodeData.keyPoints.slice(0, 3).map((point, idx) => (
              <li key={idx} className="text-xs text-gray-600 flex items-start gap-1">
                <span className="text-indigo-400">•</span>
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-indigo-500" />
    </div>
  );
}
