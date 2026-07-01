"use client";

import { useCallback, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  Connection,
  Edge,
  Node,
  BackgroundVariant,
  Panel,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { InputNode } from "./nodes/InputNode";
import { AssumptionNode } from "./nodes/AssumptionNode";
import { BiasNode } from "./nodes/BiasNode";
import { EvidenceNode } from "./nodes/EvidenceNode";
import { AlternativeNode } from "./nodes/AlternativeNode";
import { QuestionNode } from "./nodes/QuestionNode";
import { ConclusionNode } from "./nodes/ConclusionNode";
import { Toolbar } from "./Toolbar";
import { cn } from "@/lib/utils";

const nodeTypes = {
  input: InputNode,
  assumption: AssumptionNode,
  bias: BiasNode,
  evidence: EvidenceNode,
  alternative: AlternativeNode,
  question: QuestionNode,
  conclusion: ConclusionNode,
};

const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    position: { x: 250, y: 50 },
    data: { label: "What's the best strategy for scaling our startup?" },
  },
];

const initialEdges: Edge[] = [];

interface ReasoningWorkspaceProps {
  className?: string;
}

export function ReasoningWorkspace({ className }: ReasoningWorkspaceProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  const onNodeUpdate = useCallback(
    (nodeId: string, data: Record<string, unknown>) => {
      setNodes((nds) =>
        nds.map((node) =>
          node.id === nodeId ? { ...node, data: { ...node.data, ...data } } : node
        )
      );
    },
    [setNodes]
  );

  const onAddNode = useCallback(
    (type: string) => {
      const newNode: Node = {
        id: `${Date.now()}`,
        type,
        position: { x: Math.random() * 400, y: Math.random() * 400 },
        data: { label: `New ${type}` },
      };
      setNodes((nds) => [...nds, newNode]);
    },
    [setNodes]
  );

  return (
    <div className={cn("w-full h-full", className)}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        <Controls />
        <MiniMap
          nodeStrokeWidth={3}
          zoomable
          pannable
          style={{ bottom: 80, right: 20 }}
        />
        <Panel position="top-left">
          <Toolbar onAddNode={onAddNode} />
        </Panel>
        <Panel position="top-right">
          {selectedNode && (
            <div className="bg-white p-4 rounded-lg shadow-lg border">
              <h3 className="font-semibold mb-2">Node Properties</h3>
              <p className="text-sm text-gray-600">Type: {selectedNode.type}</p>
            </div>
          )}
        </Panel>
      </ReactFlow>
    </div>
  );
}
