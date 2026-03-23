import { TaskCard } from '../lib/types';

const tasks: TaskCard[] = [
  {
    id: '1',
    title: 'Research Nepal telecom demand signals',
    owner: 'research',
    status: 'running',
    description: 'Province-level segmentation, channel economics, and competitor scan.',
  },
  {
    id: '2',
    title: 'Prioritize launch strategy',
    owner: 'decision',
    status: 'pending',
    description: 'Select best rollout wave, KPI model, and budget allocation.',
  },
  {
    id: '3',
    title: 'Automate outreach and reporting',
    owner: 'execution',
    status: 'pending',
    description: 'Connect WhatsApp, Gmail, Calendar, and Drive workflows.',
  },
  {
    id: '4',
    title: 'Generate campaign dashboard',
    owner: 'coding',
    status: 'pending',
    description: 'Build an internal dashboard for KPI, ROI, and field operations.',
  },
];

const statusColor: Record<TaskCard['status'], string> = {
  pending: 'bg-slate-500/20 text-slate-200',
  running: 'bg-amber-500/20 text-amber-200',
  blocked: 'bg-rose-500/20 text-rose-200',
  complete: 'bg-emerald-500/20 text-emerald-200',
};

export function TaskBoard() {
  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-fuchsia-300">Execution Graph</p>
          <h2 className="text-2xl font-semibold text-white">Multi-agent task board</h2>
        </div>
        <span className="text-sm text-slate-400">Human approval gates enabled</span>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        {tasks.map((task) => (
          <article key={task.id} className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{task.owner} agent</p>
                <h3 className="mt-2 text-lg font-medium text-white">{task.title}</h3>
              </div>
              <span className={`rounded-full px-3 py-1 text-xs font-medium ${statusColor[task.status]}`}>
                {task.status}
              </span>
            </div>
            <p className="mt-3 text-sm text-slate-300">{task.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
