const examplePrompt = 'Launch a telecom campaign in Nepal focused on enterprise and prepaid growth.';

export function ChatShell() {
  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl shadow-cyan-950/30">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Command Center</p>
          <h2 className="text-2xl font-semibold text-white">Talk to Munesh AI like your operating system</h2>
        </div>
        <span className="rounded-full border border-emerald-400/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">
          Voice Ready
        </span>
      </div>

      <div className="rounded-2xl border border-white/10 bg-slate-950/80 p-4 text-slate-300">
        <p className="text-sm text-slate-400">Example prompt</p>
        <p className="mt-2 text-base text-white">“{examplePrompt}”</p>
      </div>

      <div className="mt-4 rounded-2xl border border-cyan-400/20 bg-cyan-400/5 p-4 text-sm text-slate-200">
        Munesh AI converts intent into a task graph, collaborates across specialist agents, and returns timelines,
        automations, ROI signals, and execution-ready assets.
      </div>
    </section>
  );
}
