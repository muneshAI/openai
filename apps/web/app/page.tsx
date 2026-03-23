import { ActivityLog } from '../components/ActivityLog';
import { ChatShell } from '../components/ChatShell';
import { TaskBoard } from '../components/TaskBoard';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-7xl space-y-6">
        <section className="grid gap-6 rounded-[2rem] border border-white/10 bg-gradient-to-br from-slate-900 via-slate-950 to-cyan-950/50 p-8 shadow-2xl shadow-cyan-950/30 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <p className="text-sm uppercase tracking-[0.5em] text-cyan-300">Munesh AI</p>
            <h1 className="mt-4 max-w-3xl text-5xl font-semibold tracking-tight text-white">
              An autonomous operating system for telecom growth, business automation, and executive productivity.
            </h1>
            <p className="mt-4 max-w-2xl text-lg text-slate-300">
              Think like a CEO, act like an operator, and execute like an automation engine with multi-agent
              orchestration, memory, analytics, and no-code app generation.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
              <p className="text-sm text-slate-400">Focus market</p>
              <p className="mt-2 text-2xl font-semibold">Nepal Telecom</p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
              <p className="text-sm text-slate-400">Core mode</p>
              <p className="mt-2 text-2xl font-semibold">Autonomous Ops</p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
              <p className="text-sm text-slate-400">Integrations</p>
              <p className="mt-2 text-2xl font-semibold">Gmail · Slack · Drive</p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
              <p className="text-sm text-slate-400">Decisioning</p>
              <p className="mt-2 text-2xl font-semibold">ROI + Risk + Next Steps</p>
            </div>
          </div>
        </section>

        <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <ChatShell />
          <ActivityLog />
        </div>

        <TaskBoard />
      </div>
    </main>
  );
}
