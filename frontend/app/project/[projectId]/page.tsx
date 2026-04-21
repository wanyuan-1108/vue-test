import { ProjectScreen } from "@/components/project/project-screen";

export default function ProjectPage({ params }: { params: { projectId: string } }) {
  return <ProjectScreen projectId={params.projectId} />;
}
