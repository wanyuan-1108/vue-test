"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthShell } from "@/components/auth/auth-shell";
import { TemplatePreferenceEditor } from "@/components/projects/template-preference-editor";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { registerUser } from "@/lib/api";
import { saveSession } from "@/lib/auth";
import { createEmptyTemplatePreferences, saveUserTemplatePreferences } from "@/lib/template-preferences";

export function RegisterForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [templatePreferences, setTemplatePreferences] = useState(createEmptyTemplatePreferences());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("两次输入的密码不一致。");
      return;
    }

    setLoading(true);

    try {
      const response = await registerUser({ name, email, password });
      saveSession(response.access_token, response.user);
      saveUserTemplatePreferences(response.user.id, templatePreferences);
      router.push("/");
      router.refresh();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "注册失败，请稍后再试。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell
      title="创建你的账号"
      description="注册后即可保存项目、持续优化页面，并根据你的标签偏好获得更精准的模板推荐。"
      panelClassName="max-w-4xl"
      footer={
        <>
          已有账号？<Link href="/login" className="text-white">去登录</Link>
        </>
      }
    >
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div className="grid gap-4 md:grid-cols-2">
          <Input placeholder="昵称" value={name} onChange={(event) => setName(event.target.value)} required />
          <Input type="email" placeholder="邮箱" value={email} onChange={(event) => setEmail(event.target.value)} required />
          <Input type="password" placeholder="密码" value={password} onChange={(event) => setPassword(event.target.value)} required />
          <Input
            type="password"
            placeholder="确认密码"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            required
          />
        </div>

        <TemplatePreferenceEditor
          value={templatePreferences}
          onChange={setTemplatePreferences}
          title="兴趣标签"
          description="这些偏好会直接影响模板推荐结果。现在填写，注册后也可以在模板区继续调整。"
        />

        {error ? <p className="text-sm text-rose-300">{error}</p> : null}

        <Button className="w-full" size="lg" type="submit" disabled={loading}>
          {loading ? "正在创建账号..." : "注册"}
        </Button>
      </form>
    </AuthShell>
  );
}
