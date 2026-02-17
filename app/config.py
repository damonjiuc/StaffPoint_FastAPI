from pydantic_settings import BaseSettings
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent

regions = {
    "msk": {"slug": "msk", "name": "Москва", "insert": "в Москве"},
    "spb": {"slug": "spb", "name": "Санкт-Петербург", "insert": "в Санкт-Петербурге"},
    "ekb": {"slug": "ekb", "name": "Екатеринбург", "insert": "в Екатеринбурге"},
    "novosib": {"slug": "novosib", "name": "Новосибирск", "insert": "в Новосибирске"},
    "kzn": {"slug": "kzn", "name": "Казань", "insert": "в Казани"},
    "nn": {"slug": "nn", "name": "Нижний Новгород", "insert": "в Нижнем Новгороде"},
    "krr": {"slug": "krr", "name": "Краснодар", "insert": "в Краснодаре"},
    "chelyabinsk": {"slug": "chelyabinsk", "name": "Челябинск", "insert": "в Челябинске"},
    "samara": {"slug": "samara", "name": "Самара", "insert": "в Самаре"},
    "omsk": {"slug": "omsk", "name": "Омск", "insert": "в Омске"},
    "rostov": {"slug": "rostov", "name": "Ростов-на-Дону", "insert": "в Ростове-на-Дону"},
    "ufa": {"slug": "ufa", "name": "Уфа", "insert": "в Уфе"},
    "krasnoyarsk": {"slug": "krasnoyarsk", "name": "Красноярск", "insert": "в Красноярске"},
    "voronezh": {"slug": "voronezh", "name": "Воронеж", "insert": "в Воронеже"},
    "perm": {"slug": "perm", "name": "Пермь", "insert": "в Перми"},
    "volgograd": {"slug": "volgograd", "name": "Волгоград", "insert": "в Волгограде"},
    "vladivostok": {"slug": "vladivostok", "name": "Владивосток", "insert": "во Владивостоке"},
    "irkutsk": {"slug": "irkutsk", "name": "Иркутск", "insert": "в Иркутске"},
    "yaroslavl": {"slug": "yaroslavl", "name": "Ярославль", "insert": "в Ярославле"},
    "khabarovsk": {"slug": "khabarovsk", "name": "Хабаровск", "insert": "в Хабаровске"},
    "tolyatti": {"slug": "tolyatti", "name": "Тольятти", "insert": "в Тольятти"},
    "barnaul": {"slug": "barnaul", "name": "Барнаул", "insert": "в Барнауле"},
    "ulyanovsk": {"slug": "ulyanovsk", "name": "Ульяновск", "insert": "в Ульяновске"},
    "tumen": {"slug": "tumen", "name": "Тюмень", "insert": "в Тюмени"},
    "izhevsk": {"slug": "izhevsk", "name": "Ижевск", "insert": "в Ижевске"},
    "vladimir": {"slug": "vladimir", "name": "Владимир", "insert": "во Владимире"},
    "tomsk": {"slug": "tomsk", "name": "Томск", "insert": "в Томске"},
    "orenburg": {"slug": "orenburg", "name": "Оренбург", "insert": "в Оренбурге"},
    "kemerovo": {"slug": "kemerovo", "name": "Кемерово", "insert": "в Кемерово"},
    "novokuznetsk": {"slug": "novokuznetsk", "name": "Новокузнецк", "insert": "в Новокузнецке"},
    "ryazan": {"slug": "ryazan", "name": "Рязань", "insert": "в Рязани"},
    "astrahan": {"slug": "astrahan", "name": "Астрахань", "insert": "в Астрахани"},
    "naberezhnye_chelny": {"slug": "naberezhnye_chelny", "name": "Набережные Челны", "insert": "в Набережных Челнах"},
    "penza": {"slug": "penza", "name": "Пенза", "insert": "в Пензе"},
    "kirov": {"slug": "kirov", "name": "Киров", "insert": "в Кирове"},
    "lipetsk": {"slug": "lipetsk", "name": "Липецк", "insert": "в Липецке"},
    "balashiha": {"slug": "balashiha", "name": "Балашиха", "insert": "в Балашихе"},
    "kaliningrad": {"slug": "kaliningrad", "name": "Калининград", "insert": "в Калининграде"},
    "tula": {"slug": "tula", "name": "Тула", "insert": "в Туле"},
    "stavropol": {"slug": "stavropol", "name": "Ставрополь", "insert": "в Ставрополе"}
}


class Settings(BaseSettings):
    DB_ROUTE: str

    debug: bool = True

    BASE_URL: str = "https://staffpoint.ru"

    # SMTP настройки
    SMTP_HOST: str
    SMTP_PORT: int = 25
    SMTP_TLS: bool = False
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    TEMPLATES_DIR: Path = BASE_DIR / 'app' / 'templates'
    STATIC_URL: str = '/static'
    STATIC_DIR: Path = BASE_DIR / 'app' / 'static'
    UPLOAD_DIR: Path = BASE_DIR / 'app' / 'static' / 'uploads'

    def mount_static(self, app):
        if self.STATIC_DIR.exists():
            app.mount(
                self.STATIC_URL,
                StaticFiles(directory=self.STATIC_DIR),
                name='static'
            )
        else:
            raise RuntimeError(f'Static directory not found: {self.STATIC_DIR}')

    def configure_templates(self):
        templates = Jinja2Templates(directory=self.TEMPLATES_DIR)

        templates.env.globals['url_for'] = lambda name, **params: f'/static/{params.get("filename", "")}'

        templates.env.globals['regions'] = regions

        return templates

    @property
    def database_url(self) -> str:
        return f'{self.DB_ROUTE}'

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()