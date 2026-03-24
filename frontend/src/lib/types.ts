export type Step = {
  task_id: string;
  agent: string;
  status: string;
  output_keys: string[];
};

export type ExecutionResponse = {
  trace_id: string;
  goal: string;
  status: string;
  steps: Step[];
  summary: string;
};
