"use server";

type StartAuditInput = {
  inputText: string;
};

type StartAuditResult = {
  threadId?: string;
  interrupt?: unknown;
  error?: string;
};

type ResumeAuditInput = {
  threadId: string;
  decision: string;
  notes: string;
};

type ResumeAuditResult = {
  threadId?: string;
  decision?: string;
  notes?: string;
  error?: string;
};

const backendUrl =
  process.env.BACKEND_URL ??
  process.env.NEXT_PUBLIC_BACKEND_URL ??
  "http://localhost:8000";

export async function startAudit(
  input: StartAuditInput
): Promise<StartAuditResult> {
  try {
    const response = await fetch(`${backendUrl}/api/v1/audit/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input_text: input.inputText }),
      cache: "no-store",
    });

    if (!response.ok) {
      return { error: `Start audit failed (${response.status}).` };
    }

    const data = (await response.json()) as {
      thread_id: string;
      interrupt?: unknown;
    };
    return { threadId: data.thread_id, interrupt: data.interrupt };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : "Start audit failed.",
    };
  }
}

export async function resumeAudit(
  input: ResumeAuditInput
): Promise<ResumeAuditResult> {
  try {
    const response = await fetch(`${backendUrl}/api/v1/audit/resume`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        thread_id: input.threadId,
        decision: input.decision,
        notes: input.notes,
      }),
      cache: "no-store",
    });

    if (!response.ok) {
      return { error: `Resume audit failed (${response.status}).` };
    }

    const data = (await response.json()) as {
      thread_id: string;
      decision: string;
      notes: string;
    };
    return { threadId: data.thread_id, decision: data.decision, notes: data.notes };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : "Resume audit failed.",
    };
  }
}
