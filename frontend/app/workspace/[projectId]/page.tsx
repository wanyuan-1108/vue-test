import { redirect } from "next/navigation";

export default function LegacyWorkspacePage({ params }: { params: { projectId: string } }) {
  redirect(`/project/${params.projectId}`);
}
