const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const isFormData = options?.body instanceof FormData;
  const res = await fetch(`${API_BASE}${path}`, {
    headers: isFormData ? {} : { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err);
  }
  return res.json();
}

async function downloadBlob(path: string, data: any, filename: string = "resultado.xlsx"): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 100);
}

const uploadWithProgress = (
  file: File,
  onProgress: (percent: number) => void
): Promise<any> => {
  return new Promise((resolve, reject) => {
    const form = new FormData();
    form.append("file", file);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE}/api/crossref/upload`);
    xhr.upload.onprogress = (e: ProgressEvent) => {
      if (e.lengthComputable) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(xhr.responseText));
      }
    };
    xhr.onerror = () => reject(new Error("Upload failed"));
    xhr.onabort = () => reject(new Error("Upload cancelled"));
    xhr.send(form);
  });
};

export const api = {
  ingest: {
    upload: (files: File[]) => {
      const form = new FormData();
      files.forEach((f) => form.append("files", f));
      return request<{ files: string[]; count: number }>("/api/ingest/upload", {
        method: "POST",
        body: form,
      });
    },
  },
  templates: {
    list: () => request<any[]>("/api/templates/"),
    get: (id: string) => request<any>(`/api/templates/${id}`),
    create: (data: any) =>
      request<any>("/api/templates/", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: any) =>
      request<any>(`/api/templates/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<any>(`/api/templates/${id}`, { method: "DELETE" }),
  },
  extraction: {
    extract: (data: any) =>
      request<any[]>("/api/extraction/", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    batch: (data: any) =>
      request<any>("/api/extraction/extract/batch", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
  rules: {
    list: () => request<any[]>("/api/rules/"),
    create: (data: any) =>
      request<any>("/api/rules/", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    evaluate: (data: any) =>
      request<any>("/api/rules/evaluate", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
  export: {
    excel: (data: any) => downloadBlob("/api/export/", data),
  },
  crossref: {
    upload: (file: File) => {
      const form = new FormData();
      form.append("file", file);
      return request<any>("/api/crossref/upload", {
        method: "POST",
        body: form,
      });
    },
    list: () => request<any[]>("/api/crossref/files"),
    get: (id: string) => request<any>(`/api/crossref/files/${id}`),
    delete: (id: string) =>
      request<any>(`/api/crossref/files/${id}`, { method: "DELETE" }),
  },
};

export { uploadWithProgress };
