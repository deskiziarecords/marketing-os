"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { tenants } from "@/lib/api";
import type { ProjectTemplate } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter,
} from "@/components/ui/dialog";
import { Layers, CheckCircle } from "lucide-react";

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<ProjectTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ProjectTemplate | null>(null);
  const [projectId, setProjectId] = useState("");
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState<string | null>(null);

  useEffect(() => {
    tenants.listTemplates().then(setTemplates).finally(() => setLoading(false));
  }, []);

  const handleApply = async () => {
    if (!selected || !projectId.trim()) return toast.error("Enter a project ID");
    setApplying(true);
    try {
      await tenants.applyTemplate(projectId.trim(), selected.slug);
      setApplied(selected.slug);
      toast.success(`Template "${selected.name}" applied to project!`);
      setSelected(null);
      setProjectId("");
    } catch (e: unknown) {
      toast.error(String(e));
    } finally {
      setApplying(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Project Templates</h1>
        <p className="text-gray-500 text-sm mt-1">
          Apply an industry-specific template to instantly configure pipelines, AI prompts, and automations.
        </p>
      </div>

      {loading ? (
        <p className="text-gray-400">Loading templates…</p>
      ) : templates.length === 0 ? (
        <Card className="text-center py-16">
          <CardContent>
            <p className="text-gray-400">No templates found. Run <code className="text-xs bg-gray-100 px-1 rounded">python scripts/seed_templates.py</code> to seed them.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {templates.map((t) => (
            <Card key={t.id} className="flex flex-col">
              <CardHeader className="pb-3">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-purple-50 text-purple-600 shrink-0">
                    {applied === t.slug
                      ? <CheckCircle className="h-5 w-5 text-green-600" />
                      : <Layers className="h-5 w-5" />}
                  </div>
                  <div>
                    <CardTitle className="text-base leading-tight">{t.name}</CardTitle>
                    <code className="text-xs text-gray-400 mt-0.5 block">{t.slug}</code>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col gap-4">
                <CardDescription className="text-sm">{t.description}</CardDescription>
                <Button
                  size="sm"
                  variant="outline"
                  className="mt-auto"
                  onClick={() => setSelected(t)}
                >
                  Apply to Project
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={!!selected} onOpenChange={(o) => !o && setSelected(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Apply — {selected?.name}</DialogTitle>
          </DialogHeader>
          <div className="py-2 space-y-3">
            <p className="text-sm text-gray-500">
              This will clone all AI prompts from this template into the project&apos;s tenant.
            </p>
            <div className="space-y-1.5">
              <Label>Project ID</Label>
              <Input
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setSelected(null)}>Cancel</Button>
            <Button onClick={handleApply} disabled={applying}>
              {applying ? "Applying…" : "Apply Template"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
