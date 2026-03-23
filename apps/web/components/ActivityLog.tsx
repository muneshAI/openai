import { ActivityItem } from '../lib/types';

const items: ActivityItem[] = [
  {
    id: '1',
    agent: 'Research Agent',
    message: 'Mapped high-opportunity target segments in Bagmati, Gandaki, and Lumbini.',
    time: '2 min ago',
  },
  {
    id: '2',
    agent: 'Decision Agent',
    message: 'Recommended phased rollout with pilot budget and KPI guardrails.',
    time: '1 min ago',
  },
  {
    id: '3',
    agent: 'Execution Agent',
    message: 'Prepared Gmail, WhatsApp, and Drive automations pending approval.',
    time: 'now',
  },
];

export function ActivityLog() {
  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
      <div className="mb-4">
        <p className="text-sm uppercase tracking-[0.3em] text-emerald-300">Live Ops Feed</p>
        <h2 className="text-2xl font-semibold text-white">Agent activity and savings</h2>
      </div>

      <div className="space-y-4">
        {items.map((item) => (
          <article key={item.id} className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
            <div className="flex items-center justify-between text-sm text-slate-400">
              <span>{item.agent}</span>
              <span>{item.time}</span>
            </div>
            <p className="mt-2 text-sm text-slate-200">{item.message}</p>
          </article>
        ))}
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-cyan-400/20 bg-cyan-500/10 p-4">
          <p className="text-sm text-cyan-200">Automation Hours Saved</p>
          <p className="mt-2 text-3xl font-semibold text-white">68h</p>
        </div>
        <div className="rounded-2xl border border-fuchsia-400/20 bg-fuchsia-500/10 p-4">
          <p className="text-sm text-fuchsia-200">Projected ROI</p>
          <p className="mt-2 text-3xl font-semibold text-white">+18%</p>
        </div>
        <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4">
          <p className="text-sm text-emerald-200">Voice Commands</p>
          <p className="mt-2 text-3xl font-semibold text-white">Enabled</p>
        </div>
      </div>
    </section>
  );
}
