from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, FileResponse

from app.config import settings
from app.services.regions import url_for_service, get_region, regions

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


@main_router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    content = """
    User-agent: *
    Allow: /
    
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


@main_router.get('/privacy', response_class=HTMLResponse)
async def privacy_page(request: Request):
    return templates.TemplateResponse('privacy.html', {
        'request': request,
        'region': None,
        'regions': regions,
        'url_for_service' : url_for_service
    })


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