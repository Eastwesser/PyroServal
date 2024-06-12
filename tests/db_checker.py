import asyncio
import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


async def check_database():
    try:
        # Получаем URL базы данных из переменной окружения
        db_url = os.getenv('DB_URL')

        if db_url:
            # Создаем асинхронный engine
            async_engine = create_async_engine(db_url, echo=True)

            # Создаем синхронный sessionmaker
            Session = sessionmaker(bind=async_engine)

            async with async_engine.connect() as conn:
                print("Database connected successfully")

                # Создаем объект MetaData
                metadata = MetaData()

                # Отражаем существующую схему базы данных с использованием синхронной сессии
                await conn.run_sync(metadata.reflect)

                # Проверяем, существует ли таблица 'users' в метаданных
                if 'users' in metadata.tables:
                    print("The 'users' table exists in the database")
                else:
                    print("The 'users' table is missing")
        else:
            print("DB_URL environment variable is not set")
    except Exception as e:
        print(f"Error occurred while checking database: {e}")


async def main():
    await check_database()


if __name__ == '__main__':
    asyncio.run(main())
