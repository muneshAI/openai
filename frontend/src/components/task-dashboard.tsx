"use client";

import { useState } from "react";
import type { ExecutionResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/v1/execute";

export function TaskDashboard() {
  const [goal, setGoal] = useState("One prompt → full app build for expense tracker");
  const [response, setResponse] = useState<ExecutionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal, context: { voiceInput: false, streaming: true } }),
      });
      const data = (await res.json()) as ExecutionResponse;
      setResponse(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 24, fontFamily: "sans-serif" }}>
      <h1>Munesh AI — Multi-Agent Control Tower</h1>
      <p>Plan • Execute • Validate • Improve</p>

      <textarea value={goal} onChange={(e) => setGoal(e.target.value)} rows={4} style={{ width: "100%" }} />
      <button onClick={submit} disabled={loading} style={{ marginTop: 12 }}>
        {loading ? "Running..." : "Run Autonomous Workflow"}
      </button>

      {response && (
        <section style={{ marginTop: 24 }}>
          <h2>Status: {response.status}</h2>
          <p>{response.summary}</p>
          <h3>Trace: {response.trace_id}</h3>
          <ul>
            {response.steps.map((step) => (
              <li key={step.task_id}>
                <strong>{step.task_id}</strong> - {step.agent} - {step.status} ({step.output_keys.join(", ")})
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
