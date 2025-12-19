import { Button } from "@/components/ui/button";
import { PdfViewer } from "@/components/pdf-viewer/core";

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

        <section className="grid gap-8 lg:grid-cols-[2fr,1fr]">
          <PdfViewer
            fileUrl="/sample.pdf"
            boxes={[
              { x: 72, y: 120, w: 260, h: 22 },
              { x: 72, y: 170, w: 320, h: 22 },
            ]}
          />
          <aside className="rounded-3xl border border-white/40 bg-white/70 p-6 text-sm text-slate-600 shadow-xl backdrop-blur">
            <h2 className="text-lg font-semibold text-slate-900">
              Active Highlights
            </h2>
            <div className="mt-4 space-y-3">
              <div className="rounded-2xl border border-rose-200 bg-rose-50/70 p-4">
                <p className="text-sm font-semibold text-rose-700">
                  Clause 2.1 — Liability
                </p>
                <p className="mt-2 text-xs text-rose-600">
                  Needs human review due to ambiguous indemnity wording.
                </p>
              </div>
              <div className="rounded-2xl border border-amber-200 bg-amber-50/70 p-4">
                <p className="text-sm font-semibold text-amber-700">
                  Payment terms
                </p>
                <p className="mt-2 text-xs text-amber-600">
                  PDF preview ready for bbox overlay.
                </p>
              </div>
            </div>
          </aside>
        </section>
      </main>
    </div>
  );
}
