import { TEMPLATE_PREFERENCE_GROUPS, hasAnyTemplatePreferences, type TemplatePreferenceKey, type UserTemplatePreferences } from "@/lib/template-preferences";

type TemplateTagValue = string | string[] | undefined;

export type TemplateIdea = {
  id: string;
  title: string;
  prompt: string;
  description: string;
  badge?: string;
  industry?: TemplateTagValue;
  industries?: TemplateTagValue;
  purpose?: TemplateTagValue;
  purposes?: TemplateTagValue;
  style?: TemplateTagValue;
  styles?: TemplateTagValue;
  targetUser?: TemplateTagValue;
  targetUsers?: TemplateTagValue;
};

export type RecommendedTemplate = TemplateIdea & {
  recommendationScore: number;
  matchedGroups: Array<{
    key: TemplatePreferenceKey;
    label: string;
    value: string;
  }>;
};

const MATCH_WEIGHTS: Record<TemplatePreferenceKey, number> = {
  industry: 4,
  purpose: 3,
  style: 2,
  targetUser: 2,
};

export const TEMPLATE_LIBRARY: TemplateIdea[] = [
  {
    id: "real-estate-luxury",
    title: "高端房地产落地页",
    prompt: "创建一个高端房地产落地页",
    description: "强调项目价值、空间质感和高净值转化，适合品牌展示与营销获客。",
    badge: "热销模板",
    industries: ["房地产", "企业官网"],
    purposes: ["营销落地页", "展示型网站", "品牌官网"],
    styles: ["高端大气", "商务风"],
    targetUsers: ["商家", "小微企业", "大型企业"],
  },
  {
    id: "designer-portfolio",
    title: "设计师作品集",
    prompt: "设计一个大胆有辨识度的产品设计师作品集",
    description: "突出案例展示、个人品牌与作品叙事，适合个人展示和接单转化。",
    badge: "作品集",
    industries: ["摄影设计", "个人博客"],
    purposes: ["展示型网站", "博客内容发布", "品牌官网"],
    styles: ["简约风", "高端大气"],
    targetUsers: ["设计师", "个人用户"],
  },
  {
    id: "ai-saas-home",
    title: "AI SaaS 官网",
    prompt: "制作一个包含定价和常见问题的 AI SaaS 首页",
    description: "覆盖产品亮点、定价方案和 FAQ，适合科技产品的品牌官网与转化首页。",
    badge: "热门模板",
    industries: ["科技互联网", "企业官网"],
    purposes: ["品牌官网", "营销落地页", "展示型网站"],
    styles: ["科技感", "简约风", "暗黑风"],
    targetUsers: ["开发者", "小微企业", "大型企业"],
  },
  {
    id: "restaurant-reservation",
    title: "餐饮预约官网",
    prompt: "生成一个带菜单展示和门店预约的餐饮品牌官网",
    description: "适合餐饮品牌展示菜品、门店信息和预约入口，提升品牌质感与转化率。",
    badge: "门店推荐",
    industries: ["餐饮美食"],
    purposes: ["品牌官网", "预约系统", "展示型网站"],
    styles: ["清新风", "高端大气"],
    targetUsers: ["商家", "个人用户"],
  },
  {
    id: "education-course",
    title: "教育培训课程页",
    prompt: "搭建一个强调课程体系和报名转化的教育培训官网",
    description: "适合课程介绍、讲师展示和报名引导，适配教育机构和培训品牌。",
    badge: "课程模板",
    industries: ["教育培训"],
    purposes: ["展示型网站", "营销落地页", "预约系统"],
    styles: ["简约风", "商务风", "清新风"],
    targetUsers: ["学生", "个人用户", "小微企业"],
  },
  {
    id: "retail-commerce",
    title: "零售品牌商城",
    prompt: "制作一个突出商品推荐和促销活动的在线商城首页",
    description: "适合商品售卖、活动曝光和高频转化场景，能快速搭出标准商城首页。",
    badge: "商城模板",
    industries: ["电商零售"],
    purposes: ["在线商城", "营销落地页"],
    styles: ["扁平化", "简约风"],
    targetUsers: ["商家", "个人用户"],
  },
  {
    id: "medical-booking",
    title: "医疗健康预约站",
    prompt: "设计一个包含医生介绍和预约入口的医疗健康官网",
    description: "适合诊所、医疗服务机构展示服务内容与预约流程，风格更可信稳重。",
    badge: "预约推荐",
    industries: ["医疗健康"],
    purposes: ["预约系统", "品牌官网", "展示型网站"],
    styles: ["商务风", "简约风"],
    targetUsers: ["个人用户", "大型企业"],
  },
  {
    id: "travel-hotel",
    title: "旅游酒店预订页",
    prompt: "制作一个适合酒店民宿展示和预订的旅游官网",
    description: "适合展示房型、行程亮点和预订入口，适配酒店、民宿和旅游品牌。",
    badge: "假日模板",
    industries: ["旅游酒店"],
    purposes: ["预约系统", "营销落地页", "展示型网站"],
    styles: ["高端大气", "清新风"],
    targetUsers: ["个人用户", "商家"],
  },
  {
    id: "tech-recruitment",
    title: "科技招聘官网",
    prompt: "设计一个适合科技公司招聘和团队展示的官网",
    description: "适合团队介绍、岗位发布和雇主品牌建设，适配科技公司招聘页。",
    badge: "招聘模板",
    industries: ["科技互联网", "企业官网"],
    purposes: ["招聘网站", "品牌官网", "展示型网站"],
    styles: ["科技感", "商务风", "暗黑风"],
    targetUsers: ["开发者", "大型企业", "小微企业"],
  },
  {
    id: "gaming-community",
    title: "游戏社区论坛",
    prompt: "创建一个适合玩家交流和活动运营的游戏社区论坛",
    description: "适合做玩家内容聚合、公告活动和社区氛围展示，强化互动感。",
    badge: "社区模板",
    industries: ["游戏娱乐"],
    purposes: ["社区论坛", "展示型网站"],
    styles: ["暗黑风", "卡通风"],
    targetUsers: ["学生", "个人用户"],
  },
];

function toTagArray(value: TemplateTagValue) {
  if (Array.isArray(value)) {
    return value;
  }

  if (typeof value === "string" && value.trim()) {
    return [value.trim()];
  }

  return [] as string[];
}

function getTemplateTagValues(template: TemplateIdea, key: TemplatePreferenceKey) {
  if (key === "industry") {
    return [...toTagArray(template.industries), ...toTagArray(template.industry)];
  }

  if (key === "purpose") {
    return [...toTagArray(template.purposes), ...toTagArray(template.purpose)];
  }

  if (key === "style") {
    return [...toTagArray(template.styles), ...toTagArray(template.style)];
  }

  return [...toTagArray(template.targetUsers), ...toTagArray(template.targetUser)];
}

export function getRecommendedTemplates(
  preferences: UserTemplatePreferences,
  templates: TemplateIdea[] = TEMPLATE_LIBRARY,
  limit = 4
): RecommendedTemplate[] {
  const hasSelectedTags = hasAnyTemplatePreferences(preferences);
  const preferenceGroupsByKey = Object.fromEntries(TEMPLATE_PREFERENCE_GROUPS.map((group) => [group.key, group]));

  const rankedTemplates = templates
    .map((template, index) => {
      const matchedGroups = TEMPLATE_PREFERENCE_GROUPS.reduce<RecommendedTemplate["matchedGroups"]>((matches, group) => {
        const selectedValue = preferences[group.key];
        if (!selectedValue) {
          return matches;
        }

        const templateTagValues = getTemplateTagValues(template, group.key);
        if (!templateTagValues.includes(selectedValue)) {
          return matches;
        }

        matches.push({
          key: group.key,
          label: preferenceGroupsByKey[group.key]?.label ?? group.key,
          value: selectedValue,
        });

        return matches;
      }, []);

      const recommendationScore = matchedGroups.reduce((score, match) => score + MATCH_WEIGHTS[match.key], 0);

      return {
        ...template,
        recommendationScore,
        matchedGroups,
        index,
      };
    })
    .sort((left, right) => right.recommendationScore - left.recommendationScore || left.index - right.index);

  const positiveMatches = rankedTemplates.filter((template) => template.recommendationScore > 0);
  const fallbackMatches = rankedTemplates.filter((template) => template.recommendationScore === 0);
  const selectedTemplates = hasSelectedTags ? [...positiveMatches, ...fallbackMatches].slice(0, limit) : fallbackMatches.slice(0, limit);

  return selectedTemplates.map(({ index, ...template }) => template);
}
