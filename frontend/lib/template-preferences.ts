export type TemplatePreferenceKey = "industry" | "purpose" | "style" | "targetUser";

export type UserTemplatePreferences = {
  industry: string;
  purpose: string;
  style: string;
  targetUser: string;
};

export type TemplatePreferenceGroup = {
  key: TemplatePreferenceKey;
  label: string;
  description: string;
  options: string[];
};

const TEMPLATE_PREFERENCES_STORAGE_KEY = "designgen_template_preferences";

export const TEMPLATE_PREFERENCE_GROUPS: TemplatePreferenceGroup[] = [
  {
    key: "industry",
    label: "行业类型",
    description: "告诉我们你最常服务的行业方向。",
    options: ["餐饮美食", "教育培训", "电商零售", "企业官网", "个人博客", "摄影设计", "医疗健康", "房地产", "旅游酒店", "科技互联网", "游戏娱乐"],
  },
  {
    key: "purpose",
    label: "网站用途",
    description: "你更常想做哪一类网站？",
    options: ["展示型网站", "在线商城", "品牌官网", "预约系统", "博客内容发布", "营销落地页", "招聘网站", "社区论坛", "数据展示大屏"],
  },
  {
    key: "style",
    label: "设计风格",
    description: "先选一个最贴近你审美偏好的方向。",
    options: ["简约风", "科技感", "商务风", "卡通风", "高端大气", "扁平化", "暗黑风", "清新风"],
  },
  {
    key: "targetUser",
    label: "目标用户",
    description: "帮助系统判断更适合谁来使用这个站点。",
    options: ["个人用户", "学生", "商家", "小微企业", "大型企业", "开发者", "设计师"],
  },
];

const EMPTY_TEMPLATE_PREFERENCES: UserTemplatePreferences = {
  industry: "",
  purpose: "",
  style: "",
  targetUser: "",
};

function normalizeTemplatePreferences(preferences?: Partial<UserTemplatePreferences> | null): UserTemplatePreferences {
  return {
    industry: preferences?.industry?.trim() ?? "",
    purpose: preferences?.purpose?.trim() ?? "",
    style: preferences?.style?.trim() ?? "",
    targetUser: preferences?.targetUser?.trim() ?? "",
  };
}

function readTemplatePreferencesMap() {
  if (typeof window === "undefined") {
    return {} as Record<string, UserTemplatePreferences>;
  }

  const raw = window.localStorage.getItem(TEMPLATE_PREFERENCES_STORAGE_KEY);
  if (!raw) {
    return {} as Record<string, UserTemplatePreferences>;
  }

  try {
    const parsed = JSON.parse(raw) as Record<string, Partial<UserTemplatePreferences>>;
    return Object.fromEntries(Object.entries(parsed).map(([userId, preferences]) => [userId, normalizeTemplatePreferences(preferences)]));
  } catch {
    return {} as Record<string, UserTemplatePreferences>;
  }
}

function writeTemplatePreferencesMap(preferencesMap: Record<string, UserTemplatePreferences>) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(TEMPLATE_PREFERENCES_STORAGE_KEY, JSON.stringify(preferencesMap));
}

export function createEmptyTemplatePreferences(): UserTemplatePreferences {
  return { ...EMPTY_TEMPLATE_PREFERENCES };
}

export function getUserTemplatePreferences(userId?: string | null) {
  if (!userId) {
    return createEmptyTemplatePreferences();
  }

  const preferencesMap = readTemplatePreferencesMap();
  return preferencesMap[userId] ?? createEmptyTemplatePreferences();
}

export function saveUserTemplatePreferences(userId: string, preferences: Partial<UserTemplatePreferences>) {
  if (!userId) {
    return;
  }

  const preferencesMap = readTemplatePreferencesMap();
  preferencesMap[userId] = normalizeTemplatePreferences(preferences);
  writeTemplatePreferencesMap(preferencesMap);
}

export function hasAnyTemplatePreferences(preferences: UserTemplatePreferences) {
  return Object.values(preferences).some((value) => value.trim().length > 0);
}

export function hasCompleteTemplatePreferences(preferences: UserTemplatePreferences) {
  return Object.values(preferences).every((value) => value.trim().length > 0);
}
