from __future__ import annotations

from typing import Dict, List


BRAND_TO_INDUSTRY: Dict[str, str] = {
    "mcdonalds": "burger_fast_food",
    "starbucks": "coffee_brand",
    "apple": "tech_product_brand",
    "nike": "fashion_brand",
    "tesla": "tech_product_brand",
}


INDUSTRY_KEYWORDS: Dict[str, List[str]] = {
    "burger_fast_food": [
        "麦当劳",
        "汉堡",
        "薯条",
        "炸鸡",
        "鸡块",
        "快餐",
        "burger",
        "fries",
        "fried chicken",
    ],
    "coffee_brand": [
        "咖啡",
        "拿铁",
        "卡布奇诺",
        "冷萃",
        "咖啡馆",
        "cafe",
        "coffee",
        "latte",
    ],
    "dessert_brand": [
        "甜品",
        "蛋糕",
        "马卡龙",
        "冰淇淋",
        "甜甜圈",
        "dessert",
        "cake",
        "donut",
    ],
    "fashion_brand": [
        "服装",
        "潮流",
        "时尚",
        "穿搭",
        "球鞋",
        "外套",
        "fashion",
        "clothing",
        "nike",
    ],
    "tech_product_brand": [
        "科技",
        "数码",
        "电子产品",
        "手机",
        "耳机",
        "电脑",
        "saas",
        "app",
        "dashboard",
        "tech",
    ],
    "restaurant_brand": [
        "餐厅",
        "餐饮",
        "牛排",
        "料理",
        "美食",
        "restaurant",
        "dining",
    ],
}


INDUSTRY_LABELS: Dict[str, str] = {
    "burger_fast_food": "汉堡快餐品牌",
    "coffee_brand": "咖啡品牌",
    "dessert_brand": "甜品品牌",
    "fashion_brand": "时尚服饰品牌",
    "tech_product_brand": "科技产品品牌",
    "restaurant_brand": "餐饮品牌",
    "brand": "品牌官网",
}


PRODUCT_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    "burger_fast_food": [
        {
            "name": "经典牛肉汉堡",
            "description": "厚切牛肉饼搭配融化芝士与爽脆生菜，层次饱满，适合做品牌主推单品。",
            "price": "¥32",
            "image_query": "burger",
            "tag": "招牌热卖",
            "meta": "高人气单品",
        },
        {
            "name": "黄金薯条",
            "description": "外脆内软，适合作为组合套餐搭配，强化快餐品牌的经典记忆点。",
            "price": "¥15",
            "image_query": "french fries",
            "tag": "经典搭配",
            "meta": "必点小食",
        },
        {
            "name": "香辣炸鸡",
            "description": "高饱和视觉与酥脆口感兼具，适合在产品卡片区打造冲击力。",
            "price": "¥28",
            "image_query": "fried chicken",
            "tag": "人气推荐",
            "meta": "门店热销",
        },
        {
            "name": "鸡块拼盘",
            "description": "适合家庭与多人分享场景，帮助页面形成丰富套餐层次。",
            "price": "¥22",
            "image_query": "chicken nuggets",
            "tag": "分享装",
            "meta": "高转化套餐",
        },
        {
            "name": "冰爽可乐",
            "description": "强化快餐套餐的完整感，让画面更接近真实商业官网。",
            "price": "¥10",
            "image_query": "cola drink",
            "tag": "清爽加购",
            "meta": "组合推荐",
        },
    ],
    "coffee_brand": [
        {
            "name": "美式咖啡",
            "description": "干净利落的风味适合作为咖啡品牌首页的经典入门款。",
            "price": "¥22",
            "image_query": "americano coffee",
            "tag": "经典款",
            "meta": "日常首选",
        },
        {
            "name": "拿铁咖啡",
            "description": "奶香与咖啡香平衡顺滑，适合年轻用户与大众口味。",
            "price": "¥28",
            "image_query": "latte",
            "tag": "人气王",
            "meta": "高复购单品",
        },
        {
            "name": "卡布奇诺",
            "description": "绵密奶泡营造温暖精致气质，适合搭配品牌故事区出现。",
            "price": "¥30",
            "image_query": "cappuccino",
            "tag": "精品推荐",
            "meta": "门店精选",
        },
        {
            "name": "摩卡咖啡",
            "description": "巧克力与咖啡风味交融，视觉表现浓郁，适合做促销活动图。",
            "price": "¥32",
            "image_query": "mocha coffee",
            "tag": "甜感风味",
            "meta": "限定主推",
        },
        {
            "name": "冷萃咖啡",
            "description": "清爽克制的视觉与口感，适合现代感与高级感风格页面。",
            "price": "¥30",
            "image_query": "cold brew coffee",
            "tag": "清爽特调",
            "meta": "夏日推荐",
        },
    ],
    "dessert_brand": [
        {
            "name": "奶油蛋糕",
            "description": "轻盈奶香与柔软口感兼备，适合打造甜品官网的招牌视觉。",
            "price": "¥36",
            "image_query": "cake",
            "tag": "招牌甜品",
            "meta": "节日热卖",
        },
        {
            "name": "马卡龙礼盒",
            "description": "色彩丰富、视觉高级，适合用于品牌精品区与礼赠场景。",
            "price": "¥48",
            "image_query": "macaron",
            "tag": "礼盒推荐",
            "meta": "高颜值系列",
        },
        {
            "name": "香草冰淇淋",
            "description": "适合用大图营造清爽感，让页面氛围更丰富真实。",
            "price": "¥20",
            "image_query": "ice cream",
            "tag": "清爽系列",
            "meta": "夏日人气",
        },
        {
            "name": "甜甜圈",
            "description": "具备可爱和缤纷的视觉特征，适合强化品牌趣味性。",
            "price": "¥18",
            "image_query": "donut",
            "tag": "热门单品",
            "meta": "下午茶搭配",
        },
        {
            "name": "布朗尼",
            "description": "浓郁巧克力风味突出，适合做口味层次型内容展示。",
            "price": "¥24",
            "image_query": "brownie dessert",
            "tag": "浓郁风味",
            "meta": "门店精选",
        },
    ],
    "fashion_brand": [
        {
            "name": "品牌连帽卫衣",
            "description": "宽松版型和舒适面料适合做年轻化街头风品牌主推款。",
            "price": "¥299",
            "image_query": "hoodie fashion",
            "tag": "新品上架",
            "meta": "街头风格",
        },
        {
            "name": "工装外套",
            "description": "轮廓感利落，适合展示品牌层次化穿搭方案。",
            "price": "¥499",
            "image_query": "jacket fashion",
            "tag": "造型推荐",
            "meta": "秋冬精选",
        },
        {
            "name": "经典白色球鞋",
            "description": "百搭基础款适合承接大多数时尚品牌官网的转化需求。",
            "price": "¥399",
            "image_query": "white sneakers",
            "tag": "热销款",
            "meta": "穿搭必备",
        },
    ],
    "tech_product_brand": [
        {
            "name": "旗舰手机",
            "description": "高性能芯片与沉浸屏幕带来强科技感，适合作为主打产品。",
            "price": "¥5999",
            "image_query": "smartphone",
            "tag": "旗舰新品",
            "meta": "核心产品",
        },
        {
            "name": "降噪耳机",
            "description": "强调通勤、音质与续航，适合用于推荐区强化品牌生态。",
            "price": "¥1299",
            "image_query": "wireless headphones",
            "tag": "人气配件",
            "meta": "生态联动",
        },
        {
            "name": "智能手表",
            "description": "适合呈现健康、效率与互联能力，增强科技官网的真实感。",
            "price": "¥1899",
            "image_query": "smart watch",
            "tag": "智能新品",
            "meta": "便携设备",
        },
    ],
    "restaurant_brand": [
        {
            "name": "主厨招牌套餐",
            "description": "通过完整套餐展示餐厅的风味体系与视觉层次。",
            "price": "¥128",
            "image_query": "restaurant meal",
            "tag": "主厨推荐",
            "meta": "高客单组合",
        },
        {
            "name": "当季特色主菜",
            "description": "适合用大图表现摆盘与质感，增强餐厅官网的可信度。",
            "price": "¥88",
            "image_query": "restaurant main course",
            "tag": "当季限定",
            "meta": "到店热卖",
        },
        {
            "name": "手工甜品",
            "description": "补充用餐后的甜点体验，让页面内容更完整丰富。",
            "price": "¥36",
            "image_query": "restaurant dessert",
            "tag": "餐后推荐",
            "meta": "精致收尾",
        },
    ],
    "brand": [
        {
            "name": "核心产品 A",
            "description": "用于承接品牌官网的产品展示区，保持现代中文商业语气。",
            "price": "¥199",
            "image_query": "brand product",
            "tag": "主推",
            "meta": "品牌精选",
        },
        {
            "name": "核心产品 B",
            "description": "适合在通用品牌场景下展示卖点、功能和转化入口。",
            "price": "¥299",
            "image_query": "premium product",
            "tag": "推荐",
            "meta": "精选内容",
        },
        {
            "name": "核心产品 C",
            "description": "用于补齐产品矩阵，使页面结构更像真实商业官网。",
            "price": "¥399",
            "image_query": "product showcase",
            "tag": "新品",
            "meta": "形象展示",
        },
    ],
}


def infer_industry(prompt: str, reference_brands: List[str]) -> str:
    lowered = prompt.lower()
    for brand in reference_brands:
        if brand in BRAND_TO_INDUSTRY:
            return BRAND_TO_INDUSTRY[brand]

    for industry, keywords in INDUSTRY_KEYWORDS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return industry

    return "brand"


def industry_label(industry_hint: str) -> str:
    return INDUSTRY_LABELS.get(industry_hint, INDUSTRY_LABELS["brand"])


def get_products(industry_hint: str) -> List[Dict[str, str]]:
    industry = industry_hint if industry_hint in PRODUCT_LIBRARY else "brand"
    return [dict(item) for item in PRODUCT_LIBRARY[industry]]


def get_featured_products(industry_hint: str) -> List[Dict[str, str]]:
    return get_products(industry_hint)[:3]


def get_image_keywords(industry_hint: str) -> List[str]:
    queries: List[str] = []
    for item in get_products(industry_hint):
        query = item.get("image_query", "").strip()
        if query and query not in queries:
            queries.append(query)
    return queries
