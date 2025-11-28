from fastapi import HTTPException
from app.config import regions


def get_region(region_slug: str | None):
    print('region_slug raw:', region_slug)
    if not region_slug:
        return None
    if region_slug not in regions:
        raise HTTPException(status_code=404, detail='Регион не найден')
    return regions[region_slug]


def url_for_service(service_slug: str, region: dict | None = None) -> str:
    """
    Возвращает корректный URL для услуги с учётом региона.
    """
    if region and region.get('slug'):
        return f'/{region["slug"]}/{service_slug}'
    return f'/{service_slug}'