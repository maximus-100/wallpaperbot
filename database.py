import sqlite3


class WallpapersDB:

    @staticmethod
    def connect():
        database = sqlite3.connect('wallpaper.db')
        cursor = database.cursor()
        return database, cursor

    @staticmethod
    def close(database):
        database.close()

    @staticmethod
    def create_categories_table():
        database, cursor = WallpapersDB.connect()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(20) UNIQUE
        );
        ''')
        database.commit()
        WallpapersDB.close(database)

    @staticmethod
    def create_images_table():
        database, cursor = WallpapersDB.connect()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS images(
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_link TEXT UNIQUE,
            category_id INTEGER REFERENCES categories(category_id)
        );
        ''')
        database.commit()
        WallpapersDB.close(database)

    @staticmethod
    def insert_category(true_name):
        database, cursor = WallpapersDB.connect()
        cursor.execute('''
        INSERT OR IGNORE INTO categories (category_name) VALUES (?);
        ''', (true_name, ))

        database.commit()
        WallpapersDB.close(database)

    @staticmethod
    def get_category_id(true_name):
        database, cursor = WallpapersDB.connect()
        cursor.execute('''
        SELECT category_id FROM categories WHERE category_name = ?
        ''', (true_name, ))
        category_id = cursor.fetchone()
        WallpapersDB.close(database)
        return category_id[0]

    @staticmethod
    def insert_into_images(image_link, category_id):
        database, cursor = WallpapersDB.connect()
        cursor.execute('''
           INSERT OR IGNORE INTO images(image_link, category_id) VALUES (?, ?)

           ''', (image_link, category_id))
        database.commit()
        WallpapersDB.close(database)


WallpapersDB.create_categories_table()
WallpapersDB.create_images_table()