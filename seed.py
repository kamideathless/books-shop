import asyncio
import random
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
    {"title": "Белая гвардия", "author": "Михаил Булгаков", "year": 1925},
    {"title": "Собачье сердце", "author": "Михаил Булгаков", "year": 1925},
    {"title": "Роковые яйца", "author": "Михаил Булгаков", "year": 1924},
    {"title": "Война и мир", "author": "Лев Толстой", "year": 1869},
    {"title": "Анна Каренина", "author": "Лев Толстой", "year": 1878},
    {"title": "Воскресение", "author": "Лев Толстой", "year": 1899},
    {"title": "Детство", "author": "Лев Толстой", "year": 1852},
    {"title": "Крейцерова соната", "author": "Лев Толстой", "year": 1889},
    {"title": "Братья Карамазовы", "author": "Фёдор Достоевский", "year": 1880},
    {"title": "Идиот", "author": "Фёдор Достоевский", "year": 1869},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "year": 1866},
    {"title": "Бесы", "author": "Фёдор Достоевский", "year": 1872},
    {"title": "Подросток", "author": "Фёдор Достоевский", "year": 1875},
    {"title": "Белые ночи", "author": "Фёдор Достоевский", "year": 1848},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "year": 1833},
    {"title": "Капитанская дочка", "author": "Александр Пушкин", "year": 1836},
    {"title": "Пиковая дама", "author": "Александр Пушкин", "year": 1834},
    {"title": "Дубровский", "author": "Александр Пушкин", "year": 1841},
    {"title": "Повести Белкина", "author": "Александр Пушкин", "year": 1831},
    {"title": "Мёртвые души", "author": "Николай Гоголь", "year": 1842},
    {"title": "Ревизор", "author": "Николай Гоголь", "year": 1836},
    {"title": "Тарас Бульба", "author": "Николай Гоголь", "year": 1835},
    {"title": "Вечера на хуторе близ Диканьки", "author": "Николай Гоголь", "year": 1831},
    {"title": "Шинель", "author": "Николай Гоголь", "year": 1842},
    {"title": "Три товарища", "author": "Эрих Мария Ремарк", "year": 1936},
    {"title": "На западном фронте без перемен", "author": "Эрих Мария Ремарк", "year": 1929},
    {"title": "Триумфальная арка", "author": "Эрих Мария Ремарк", "year": 1945},
    {"title": "Ночь в Лиссабоне", "author": "Эрих Мария Ремарк", "year": 1962},
    {"title": "Жизнь взаймы", "author": "Эрих Мария Ремарк", "year": 1959},
    {"title": "Чёрный обелиск", "author": "Эрих Мария Ремарк", "year": 1956},
    {"title": "Старик и море", "author": "Эрнест Хемингуэй", "year": 1952},
    {"title": "Прощай оружие", "author": "Эрнест Хемингуэй", "year": 1929},
    {"title": "По ком звонит колокол", "author": "Эрнест Хемингуэй", "year": 1940},
    {"title": "Фиеста", "author": "Эрнест Хемингуэй", "year": 1926},
    {"title": "Снега Килиманджаро", "author": "Эрнест Хемингуэй", "year": 1936},
    {"title": "1984", "author": "Джордж Оруэлл", "year": 1949},
    {"title": "Скотный двор", "author": "Джордж Оруэлл", "year": 1945},
    {"title": "Дорога на Уиган-Пирс", "author": "Джордж Оруэлл", "year": 1937},
    {"title": "Вишнёвый сад", "author": "Антон Чехов", "year": 1904},
    {"title": "Три сестры", "author": "Антон Чехов", "year": 1901},
    {"title": "Дядя Ваня", "author": "Антон Чехов", "year": 1897},
    {"title": "Палата №6", "author": "Антон Чехов", "year": 1892},
    {"title": "Степь", "author": "Антон Чехов", "year": 1888},
    {"title": "Отцы и дети", "author": "Иван Тургенев", "year": 1862},
    {"title": "Рудин", "author": "Иван Тургенев", "year": 1856},
    {"title": "Дворянское гнездо", "author": "Иван Тургенев", "year": 1859},
    {"title": "Накануне", "author": "Иван Тургенев", "year": 1860},
    {"title": "Герой нашего времени", "author": "Михаил Лермонтов", "year": 1840},
    {"title": "Демон", "author": "Михаил Лермонтов", "year": 1842},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "year": 1940},
    {"title": "Доктор Живаго", "author": "Борис Пастернак", "year": 1957},
    {"title": "Зов предков", "author": "Джек Лондон", "year": 1903},
    {"title": "Белый клык", "author": "Джек Лондон", "year": 1906},
    {"title": "Мартин Иден", "author": "Джек Лондон", "year": 1909},
    {"title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "year": 1997},
    {"title": "Гарри Поттер и тайная комната", "author": "Джоан Роулинг", "year": 1998},
    {"title": "Гарри Поттер и узник Азкабана", "author": "Джоан Роулинг", "year": 1999},
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "year": 1943},
    {"title": "Великий Гэтсби", "author": "Фрэнсис Скотт Фицджеральд", "year": 1925},
    {"title": "Над пропастью во ржи", "author": "Джером Сэлинджер", "year": 1951},
    {"title": "Шантарам", "author": "Грегори Дэвид Робертс", "year": 2003},
    {"title": "Алхимик", "author": "Пауло Коэльо", "year": 1988},
    {"title": "Вероника решает умереть", "author": "Пауло Коэльо", "year": 1998},
    {"title": "Пятая гора", "author": "Пауло Коэльо", "year": 1996},
]

FAKE_USERS = [
    {"username": "alex_reader", "name": "Александр", "age": 28},
    {"username": "maria_books", "name": "Мария", "age": 24},
    {"username": "ivan_lit", "name": "Иван", "age": 35},
    {"username": "olga_reads", "name": "Ольга", "age": 31},
    {"username": "dmitry_pages", "name": "Дмитрий", "age": 22},
    {"username": "anna_bookworm", "name": "Анна", "age": 27},
    {"username": "sergey_lit", "name": "Сергей", "age": 40},
    {"username": "natasha_reads", "name": "Наташа", "age": 19},
    {"username": "pavel_books", "name": "Павел", "age": 33},
    {"username": "elena_pages", "name": "Елена", "age": 26},
    {"username": "andrey_reader", "name": "Андрей", "age": 29},
    {"username": "yulia_lit", "name": "Юлия", "age": 23},
    {"username": "nikita_books", "name": "Никита", "age": 21},
    {"username": "ksenia_reads", "name": "Ксения", "age": 30},
    {"username": "maxim_pages", "name": "Максим", "age": 25},
    {"username": "tatiana_lit", "name": "Татьяна", "age": 38},
    {"username": "roman_reader", "name": "Роман", "age": 32},
    {"username": "daria_books", "name": "Дарья", "age": 20},
    {"username": "kirill_reads", "name": "Кирилл", "age": 36},
    {"username": "victoria_pages", "name": "Виктория", "age": 27},
    {"username": "artem_lit", "name": "Артём", "age": 24},
    {"username": "polina_reader", "name": "Полина", "age": 22},
    {"username": "igor_books", "name": "Игорь", "age": 41},
    {"username": "alina_reads", "name": "Алина", "age": 18},
    {"username": "denis_pages", "name": "Денис", "age": 34},
]

REVIEW_TEXTS = [
    "Отличная книга, рекомендую всем!",
    "Читал на одном дыхании, не мог оторваться.",
    "Классика мировой литературы, обязательно к прочтению.",
    "Немного скучновато в начале, но потом захватывает.",
    "Одна из лучших книг что я читал.",
    "Глубокая и философская книга.",
    "Не понравилось, слишком затянуто.",
    "Прекрасный язык, великолепные образы.",
    "Перечитывал несколько раз, каждый раз открываю что-то новое.",
    "Средняя книга, ничего особенного.",
    "Шедевр! Обязательно прочитайте.",
    "Тяжело читать, но оно того стоит.",
    "Лёгкое чтение, приятно провёл время.",
    "Не моё, но понимаю почему это классика.",
    "Очень понравилось, советую друзьям.",
]

ADMIN_USER = {
    "username": "adminuser",
    "password": "adminpass123",
    "name": "Admin",
    "age": 30,
}


async def seed():
    from app.models import Book, User
    from app.models.shop import ShopItem
    from app.models.review import Review
    from app.models.user import UserRole
    from app.utils.utils import hash_password

    async with async_session() as session:
        # --- книги ---
        result = await session.execute(select(Book))
        existing_books = result.scalars().all()
        existing_titles = {b.title for b in existing_books}

        added_books = []
        for book_data in BOOKS:
            if book_data["title"] not in existing_titles:
                book = Book(**book_data)
                session.add(book)
                added_books.append(book)

        await session.flush()
        all_books = existing_books + added_books
        print(f"Добавлено книг: {len(added_books)}")

        # --- магазин ---
        result = await session.execute(select(ShopItem.book_id))
        existing_shop_ids = {row[0] for row in result.all()}

        shop_added = 0
        for book in all_books:
            if book.id not in existing_shop_ids:
                session.add(ShopItem(
                    book_id=book.id,
                    price=round(random.uniform(299, 1499), 2),
                    stock=random.randint(1, 50),
                ))
                shop_added += 1
        print(f"Добавлено в магазин: {shop_added}")

        # --- пользователи ---
        result = await session.execute(select(User.username))
        existing_usernames = {row[0] for row in result.all()}

        added_users = []
        for user_data in FAKE_USERS:
            if user_data["username"] not in existing_usernames:
                password = f"{user_data['username']}_pass"
                user = User(
                    username=user_data["username"],
                    name=user_data["name"],
                    age=user_data.get("age", 25),
                    password=password,
                    hashed_password=hash_password(password),
                    role=UserRole.USER,
                )
                session.add(user)
                added_users.append(user)

        await session.flush()
        print(f"Добавлено пользователей: {len(added_users)}")

        # --- отзывы ---
        result = await session.execute(select(Review.user_id, Review.book_id))
        existing_reviews = {(row[0], row[1]) for row in result.all()}

        reviews_added = 0
        for user in added_users:
            books_to_review = random.sample(all_books, k=random.randint(5, 15))
            for book in books_to_review:
                if (user.id, book.id) not in existing_reviews:
                    session.add(Review(
                        user_id=user.id,
                        book_id=book.id,
                        rate=round(random.uniform(2.0, 5.0), 1),
                        description=random.choice(REVIEW_TEXTS),
                    ))
                    existing_reviews.add((user.id, book.id))
                    reviews_added += 1

        # --- админ ---
        result = await session.execute(
            select(User).where(User.username == ADMIN_USER["username"])
        )
        if result.scalar_one_or_none() is None:
            session.add(User(
                username=ADMIN_USER["username"],
                password=ADMIN_USER["password"],
                name=ADMIN_USER["name"],
                age=ADMIN_USER["age"],
                hashed_password=hash_password(ADMIN_USER["password"]),
                role=UserRole.ADMIN,
            ))
            print(f"Создан админ: {ADMIN_USER['username']} / {ADMIN_USER['password']}")

        await session.commit()
        print(f"Добавлено отзывов: {reviews_added}")
        print("Seed завершён.")


if __name__ == "__main__":
    asyncio.run(seed())