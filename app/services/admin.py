from sqladmin import ModelView
from app.database.models import News
from app.database.models import NewsSection, Tag
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    async def login(self, request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == "admin" and password == "password":
            request.session["user"] = {"username": "admin"}
            return True

        return False

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        return request.session.get("user")


class NewsAdmin(ModelView, model=News):
    name = "Новость"
    name_plural = "Новости"
    edit_template = "sqladmin/news.html"

    # Что показывать в списке
    column_list = [
        News.id,
        News.title,
        News.views_count,
        News.is_published,
        News.published_at,
        News.section,
    ]

    # Поиск
    column_searchable_list = [News.title]

    # Сортировка
    column_sortable_list = [News.published_at]

    # Что редактировать в форме
    form_columns = [
        News.title,
        News.slug,
        News.section,
        News.meta_title,
        News.meta_description,
        News.meta_keywords,
        News.image,
        News.preview_text,
        News.content,
        News.tags,
        News.is_published,
        News.published_at
    ]


class NewsSectionAdmin(ModelView, model=NewsSection):
    name = "Раздел"
    name_plural = "Разделы"
    column_list = [NewsSection.id, NewsSection.title, NewsSection.slug]
    column_searchable_list = [NewsSection.title]


class TagAdmin(ModelView, model=Tag):
    name = "Тег"
    name_plural = "Теги"
    column_list = [Tag.id, Tag.title, Tag.slug]
    column_searchable_list = [Tag.title]