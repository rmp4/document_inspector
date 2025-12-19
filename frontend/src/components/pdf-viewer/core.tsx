"use client";

import { useMemo, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import { Button } from "@/components/ui/button";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

type PdfViewerProps = {
  fileUrl: string;
  boxes?: Array<{ x: number; y: number; w: number; h: number }>;
};

export function PdfViewer({ fileUrl }: PdfViewerProps) {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [error, setError] = useState<string | null>(null);

  const pageLabel = useMemo(() => {
    if (!numPages) {
      return "Page 1 / ?";
    }
    return `Page ${pageNumber} / ${numPages}`;
  }, [numPages, pageNumber]);

  return (
    <div className="w-full space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-white/20 bg-white/70 px-4 py-3 backdrop-blur">
        <div className="text-sm font-semibold text-slate-700">{pageLabel}</div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={() => setScale((value) => Math.max(0.6, value - 0.1))}
          >
            Zoom -
          </Button>
          <Button
            variant="outline"
            onClick={() => setScale((value) => Math.min(2, value + 0.1))}
          >
            Zoom +
          </Button>
          <Button
            variant="outline"
            onClick={() => setPageNumber((value) => Math.max(1, value - 1))}
          >
            Prev
          </Button>
          <Button
            variant="outline"
            onClick={() =>
              setPageNumber((value) =>
                numPages ? Math.min(numPages, value + 1) : value + 1
              )
            }
          >
            Next
          </Button>
        </div>
      </div>

      <div className="overflow-auto rounded-2xl border border-white/30 bg-white/80 p-6 shadow-lg">
        {error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        ) : (
          <div className="relative inline-block">
            <Document
              file={fileUrl}
              onLoadSuccess={(info) => setNumPages(info.numPages)}
              onLoadError={(err) => setError(err.message)}
              loading={
                <div className="text-sm font-medium text-slate-600">
                  Loading PDF...
                </div>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                renderTextLayer={false}
                renderAnnotationLayer={false}
              />
            </Document>
          </div>
        )}
      </div>
    </div>
  );
}
