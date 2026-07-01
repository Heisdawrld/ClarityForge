export interface AIProvider {
  name: string;
  providerType: "openai" | "anthropic" | "groq" | "ollama";
  
  complete(prompt: string, options?: AICompletionOptions): Promise<AIResponse>;
  chat(messages: AIMessage[], options?: AICompletionOptions): Promise<AIResponse>;
}

export interface AICompletionOptions {
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  stop?: string[];
}

export interface AIResponse {
  content: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model: string;
  finishReason: "stop" | "length" | "content_filter" | "error";
}

export interface AIMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export type ProviderConfig = {
  apiKey?: string;
  baseUrl?: string;
  model?: string;
  timeout?: number;
};

export const DEFAULT_MODELS = {
  openai: {
    chat: "gpt-4-turbo-preview",
    completion: "gpt-3.5-turbo-instruct",
  },
  anthropic: {
    chat: "claude-3-opus-20240229",
    completion: "claude-3-opus-20240229",
  },
  groq: {
    chat: "mixtral-8x7b-32768",
    completion: "mixtral-8x7b-32768",
  },
  ollama: {
    chat: "llama2:latest",
    completion: "llama2:latest",
  },
} as const;

export interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  cost?: number;
}

export interface BudgetAlert {
  threshold: number;
  current: number;
  budget: number;
}
