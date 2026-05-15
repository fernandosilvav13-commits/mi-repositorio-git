"use client";

import { useState, useRef, useEffect } from "react";
import Tile from "@/components/apple/Tile";
import FrostedContainer from "@/components/apple/FrostedContainer";
import PillChip from "@/components/apple/PillChip";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Upload, FileText, Trash2, ArrowLeft, Check, X } from "lucide-react";
import { toast } from "sonner";
import { api, uploadWithProgress } from "@/lib/api";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface UploadItem {
  file: File;
  progress: number;
  status: "pending" | "uploading" | "done" | "error";
  result?: any;
  error?: string;
}

export default function CrossrefPage() {
  const [files, setFiles] = useState<any[]>([]);
  const [uploadQueue, setUploadQueue] = useState<UploadItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleteTarget, setDeleteTarget] = useState<any | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [newFileIds, setNewFileIds] = useState<Set<string>>(new Set());
  const [removingId, setRemovingId] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      setLoading(true);
      const data = await api.crossref.list();
      setFiles(data || []);
    } catch {
      // not authenticated yet
    } finally {
      setLoading(false);
    }
  };

  const processUpload = async (file: File) => {
    try {
      const result = await uploadWithProgress(file, (percent) => {
        setUploadQueue((prev) =>
          prev.map((q) =>
            q.file === file ? { ...q, progress: percent } : q,
          ),
        );
      });

      // Mark as done
      setUploadQueue((prev) =>
        prev.map((q) =>
          q.file === file
            ? { ...q, status: "done", progress: 100, result }
            : q,
        ),
      );

      // Add to files list at top
      setFiles((prev) => [result, ...prev]);
      setNewFileIds((prev) => new Set(prev).add(result.id));

      // Remove from queue after completion display
      setTimeout(() => {
        setUploadQueue((prev) => prev.filter((q) => q.file !== file));
      }, 2000);

      // Clear new file ID after animation
      setTimeout(() => {
        setNewFileIds((prev) => {
          const next = new Set(prev);
          next.delete(result.id);
          return next;
        });
      }, 1500);
    } catch (e: any) {
      setUploadQueue((prev) =>
        prev.map((q) =>
          q.file === file
            ? { ...q, status: "error", error: e.message }
            : q,
        ),
      );
      toast.error(`Upload failed — ${e.message}`);
    }
  };

  const handleFilesSelected = (selectedFiles: File[]) => {
    const validFiles = Array.from(selectedFiles);
    const newItems: UploadItem[] = validFiles.map((f) => ({
      file: f,
      progress: 0,
      status: "pending" as const,
    }));
    setUploadQueue((prev) => [...prev, ...newItems]);

    // Process each file concurrently
    validFiles.forEach((file) => processUpload(file));
  };

  const retryUpload = (file: File) => {
    setUploadQueue((prev) =>
      prev.map((q) =>
        q.file === file
          ? { ...q, status: "uploading", progress: 0, error: undefined }
          : q,
      ),
    );
    processUpload(file);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFilesSelected(Array.from(e.target.files));
      e.target.value = "";
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFilesSelected(Array.from(e.dataTransfer.files));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    const targetId = deleteTarget.id;
    setDeleteTarget(null); // Close dialog immediately

    try {
      await api.crossref.delete(targetId);
      setRemovingId(targetId);

      // Animate out then remove from state
      setTimeout(() => {
        setFiles((prev) => prev.filter((f) => f.id !== targetId));
        setRemovingId(null);
        toast.success("File deleted");
      }, 300);
    } catch (e: any) {
      toast.error(e.message || "Error deleting file");
    }
  };

  const formatStatusLabel = (status: string | null | undefined): string => {
    if (status === "matched") return "Matched";
    if (status === "unmatched") return "Unmatched";
    return "Processing";
  };

  return (
    <div className="flex flex-col w-full bg-white">
      {/* Floating Back Button */}
      <div className="fixed top-8 left-8 z-50">
        <Link href="/">
          <Button
            variant="ghost"
            className="rounded-full bg-white/80 backdrop-blur-md shadow-sm hover:bg-white active-scale"
          >
            <ArrowLeft size={20} className="mr-2" />
            Back
          </Button>
        </Link>
      </div>

      {/* Section 1 — Upload Hero Tile */}
      <Tile variant="white" className="pt-32 pb-20">
        <h2 className="text-[21px] font-semibold tracking-[0.011em] text-ink/60 mb-2 uppercase">
          Collection
        </h2>
        <h1 className="apple-tight text-[40px] md:text-[48px] text-ink leading-[1.1] mb-10">
          Reference Data
        </h1>

        {/* Drop Zone */}
        <div
          role="button"
          aria-label="Upload cross-reference files"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              fileRef.current?.click();
            }
          }}
          onClick={() => fileRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "border-2 border-dashed rounded-lg p-12 md:p-16 text-center cursor-pointer transition-all duration-300 focus-visible:outline-2 focus-visible:outline-[#0071e3]",
            dragOver
              ? "border-action-blue border-solid bg-[rgba(0,102,204,0.08)] scale-[1.01]"
              : "border-black/8 hover:border-action-blue hover:bg-[rgba(0,102,204,0.03)]",
          )}
        >
          <input
            ref={fileRef}
            type="file"
            multiple
            className="hidden"
            accept=".pdf,.csv,.ppt,.pptx,.doc,.docx"
            onChange={handleInputChange}
          />
          <Upload size={40} className="text-ink/40 mx-auto" />
          <p className="text-[17px] font-normal text-ink/70 mt-4">
            Drop reference files here
          </p>
          <p className="text-[14px] text-ink/40 mt-1">or click to browse</p>
        </div>

        {/* Format Badges */}
        <div className="flex items-center justify-center gap-2 mt-6">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-[14px] font-semibold text-action-blue bg-action-blue/5">
            PDF
          </span>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-[14px] font-semibold text-action-blue bg-action-blue/5">
            CSV
          </span>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-[14px] font-semibold text-action-blue bg-action-blue/5">
            PPT
          </span>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-[14px] font-semibold text-action-blue bg-action-blue/5">
            DOCX
          </span>
        </div>

        {/* Upload Queue */}
        {uploadQueue.length > 0 && (
          <div className="w-full max-w-md mx-auto mt-6 space-y-3">
            {uploadQueue.map((item) => (
              <div
                key={item.file.name}
                className="flex items-center gap-4 w-full animate-in fade-in slide-in-from-top-2 duration-300"
              >
                <FileText size={18} className="text-ink/50 shrink-0" />
                <span className="text-[14px] font-medium truncate max-w-[140px] shrink-0">
                  {item.file.name}
                </span>
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <div className="h-1 rounded bg-black/8 flex-1 min-w-[60px]">
                    <div
                      className="h-full rounded bg-action-blue transition-all duration-300"
                      style={{ width: `${item.progress}%` }}
                      role="progressbar"
                      aria-valuenow={item.progress}
                      aria-valuemin={0}
                      aria-valuemax={100}
                    />
                  </div>
                  {item.status === "done" ? (
                    <span className="text-[14px] text-[#34c759] shrink-0 flex items-center gap-1">
                      <Check size={14} />
                      Complete
                    </span>
                  ) : item.status === "error" ? (
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="text-[14px] text-[#ff3b30] flex items-center gap-1">
                        <X size={14} />
                        Failed
                      </span>
                      <Button
                        variant="ghost"
                        size="xs"
                        onClick={() => retryUpload(item.file)}
                        className="text-[#007aff] hover:text-[#007aff]/80"
                      >
                        Try Again
                      </Button>
                    </div>
                  ) : (
                    <span className="text-[14px] text-ink/50 shrink-0">
                      {item.progress}%
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Tile>

      {/* Section 2 — File List Tile */}
      <Tile variant="dark" className="min-h-[400px] !items-start">
        <h2 className="text-[21px] font-semibold tracking-[0.011em] text-white/60 mb-6 uppercase text-left w-full">
          Uploaded Files
        </h2>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 w-full text-white/20">
            <p className="text-[17px]">Loading files...</p>
          </div>
        ) : files.length === 0 && uploadQueue.length === 0 ? (
          /* Empty State */
          <div className="flex flex-col items-center justify-center py-24 w-full text-white/20">
            <div className="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center mb-8">
              <FileText size={32} />
            </div>
            <p className="text-[21px] font-normal tracking-tight mb-2">
              No reference files yet
            </p>
            <p className="text-[17px] max-w-sm text-center">
              Upload a CSV, PDF, PPT, or DOCX file to begin cross-referencing
              your data.
            </p>
          </div>
        ) : files.length > 0 ? (
          /* Frosted Table */
          <div className="w-full">
            <FrostedContainer variant="white" className="rounded-xl overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-white/70 backdrop-blur-md border-b border-white/20">
                    <TableHead className="text-[14px] font-semibold text-ink">
                      File
                    </TableHead>
                    <TableHead className="text-[14px] font-semibold text-ink">
                      Status
                    </TableHead>
                    <TableHead className="w-12" />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {files.map((f: any, idx: number) => {
                    const isNew = newFileIds.has(f.id);
                    const removing = removingId === f.id;
                    return (
                      <TableRow
                        key={f.id}
                        className={cn(
                          "bg-white/40 backdrop-blur-md border-b border-white/20 hover:bg-white/60 transition-colors duration-300",
                          isNew &&
                            "animate-in fade-in slide-in-from-top-2 duration-500 fill-mode-both",
                          removing && "animate-out fade-out duration-300",
                        )}
                        style={
                          isNew
                            ? { animationDelay: `${idx * 100}ms` }
                            : undefined
                        }
                      >
                        <TableCell className="font-semibold text-white text-[17px]">
                          {f.name}
                        </TableCell>
                        <TableCell>
                          <PillChip
                            variant="status"
                            statusType={f.status || "processing"}
                          >
                            {formatStatusLabel(f.status)}
                          </PillChip>
                        </TableCell>
                        <TableCell>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setDeleteTarget(f)}
                            aria-label={`Delete ${f.name}`}
                            className="text-white/40 hover:text-[#ff3b30] h-11 w-11"
                          >
                            <Trash2 size={16} />
                          </Button>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </FrostedContainer>
          </div>
        ) : null}
      </Tile>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteTarget !== null}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
      >
        <DialogContent className="rounded-xl p-6 max-w-sm">
          <DialogHeader>
            <DialogTitle className="text-[17px] font-semibold">
              Delete {deleteTarget?.name}?
            </DialogTitle>
          </DialogHeader>
          <DialogDescription className="text-[14px] text-muted-foreground">
            This action cannot be undone.
          </DialogDescription>
          <DialogFooter>
            <DialogClose render={<Button variant="ghost">Cancel</Button>} />
            <Button variant="destructive" onClick={handleDeleteConfirm}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
