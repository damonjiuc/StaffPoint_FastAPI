import json

from datetime import datetime
from typing import Iterable

from app.database.models import News

BASE_URL = "https://staffpoint.ru"


def dump_jsonld(data: dict) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
        separators=(",", ": ")
    )


def breadcrumb(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    }


def news_list_schema(news_items: Iterable[News]) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Главная",
                        "item": "https://staffpoint.ru/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Новости",
                        "item": "https://staffpoint.ru/news/",
                    },
                ],
            },
            {
                "@type": "CollectionPage",
                "name": "Новости — Staff Point",
                "url": "https://staffpoint.ru/news/",
                "description": "Статьи и новости о мерчандайзинге и ритейле в различных индустриях (FMCG, Beauty, DIY и др.) от мерчандайзинг агентства Staff Point.",
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index + 1,
                            "name": f"{news.title}",
                            "url": f"https://staffpoint.ru/news/{news.slug}/",
                        }
                        for index, news in enumerate(news_items)
                    ],
                },
            },
        ],
    }


def news_detail_schema(news: News) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Главная",
                        "item": "https://staffpoint.ru/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Новости",
                        "item": "https://staffpoint.ru/news/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": news.title,
                        "item": f"https://staffpoint.ru/news/{news.slug}/",
                    },
                ],
            },
            {
                "@type": "NewsArticle",
                "headline": news.title,
                "datePublished": news.published_at.isoformat(),
                "author": {
                    "@type": "Organization",
                    "name": "Staff Point",
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Staff Point",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://staffpoint.ru/static/staffpoint-logo.png",
                    },
                },
            },
        ],
    }