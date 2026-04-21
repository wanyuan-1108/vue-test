"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthShell } from "@/components/auth/auth-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { loginUser } from "@/lib/api";
import { saveSession } from "@/lib/auth";

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await loginUser({ email, password });
      saveSession(response.access_token, response.user);
      router.push("/");
      router.refresh();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "登录失败，请稍后再试。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell
      title="登录 DesignGen"
      description="输入账号后即可进入 AI 网页生成工作台，创建、预览并下载你的网站源码。"
      footer={
        <>
          还没有账号？ <Link href="/register" className="text-white">立即注册</Link>
        </>
      }
    >
      <form className="space-y-4" onSubmit={handleSubmit}>
        <Input type="email" placeholder="邮箱" value={email} onChange={(event) => setEmail(event.target.value)} required />
        <Input type="password" placeholder="密码" value={password} onChange={(event) => setPassword(event.target.value)} required />
        {error ? <p className="text-sm text-rose-300">{error}</p> : null}
        <Button className="w-full" size="lg" type="submit" disabled={loading}>
          {loading ? "正在登录..." : "登录"}
        </Button>
      </form>
    </AuthShell>
  );
}
