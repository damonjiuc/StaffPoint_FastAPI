from sqlalchemy import Date, func, Integer, String, Text, Table, ForeignKey, Column, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created: Mapped[Date] = mapped_column(Date, default=date.today())
    updated: Mapped[Date] = mapped_column(Date, default=date.today(), onupdate=date.today())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class NewsSection(Base):
    __tablename__ = "news_sections"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)

    news: Mapped[list["News"]] = relationship(
        back_populates="section"
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"<Tag {self.title}>"


class Tag(Base):
    __tablename__ = "tags"

    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    news: Mapped[list["News"]] = relationship(
        secondary="news_tags",
        back_populates="tags"
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"<Tag {self.title}>"


news_tags = Table(
    "news_tags",
    Base.metadata,
    Column("news_id", ForeignKey("news.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class News(Base):
    __tablename__ = "news"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    preview_text: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    section_id: Mapped[int] = mapped_column(
        ForeignKey("news_sections.id"),
        index=True
    )

    section: Mapped["NewsSection"] = relationship(back_populates="news")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="news_tags",
        back_populates="news"
    )

    # 🔍 SEO
    meta_title: Mapped[str | None] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(String(255))
    meta_keywords: Mapped[str | None] = mapped_column(String(255))

    # 📈 просмотры
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    # 🖼 изображение превью
    image: Mapped[str | None] = mapped_column(String(255))

    # 📅 публикация
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime)