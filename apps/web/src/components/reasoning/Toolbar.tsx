"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ToolbarProps {
  onAddNode: (type: string) => void;
}

const nodeButtons = [
  { type: "assumption", label: "+ Assumption", icon: "🎯", color: "purple" },
  { type: "bias", label: "+ Bias", icon: "⚠️", color: "orange" },
  { type: "evidence", label: "+ Evidence", icon: "📚", color: "gray" },
  { type: "alternative", label: "+ Alternative", icon: "🔄", color: "teal" },
  { type: "question", label: "+ Question", icon: "❓", color: "yellow" },
  { type: "conclusion", label: "+ Conclusion", icon: "✅", color: "indigo" },
];

export function Toolbar({ onAddNode }: ToolbarProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg border p-2 flex flex-col gap-1">
      <div className="text-xs font-semibold text-gray-500 px-2 py-1">
        Add Node
      </div>
      {nodeButtons.map((btn) => (
        <Button
          key={btn.type}
          variant="ghost"
          size="sm"
          onClick={() => onAddNode(btn.type)}
          className={cn(
            "justify-start text-xs h-8",
            btn.color === "purple" && "text-purple-600 hover:text-purple-700 hover:bg-purple-50",
            btn.color === "orange" && "text-orange-600 hover:text-orange-700 hover:bg-orange-50",
            btn.color === "gray" && "text-gray-600 hover:text-gray-700 hover:bg-gray-50",
            btn.color === "teal" && "text-teal-600 hover:text-teal-700 hover:bg-teal-50",
            btn.color === "yellow" && "text-yellow-600 hover:text-yellow-700 hover:bg-yellow-50",
            btn.color === "indigo" && "text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50"
          )}
        >
          <span className="mr-2">{btn.icon}</span>
          {btn.label}
        </Button>
      ))}
      <div className="border-t my-1" />
      <Button variant="ghost" size="sm" className="text-xs h-8 justify-start text-gray-600">
        🗑️ Clear All
      </Button>
      <Button variant="ghost" size="sm" className="text-xs h-8 justify-start text-gray-600">
        📥 Export
      </Button>
    </div>
  );
}
