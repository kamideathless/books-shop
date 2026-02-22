import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"{os.getenv('DATABASE_SCHEMA')}://"
    f"{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

BOOKS = [
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967},
    {"title": "1984", "author": "Джордж Оруэлл", "year": 1949},
    {"title": "Война и мир", "author": "Лев Толстой", "year": 1869},
    {"title": "Анна Каренина", "author": "Лев Толстой", "year": 1878},
    {"title": "Воскресение", "author": "Лев Толстой", "year": 1899},
    {"title": "Братья Карамазовы", "author": "Фёдор Достоевский", "year": 1880},
    {"title": "Идиот", "author": "Фёдор Достоевский", "year": 1869},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "year": 1866},
    {"title": "Бесы", "author": "Фёдор Достоевский", "year": 1872},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "year": 1833},
    {"title": "Капитанская дочка", "author": "Александр Пушкин", "year": 1836},
    {"title": "Пиковая дама", "author": "Александр Пушкин", "year": 1834},
    {"title": "Дубровский", "author": "Александр Пушкин", "year": 1841},
    {"title": "Мёртвые души", "author": "Николай Гоголь", "year": 1842},
    {"title": "Ревизор", "author": "Николай Гоголь", "year": 1836},
    {"title": "Тарас Бульба", "author": "Николай Гоголь", "year": 1835},
    {"title": "Три товарища", "author": "Эрих Мария Ремарк", "year": 1936},
    {
        "title": "На западном фронте без перемен",
        "author": "Эрих Мария Ремарк",
        "year": 1929,
    },
    {"title": "Триумфальная арка", "author": "Эрих Мария Ремарк", "year": 1945},
    {"title": "Ночь в Лиссабоне", "author": "Эрих Мария Ремарк", "year": 1962},
    {"title": "Старик и море", "author": "Эрнест Хемингуэй", "year": 1952},
    {"title": "Прощай оружие", "author": "Эрнест Хемингуэй", "year": 1929},
    {"title": "По ком звонит колокол", "author": "Эрнест Хемингуэй", "year": 1940},
    {
        "title": "Гарри Поттер и философский камень",
        "author": "Джоан Роулинг",
        "year": 1997,
    },
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "year": 1943},
    {"title": "Великий Гэтсби", "author": "Фрэнсис Скотт Фицджеральд", "year": 1925},
    {"title": "Над пропастью во ржи", "author": "Джером Сэлинджер", "year": 1951},
    {"title": "Герой нашего времени", "author": "Михаил Лермонтов", "year": 1840},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "year": 1940},
    {"title": "Доктор Живаго", "author": "Борис Пастернак", "year": 1957},
]

ADMIN_USER = {
    "username": "adminuser",
    "password": "adminpass123",
    "name": "Admin",
    "age": 30,
}


async def seed():
    from app.models import Book, User
    from app.models.user import UserRole
    from app.utils.utils import hash_password

    async with async_session() as session:
        result = await session.execute(select(Book))
        existing_books = result.scalars().all()
        existing_titles = {b.title for b in existing_books}

        added = 0
        for book_data in BOOKS:
            if book_data["title"] not in existing_titles:
                book = Book(**book_data)
                session.add(book)
                added += 1

        result = await session.execute(
            select(User).where(User.username == ADMIN_USER["username"])
        )
        admin = result.scalar_one_or_none()
        if admin is None:
            admin = User(
                username=ADMIN_USER["username"],
                password=ADMIN_USER["password"],
                name=ADMIN_USER["name"],
                age=ADMIN_USER["age"],
                hashed_password=hash_password(ADMIN_USER["password"]),
                role=UserRole.ADMIN,
            )
            session.add(admin)
            print(f"Создан админ: {ADMIN_USER['username']} / {ADMIN_USER['password']}")

        await session.commit()
        print(f"Добавлено книг: {added}")
        print("Seed завершён.")


if __name__ == "__main__":
    asyncio.run(seed())