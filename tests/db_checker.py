import asyncio
import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


async def check_database():
    try:
        # Get the database URL from the environment variable
        db_url = os.getenv('DB_URL')

        if db_url:
            # Create an async engine
            async_engine = create_async_engine(db_url, echo=True)

            # Create a synchronous sessionmaker
            Session = sessionmaker(bind=async_engine)

            async with async_engine.connect() as conn:
                print("Database connected successfully")

                # Create a MetaData object
                metadata = MetaData()

                # Reflect the existing database schema using a synchronous session
                await conn.run_sync(metadata.reflect)

                # Check if the 'users' table exists in the metadata
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
