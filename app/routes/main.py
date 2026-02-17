from fastapi import APIRouter, Request, UploadFile, File, Response
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, JSONResponse
from pathlib import Path
from sqlalchemy import select, desc
import shutil

from sqlalchemy.orm import selectinload

from app.config import settings
from app.database.engine import session_maker
from app.services.regions import url_for_service, get_region, regions
from app.database.models import NewsSection, Tag, News
from app.services.news import news_list_schema, news_detail_schema, dump_jsonld, render_news_sitemap

templates = settings.configure_templates()

main_router = APIRouter(
    tags=['Main']
)


@main_router.get('/favicon.svg')
async def favicon():
    return RedirectResponse(url='/static/favicon.svg')


@main_router.get('/sitemap.xml')
async def sitemap():
    return RedirectResponse(url='/static/sitemap.xml')


@main_router.get('/sitemap-static.xml')
async def sitemap():
    return RedirectResponse(url='/static/sitemap-static.xml')


@main_router.get("/sitemap-news.xml")
async def sitemap_news():
    async with session_maker() as session:
        result = await session.execute(
            select(News).where(News.is_published == True)
        )
        news_items = result.scalars().all()

    base_url = settings.BASE_URL

    urls = [
        {
            "loc": f"{base_url}/news/{news.slug}/",
            "lastmod": (
                news.updated.isoformat() or news.published_at.date().isoformat()
            ),
        }
        for news in news_items
    ]

    xml = await render_news_sitemap(urls)

    return Response(
        content=xml,
        media_type="application/xml"
    )


@main_router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    content = """
    User-agent: *
    Allow: /
    Disallow: /news/
    
    Sitemap: https://staffpoint.ru/sitemap.xml
    """
    return content


@main_router.get('/', response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request,
        'region': None,
        'regions': regions,
        'url_for_service' : url_for_service
    })


@main_router.get('/en', response_class=HTMLResponse)
async def about_page_region(request: Request, region_slug: str | None = None):
    region = get_region(region_slug)
    return templates.TemplateResponse('en_about.html', {
        'request': request,
        'region': region,
        'regions': regions,
        'url_for_service' : url_for_service
    })


UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

@main_router.post("/admin/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse({"location": f"/static/uploads/{file.filename}"})


@main_router.get('/privacy', response_class=HTMLResponse)
async def privacy_page(request: Request):
    return templates.TemplateResponse('privacy.html', {
        'request': request,
        'region': None,
        'regions': regions,
        'url_for_service' : url_for_service
    })


@main_router.get("/news/", response_class=HTMLResponse)
async def news_list(request: Request, section: str | None = None, tag: str | None = None):
    async with session_maker() as session:
        query = select(News).options(
            selectinload(News.section),
            selectinload(News.tags)
        ).where(News.is_published == True
        ).order_by(desc(News.published_at))

        if section:
            query = query.join(News.section).where(NewsSection.slug == section)

        if tag:
            query = query.join(News.tags).where(Tag.slug == tag)

        result = await session.execute(query)
        news_items = result.scalars().all()

        # Для бокового меню
        sections_result = await session.execute(select(NewsSection))
        sections = sections_result.scalars().all()

        tags_result = await session.execute(select(Tag))
        tags = tags_result.scalars().all()

        jsonld = dump_jsonld(news_list_schema(news_items))

    return templates.TemplateResponse(
        "news_list.html",
        {
            "request": request,
            "news_items": news_items,
            "sections": sections,
            "tags": tags,
            "jsonld": jsonld,
            "current_section": section,
            "current_tag": tag,
            'region': None,
            'regions': regions,
            'url_for_service': url_for_service
        }
    )

# === Детальная страница новости ===
@main_router.get("/news/{slug}/", response_class=HTMLResponse)
async def news_detail(request: Request, slug: str):
    async with session_maker() as session:
        query = select(News).options(
            selectinload(News.section),
            selectinload(News.tags)
        ).where(News.slug == slug, News.is_published == True)

        result = await session.execute(query)
        news_item = result.scalar_one_or_none()

        query = (
            select(News)
            .options(
                selectinload(News.section),
                selectinload(News.tags),
            )
            .where(News.is_published.is_(True))
            .order_by(desc(News.published_at))
            .limit(6)
        )

        result = await session.execute(query)
        news_items = result.scalars().all()

        jsonld = dump_jsonld(news_detail_schema(news_item))

        if not news_item:
            return HTMLResponse("Not Found", status_code=404)

    return templates.TemplateResponse(
        "news_detail.html",
        {
            "request": request,
            "news_items": news_items,
            "news_item": news_item,
            "jsonld": jsonld,
            'region': None,
            'regions': regions,
            'url_for_service': url_for_service
        }
    )


@main_router.get('/{region_slug}/', response_class=HTMLResponse)
async def contacts_page_region(request: Request, region_slug: str | None = None):
    region = get_region(region_slug)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'region': region,
        'regions': regions,
        'url_for_service' : url_for_service
    })


@main_router.get('/contacts', response_class=HTMLResponse)
@main_router.get('/{region_slug}/contacts', response_class=HTMLResponse)
async def contacts_page_region(request: Request, region_slug: str | None = None):
    region = get_region(region_slug)
    return templates.TemplateResponse('contacts.html', {
        'request': request,
        'region': region,
        'regions': regions,
        'url_for_service' : url_for_service
    })


@main_router.get('/about', response_class=HTMLResponse)
@main_router.get('/{region_slug}/about', response_class=HTMLResponse)
async def about_page_region(request: Request, region_slug: str | None = None):
    region = get_region(region_slug)
    return templates.TemplateResponse('about.html', {
        'request': request,
        'region': region,
        'regions': regions,
        'url_for_service' : url_for_service
    })


@main_router.get('/vacancies', response_class=HTMLResponse)
@main_router.get('/{region_slug}/vacancies', response_class=HTMLResponse)
async def vacancies_page_region(request: Request, region_slug: str | None = None):
    region = get_region(region_slug)
    return templates.TemplateResponse('vacancies.html', {
        'request': request,
        'region': region,
        'regions': regions,
        'url_for_service' : url_for_service
    })