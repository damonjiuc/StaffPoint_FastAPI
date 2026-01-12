from fastapi import APIRouter
from fastapi.responses import RedirectResponse

redirects_router = APIRouter(
    tags=['Redirects']
)

# Vacancies
@redirects_router.get("/vacancies.html")
@redirects_router.get("/vacancies/coordinator.html")
@redirects_router.get("/vacancies/controller.html")
@redirects_router.get("/vacancies/merchandising.html")
async def redirect_vacancies():
    return RedirectResponse(url="/vacancies", status_code=301)

# About
@redirects_router.get("/opps.html")
async def redirect_about():
    return RedirectResponse(url="/about", status_code=301)

# Services
@redirects_router.get("/merch.html")
async def redirect_merch():
    return RedirectResponse(url="/merch/", status_code=301)

@redirects_router.get("/tech.html")
async def redirect_posm():
    return RedirectResponse(url="/posm-placement/", status_code=301)

@redirects_router.get("/aud.html")
async def redirect_audit():
    return RedirectResponse(url="/audit/", status_code=301)

@redirects_router.get("/outsource.html")
async def redirect_outsource():
    return RedirectResponse(url="/outsource-staff/", status_code=301)