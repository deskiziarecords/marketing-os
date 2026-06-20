"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { crm, contentFactory } from "@/lib/api";
import type { Lead, ContentMaster } from "@/lib/api";
import { Users, FileText, CheckCircle, Clock } from "lucide-react";

export default function DashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [masters, setMasters] = useState<ContentMaster[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([crm.listLeads(), contentFactory.listMasters()])
      .then(([l, m]) => { setLeads(l); setMasters(m); })
      .finally(() => setLoading(false));
  }, []);

  const approved = masters.filter((m) => m.status === "approved").length;
  const drafts = masters.filter((m) => m.status === "draft").length;

  const stats = [
    { label: "Total Leads", value: leads.length, icon: Users, color: "text-blue-500" },
    { label: "Content Masters", value: masters.length, icon: FileText, color: "text-purple-500" },
    { label: "Approved Content", value: approved, icon: CheckCircle, color: "text-green-500" },
    { label: "Drafts", value: drafts, icon: Clock, color: "text-yellow-500" },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">Overview of your Marketing OS</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <Card key={label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">{label}</CardTitle>
              <Icon className={`h-4 w-4 ${color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {loading ? <span className="text-gray-300">—</span> : value}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recent Leads</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-gray-400 text-sm">Loading...</p>
            ) : leads.length === 0 ? (
              <p className="text-gray-400 text-sm">No leads yet.</p>
            ) : (
              <ul className="space-y-2">
                {leads.slice(0, 5).map((l) => (
                  <li key={l.id} className="flex items-center justify-between text-sm">
                    <span className="font-medium">{l.name}</span>
                    <span className="text-xs text-gray-400 capitalize">{l.status}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recent Content</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-gray-400 text-sm">Loading...</p>
            ) : masters.length === 0 ? (
              <p className="text-gray-400 text-sm">No content yet.</p>
            ) : (
              <ul className="space-y-2">
                {masters.slice(0, 5).map((m) => (
                  <li key={m.id} className="flex items-center justify-between text-sm">
                    <span className="font-medium truncate max-w-[200px]">{m.title}</span>
                    <span className={`text-xs capitalize px-2 py-0.5 rounded-full ${
                      m.status === "approved" ? "bg-green-100 text-green-700"
                        : m.status === "archived" ? "bg-gray-100 text-gray-500"
                        : "bg-yellow-100 text-yellow-700"
                    }`}>{m.status}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
