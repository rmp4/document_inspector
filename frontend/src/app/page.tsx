import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#f8fafc,_#dbeafe_40%,_#e2e8f0_75%)] text-slate-900">
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 pb-20 pt-16">
        <header className="flex flex-col gap-6 rounded-3xl border border-white/40 bg-white/70 p-10 shadow-xl backdrop-blur">
          <div className="flex flex-wrap items-center justify-between gap-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-500">
                Docling Audit Agent
              </p>
              <h1 className="mt-3 text-3xl font-semibold leading-tight text-slate-900 md:text-4xl">
                Docling Audit Agent
              </h1>
              <p className="mt-3 max-w-2xl text-sm text-slate-600 md:text-base">
                Upload a contract, audit highlighted passages, and keep every
                bounding box aligned with your PDF canvas.
              </p>
            </div>
            <Button className="h-11 rounded-full px-6 text-sm font-semibold">
              Start Audit
            </Button>
          </div>
        </header>

        <section className="rounded-3xl border border-white/40 bg-white/70 p-8 text-sm text-slate-600 shadow-xl backdrop-blur">
          <h2 className="text-lg font-semibold text-slate-900">
            Project status
          </h2>
          <p className="mt-3 max-w-2xl">
            The frontend shell is ready. Next up: PDF rendering, zoom controls,
            and bbox overlays.
          </p>
        </section>
      </main>
    </div>
  );
}
