"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { contentFactory } from "@/lib/api";
import type { ContentMaster, ContentVariant } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter,
} from "@/components/ui/dialog";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import { Plus, Wand2, Trash2, ChevronDown, ChevronRight } from "lucide-react";

const DEMO_TENANT = "00000000-0000-0000-0000-000000000001";
const DEMO_PROJECT = "00000000-0000-0000-0000-000000000002";

const PLATFORMS = ["instagram", "linkedin", "tiktok", "twitter", "facebook", "blog", "email"];

const STATUS_COLORS: Record<string, string> = {
  draft: "bg-yellow-100 text-yellow-700",
  approved: "bg-green-100 text-green-700",
  archived: "bg-gray-100 text-gray-500",
};

export default function ContentPage() {
  const [masters, setMasters] = useState<ContentMaster[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ title: "", content: "", status: "draft" });
  const [saving, setSaving] = useState(false);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [variants, setVariants] = useState<Record<string, ContentVariant[]>>({});
  const [generating, setGenerating] = useState<string | null>(null);
  const [genPlatform, setGenPlatform] = useState("instagram");

  const load = () =>
    contentFactory.listMasters().then(setMasters).finally(() => setLoading(false));

  useEffect(() => { load(); }, []);

  const toggleExpand = async (master: ContentMaster) => {
    if (expanded === master.id) { setExpanded(null); return; }
    setExpanded(master.id);
    if (!variants[master.id]) {
      const v = await contentFactory.listVariants(master.id);
      setVariants((prev) => ({ ...prev, [master.id]: v }));
    }
  };

  const handleCreate = async () => {
    if (!form.title || !form.content) return toast.error("Title and content required");
    setSaving(true);
    try {
      await contentFactory.createMaster({ ...form, tenant_id: DEMO_TENANT, project_id: DEMO_PROJECT });
      toast.success("Content master created");
      setShowCreate(false);
      setForm({ title: "", content: "", status: "draft" });
      load();
    } catch (e: unknown) {
      toast.error(String(e));
    } finally {
      setSaving(false);
    }
  };

  const handleApprove = async (master: ContentMaster) => {
    try {
      await contentFactory.updateMaster(master.id, { status: "approved" });
      toast.success("Approved");
      load();
    } catch (e: unknown) {
      toast.error(String(e));
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this content master and all its variants?")) return;
    try {
      await contentFactory.deleteMaster(id);
      toast.success("Deleted");
      load();
    } catch (e: unknown) {
      toast.error(String(e));
    }
  };

  const handleGenerate = async (master: ContentMaster) => {
    setGenerating(master.id);
    try {
      const v = await contentFactory.generateVariant(master.id, genPlatform);
      toast.success(`${genPlatform} variant generated!`);
      setVariants((prev) => ({ ...prev, [master.id]: [...(prev[master.id] ?? []), v] }));
      setExpanded(master.id);
    } catch (e: unknown) {
      toast.error(String(e));
    } finally {
      setGenerating(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Content Factory</h1>
          <p className="text-gray-500 text-sm mt-1">{masters.length} content masters</p>
        </div>
        <Button onClick={() => setShowCreate(true)} size="sm">
          <Plus className="h-4 w-4 mr-1" /> New Content
        </Button>
      </div>

      {loading ? (
        <p className="text-gray-400">Loading...</p>
      ) : masters.length === 0 ? (
        <Card className="text-center py-16">
          <CardContent>
            <p className="text-gray-400">No content yet. Create your first content master.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {masters.map((m) => (
            <Card key={m.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2 min-w-0">
                    <button onClick={() => toggleExpand(m)} className="shrink-0 text-gray-400 hover:text-gray-700">
                      {expanded === m.id ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                    </button>
                    <CardTitle className="text-base truncate">{m.title}</CardTitle>
                    <Badge className={STATUS_COLORS[m.status]}>{m.status}</Badge>
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    <Select value={genPlatform} onValueChange={(v) => v && setGenPlatform(v)}>
                      <SelectTrigger className="h-8 w-32 text-xs">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {PLATFORMS.map((p) => <SelectItem key={p} value={p}>{p}</SelectItem>)}
                      </SelectContent>
                    </Select>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleGenerate(m)}
                      disabled={generating === m.id}
                      className="h-8 text-xs"
                    >
                      <Wand2 className="h-3.5 w-3.5 mr-1" />
                      {generating === m.id ? "Generating…" : "Generate"}
                    </Button>
                    {m.status === "draft" && (
                      <Button size="sm" variant="outline" className="h-8 text-xs text-green-600 border-green-200 hover:bg-green-50" onClick={() => handleApprove(m)}>
                        Approve
                      </Button>
                    )}
                    <Button size="icon" variant="ghost" className="h-8 w-8" onClick={() => handleDelete(m.id)}>
                      <Trash2 className="h-3.5 w-3.5 text-red-400" />
                    </Button>
                  </div>
                </div>
              </CardHeader>

              {expanded === m.id && (
                <CardContent className="pt-0 space-y-4">
                  <div className="rounded-md bg-gray-50 p-3 text-sm text-gray-700 whitespace-pre-wrap border">
                    {m.content}
                  </div>

                  <div>
                    <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
                      Variants ({(variants[m.id] ?? []).length})
                    </p>
                    {(variants[m.id] ?? []).length === 0 ? (
                      <p className="text-sm text-gray-400">No variants yet. Use the Generate button above.</p>
                    ) : (
                      <div className="space-y-2">
                        {(variants[m.id] ?? []).map((v) => (
                          <div key={v.id} className="rounded-md border bg-white p-3">
                            <div className="flex items-center gap-2 mb-1.5">
                              <Badge variant="outline" className="text-xs capitalize">{v.platform}</Badge>
                              <span className="text-xs text-gray-400">{new Date(v.created_at).toLocaleString()}</span>
                            </div>
                            <p className="text-sm text-gray-700 whitespace-pre-wrap">{v.generated_content}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}

      <Dialog open={showCreate} onOpenChange={setShowCreate}>
        <DialogContent className="max-w-lg">
          <DialogHeader><DialogTitle>New Content Master</DialogTitle></DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-1.5">
              <Label>Title</Label>
              <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="10 Tips de Marketing Digital" />
            </div>
            <div className="space-y-1.5">
              <Label>Base Content</Label>
              <Textarea
                value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })}
                placeholder="Write your source-of-truth content here…"
                rows={6}
              />
            </div>
            <div className="space-y-1.5">
              <Label>Status</Label>
              <Select value={form.status} onValueChange={(v) => v && setForm({ ...form, status: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="draft">Draft</SelectItem>
                  <SelectItem value="approved">Approved</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreate(false)}>Cancel</Button>
            <Button onClick={handleCreate} disabled={saving}>{saving ? "Saving…" : "Create"}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
