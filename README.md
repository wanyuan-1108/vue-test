

# DesignGen

DesignGen 是一个面向真实用户的 AI 网站生成平台。用户可以注册登录，在首页输入一句网站需求，进入工作台查看生成进度、实时预览页面、阅读源码，并下载完整网站文件。

## 产品能力

- 用户注册与登录
- 首页 AI 输入
- 生成完整静态网站
- 工作台实时预览
- 查看 HTML / CSS / JavaScript 源码
- 基于当前页面继续优化
- 下载网站源码 Zip

## 技术栈

### 前端

- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui
- Monaco Editor

### 后端

- FastAPI
- SQLAlchemy
- JWT 用户认证
- SQLite

### AI

- 阿里云百炼 DashScope API
- 模型：`qwen-plus`

## 页面结构

### `/`

- 顶部导航：Logo、登录/注册或用户头像
- 居中的大输入框：`Describe the website you want to build`
- 右侧工作台卡片：展示最近项目入口

### `/login`

- Email
- Password
- 登录按钮
- 注册跳转

### `/register`

- Name
- Email
- Password
- Confirm Password
- 注册按钮

### `/workspace/[projectId]`

- 顶部：项目标题、返回首页、下载源码
- 左侧：用户可读的 AI 生成进度
- 右侧：Preview / Code 双 Tab
- 底部：继续优化输入框

## 后端接口

### 认证

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### 项目

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{projectId}`
- `POST /api/projects/{projectId}/improve`
- `GET /api/projects/{projectId}/download`

## 数据表

- `users`
- `projects`
- `project_versions`
- `project_logs`
- `generation_records`（旧结构，保留但不再作为主流程）

## 本地运行

### 1. 后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 后端环境变量

复制 `backend/.env.example` 为 `backend/.env`，至少配置：

```env
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
API_PREFIX=/api
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

DATABASE_URL=sqlite:///./designgen.db

JWT_SECRET_KEY=replace-with-a-strong-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

DASHSCAPE_API_KEY=your-dashscope-api-key
DASHSCAPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCAPE_MODEL=qwen-plus
DASHSCAPE_TEMPERATURE=0.3

ZIP_OUTPUT_DIR=./generated
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

### 4. 前端环境变量

复制 `frontend/.env.example` 为 `frontend/.env.local`：

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000/api
```

### 5. 打开地址

- 前端：`http://localhost:3000`
- 后端文档：`http://localhost:8000/docs`

## 已验证

- 后端语法检查：`python -m py_compile ...`
- 前端构建：`npm run build`
- 本地接口冒烟测试：注册、获取当前用户、获取项目列表

