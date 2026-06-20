const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ─── Types ────────────────────────────────────────────────────────────────────

export type Tenant = { id: string; name: string; subdomain: string };
export type Project = { id: string; name: string; tenant_id: string };

export type Lead = {
  id: string;
  name: string;
  email: string;
  status: string;
  tenant_id: string;
  project_id: string;
  created_at: string;
};

export type ContentMaster = {
  id: string;
  title: string;
  content: string;
  status: "draft" | "approved" | "archived";
  tenant_id: string;
  project_id: string;
  created_at: string;
  updated_at: string;
};

export type ContentVariant = {
  id: string;
  master_id: string;
  platform: string;
  generated_content: string;
  created_at: string;
};

export type PromptTemplate = {
  id: string;
  name: string;
  version: string;
  system_prompt: string;
  variables: string[];
  task_type: string;
  tenant_id: string | null;
  created_at: string;
  updated_at: string;
};

export type ProjectTemplate = {
  id: string;
  name: string;
  slug: string;
  description: string;
};

// ─── CRM ──────────────────────────────────────────────────────────────────────

export const crm = {
  listLeads: (params?: { tenant_id?: string; project_id?: string }) =>
    request<Lead[]>(`/crm/leads/${params ? "?" + new URLSearchParams(params as Record<string, string>) : ""}`),

  createLead: (body: { name: string; email: string; tenant_id: string; project_id: string }) =>
    request<Lead>("/crm/leads/", { method: "POST", body: JSON.stringify(body) }),

  updateLead: (id: string, body: Partial<Pick<Lead, "name" | "email" | "status">>) =>
    request<Lead>(`/crm/leads/${id}/`, { method: "PATCH", body: JSON.stringify(body) }),

  deleteLead: (id: string) =>
    request<void>(`/crm/leads/${id}/`, { method: "DELETE" }),
};

// ─── Content Factory ──────────────────────────────────────────────────────────

export const contentFactory = {
  listMasters: (params?: { tenant_id?: string; project_id?: string; status?: string }) =>
    request<ContentMaster[]>(`/content-factory/masters/${params ? "?" + new URLSearchParams(params as Record<string, string>) : ""}`),

  createMaster: (body: { title: string; content: string; tenant_id: string; project_id: string; status?: string }) =>
    request<ContentMaster>("/content-factory/masters/", { method: "POST", body: JSON.stringify(body) }),

  updateMaster: (id: string, body: Partial<Pick<ContentMaster, "title" | "content" | "status">>) =>
    request<ContentMaster>(`/content-factory/masters/${id}/`, { method: "PATCH", body: JSON.stringify(body) }),

  deleteMaster: (id: string) =>
    request<void>(`/content-factory/masters/${id}/`, { method: "DELETE" }),

  listVariants: (masterId: string) =>
    request<ContentVariant[]>(`/content-factory/masters/${masterId}/variants/`),

  generateVariant: (masterId: string, platform: string, prompt_template_id?: string) =>
    request<ContentVariant>(`/content-factory/masters/${masterId}/variants/generate/`, {
      method: "POST",
      body: JSON.stringify({ platform, ...(prompt_template_id ? { prompt_template_id } : {}) }),
    }),

  listPromptTemplates: (tenant_id?: string) =>
    request<PromptTemplate[]>(`/content-factory/prompt-templates/${tenant_id ? `?tenant_id=${tenant_id}` : ""}`),
};

// ─── Tenants ──────────────────────────────────────────────────────────────────

export const tenants = {
  listTemplates: () => request<ProjectTemplate[]>("/tenants/templates/"),

  applyTemplate: (project_id: string, template_slug: string) =>
    request<Project>(`/tenants/projects/${project_id}/apply-template/${template_slug}/`, { method: "POST" }),
};
