import psycopg2
from psycopg2 import sql, extensions

connection = psycopg2.connect(
    dbname='bookstore_db',
    user='postgres',
    password='YOUR_PASSWORD',
    host='localhost',
    port='5432'
)

cursor = connection.cursor()

tables_queries = (
    """
    CREATE TABLE IF NOT EXISTS Authors
    (id SERIAL PRIMARY KEY, 
     name VARCHAR(255) NOT NULL);
    """,

    """
    CREATE TABLE IF NOT EXISTS Genres
    (id SERIAL PRIMARY KEY, 
     name VARCHAR(100) NOT NULL);
    """,

    """
    CREATE TABLE IF NOT EXISTS Books
    (id SERIAL PRIMARY KEY, 
     title VARCHAR(255) NOT NULL, 
     publication_date DATE, 
     author_id INTEGER, 
     genre_id INTEGER,
     FOREIGN KEY (author_id) REFERENCES Authors (id) ON UPDATE CASCADE ON DELETE CASCADE, 
     FOREIGN KEY (genre_id) REFERENCES Genres (id) ON UPDATE CASCADE ON DELETE CASCADE
     );
    """
)

for query in tables_queries:
    cursor.execute(query)
    connection.commit()


class BookstoreDB:
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password,
                                           host=host, port=port)
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()

    def add_author(self, name: str):
        query = sql.SQL("INSERT INTO Authors (name) VALUES (%s)")
        self.cursor.execute(query, (name, ))

    def add_genre(self, genre_name):
        query = sql.SQL("INSERT INTO Genres (name) VALUES (%s)")
        self.cursor.execute(query, (genre_name, ))

    def add_book(self, title, author_id, genre_id, publication_date):
        query = sql.SQL("INSERT INTO Books (title, author_id, genre_id, publication_date)"
                        "VALUES (%s, %s, %s, %s)")
        self.cursor.execute(query, (title, author_id, genre_id, publication_date))

    def author_by_name(self, name):
        query = sql.SQL("SELECT id, name FROM Authors WHERE name = %s")
        self.cursor.execute(query, (name, ))
        author = self.cursor.fetchall()
        return author

    def close(self):
        self.cursor.close()
        self.connection.close()


db = BookstoreDB(
    dbname='bookstore_db',
    user='postgres',
    password='YOUR_PASSWORD',
    host='localhost',
    port='5432'
)

while True:
    print("1. Add author")
    print("2. Add genre")
    print("3. Find author ")
    print("4. Add book")
    print("Type 'exit' to exit the program")

    choice = input("Choice the action: ")

    if choice == '1':
        author_name = input("Enter author's name: ")
        db.add_author(author_name)
    elif choice == '2':
        genre_name = input('Enter genre name: ')
        db.add_genre(genre_name)
    elif choice == '3':
        author_name = input("Enter author's name for search: ")
        author = db.author_by_name(author_name)
        print(author)
    elif choice == '4':
        title = input('Enter book title: ')
        author_id = input("Enter author's id: ")
        genre_id = input("Enter genre's id: ")
        publication_date = input("Enter publication date: ")
        db.add_book(title, author_id, genre_id, publication_date)
    elif choice == 'exit':
        break


db.close()
