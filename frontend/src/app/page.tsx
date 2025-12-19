"use client";

import { useMemo, useRef, useState, useTransition } from "react";

import { startAudit, resumeAudit } from "@/app/actions/review";
import { PdfViewer } from "@/components/pdf-viewer/core";
import { Button } from "@/components/ui/button";

type RiskItem = {
  id: string;
  title: string;
  summary: string;
  page: number;
  boxes: Array<{ x: number; y: number; w: number; h: number }>;
};

const risks: RiskItem[] = [
  {
    id: "liability",
    title: "Clause 2.1 - Liability",
    summary: "Ambiguous indemnity wording needs review.",
    page: 1,
    boxes: [
      { x: 72, y: 120, w: 260, h: 22 },
      { x: 72, y: 170, w: 320, h: 22 },
    ],
  },
  {
    id: "payment",
    title: "Payment terms",
    summary: "Confirm net-30 language matches policy.",
    page: 2,
    boxes: [{ x: 80, y: 210, w: 240, h: 20 }],
  },
];

type AuditStatus = "idle" | "waiting" | "reviewed";

export default function Home() {
  const [pageNumber, setPageNumber] = useState(1);
  const [activeRiskId, setActiveRiskId] = useState(risks[0]?.id ?? "");
  const [threadId, setThreadId] = useState<string | null>(null);
  const [auditStatus, setAuditStatus] = useState<AuditStatus>("idle");
  const [decision, setDecision] = useState("approve");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const viewerRef = useRef<HTMLDivElement | null>(null);

  const activeRisk = useMemo(
    () => risks.find((risk) => risk.id === activeRiskId),
    [activeRiskId]
  );

  const activeBoxes = useMemo(() => activeRisk?.boxes ?? [], [activeRisk]);

  const handleSelectRisk = (risk: RiskItem) => {
    setActiveRiskId(risk.id);
    setPageNumber(risk.page);
    viewerRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleStartAudit = () => {
    setError(null);
    startTransition(async () => {
      const result = await startAudit({
        inputText: `Audit request for ${activeRisk?.title ?? "document"}`,
      });
      if (result.error) {
        setError(result.error);
        return;
      }
      setThreadId(result.threadId ?? null);
      setAuditStatus("waiting");
    });
  };

  const handleSubmitDecision = () => {
    if (!threadId) {
      setError("Start an audit before submitting a decision.");
      return;
    }
    setError(null);
    startTransition(async () => {
      const result = await resumeAudit({ threadId, decision, notes });
      if (result.error) {
        setError(result.error);
        return;
      }
      setAuditStatus("reviewed");
    });
  };

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
            <div className="flex flex-col items-start gap-3">
              <Button
                className="h-11 rounded-full px-6 text-sm font-semibold"
                onClick={handleStartAudit}
                disabled={isPending}
              >
                {isPending ? "Starting..." : "Start Audit"}
              </Button>
              <p className="text-xs text-slate-500">
                Status: {auditStatus === "idle" ? "Idle" : auditStatus}
              </p>
              {threadId ? (
                <p className="text-xs text-slate-500">
                  Thread: {threadId.slice(0, 8)}
                </p>
              ) : null}
            </div>
          </div>
        </header>

        <section className="grid gap-8 lg:grid-cols-[2fr,1fr]">
          <div ref={viewerRef}>
            <PdfViewer
              fileUrl="/sample.pdf"
              boxes={activeBoxes}
              pageNumber={pageNumber}
              onPageChange={setPageNumber}
            />
          </div>
          <aside className="rounded-3xl border border-white/40 bg-white/70 p-6 text-sm text-slate-600 shadow-xl backdrop-blur">
            <h2 className="text-lg font-semibold text-slate-900">
              Active Highlights
            </h2>
            <div className="mt-4 space-y-3">
              {risks.map((risk) => {
                const isActive = risk.id === activeRiskId;
                return (
                  <button
                    key={risk.id}
                    type="button"
                    onClick={() => handleSelectRisk(risk)}
                    className={`w-full rounded-2xl border p-4 text-left transition ${
                      isActive
                        ? "border-rose-200 bg-rose-50/70"
                        : "border-slate-200 bg-white/70"
                    }`}
                  >
                    <p
                      className={`text-sm font-semibold ${
                        isActive ? "text-rose-700" : "text-slate-800"
                      }`}
                    >
                      {risk.title}
                    </p>
                    <p
                      className={`mt-2 text-xs ${
                        isActive ? "text-rose-600" : "text-slate-500"
                      }`}
                    >
                      {risk.summary}
                    </p>
                    <p className="mt-2 text-[11px] uppercase tracking-wide text-slate-400">
                      Page {risk.page}
                    </p>
                  </button>
                );
              })}
            </div>

            <div className="mt-6 rounded-2xl border border-slate-200 bg-white/80 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                Human Review
              </p>
              <p className="mt-2 text-sm font-semibold text-slate-800">
                Decision
              </p>
              <div className="mt-3 flex gap-2">
                <Button
                  type="button"
                  variant={decision === "approve" ? "default" : "outline"}
                  onClick={() => setDecision("approve")}
                  disabled={isPending}
                >
                  Approve
                </Button>
                <Button
                  type="button"
                  variant={decision === "escalate" ? "default" : "outline"}
                  onClick={() => setDecision("escalate")}
                  disabled={isPending}
                >
                  Escalate
                </Button>
              </div>
              <label className="mt-4 block text-xs font-semibold text-slate-600">
                Notes
              </label>
              <textarea
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white/80 p-3 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                rows={3}
                placeholder="Add a short note for the audit log."
              />
              <Button
                className="mt-4 w-full"
                onClick={handleSubmitDecision}
                disabled={isPending}
              >
                {isPending ? "Submitting..." : "Submit Decision"}
              </Button>
              {auditStatus === "reviewed" ? (
                <p className="mt-3 text-xs font-semibold text-emerald-600">
                  Reviewed
                </p>
              ) : null}
              {error ? (
                <p className="mt-3 text-xs text-rose-600">{error}</p>
              ) : null}
            </div>
          </aside>
        </section>
      </main>
    </div>
  );
}
