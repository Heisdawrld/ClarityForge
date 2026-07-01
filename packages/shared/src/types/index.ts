export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ReasoningSession {
  id: string;
  userId: string;
  title: string;
  input: string;
  output: ReasoningOutput;
  createdAt: Date;
  updatedAt: Date;
}

export interface ReasoningOutput {
  assumptions: Assumption[];
  biases: BiasFlag[];
  evidence: Evidence[];
  alternatives: Alternative[];
  questions: Question[];
  confidenceScore: number;
  nodes: ReasoningNode[];
}

export interface Assumption {
  id: string;
  text: string;
  isExplicit: boolean;
  confidence: number;
}

export interface BiasFlag {
  id: string;
  type: BiasType;
  name: string;
  description: string;
  severity: "low" | "medium" | "high";
  nodeId?: string;
  mitigation: string;
}

export type BiasType =
  | "confirmation"
  | "anchoring"
  | "availability"
  | "survivorship"
  | "sunk_cost"
  | "status_quo"
  | "bandwagon"
  | "halo"
  | "authority"
  | "groupthink";

export interface Evidence {
  id: string;
  content: string;
  source: string;
  url?: string;
  relevance: number;
  polarity: "supporting" | "opposing" | "neutral";
}

export interface Alternative {
  id: string;
  perspective: string;
  reasoning: string;
  strength: number;
}

export interface Question {
  id: string;
  text: string;
  priority: "high" | "medium" | "low";
  category: string;
  answered?: boolean;
}

export interface ReasoningNode {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  data: Record<string, unknown>;
}

export type NodeType =
  | "input"
  | "assumption"
  | "bias"
  | "evidence"
  | "alternative"
  | "question"
  | "conclusion";

export interface Prediction {
  id: string;
  sessionId: string;
  userId: string;
  prediction: string;
  probability?: number;
  outcome?: string;
  actualOutcome?: string;
  isCorrect?: boolean;
  resolvedAt?: Date;
  createdAt: Date;
}

export interface CalibrationMetrics {
  userId: string;
  calibrationScore: number;
  biasPatternScore: Record<BiasType, number>;
  totalPredictions: number;
  correctPredictions: number;
  averageConfidence: number;
  updatedAt: Date;
}
