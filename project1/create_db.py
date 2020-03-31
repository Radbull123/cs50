import csv
import os
from itertools import islice
from multiprocessing import Process, cpu_count
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_HOST = "ec2-54-217-235-87.eu-west-1.compute.amazonaws.com"
DATABASE_PASSWORD = "bd2994af1944f9d43cdadb812fbe00a3feafc364d4e8e3b4bc4d2f34cfb739e7"
DATABASE_PORT = "5432"
DATABASE_NAME = "datl6i34dlller"
DATABASE_USER = "cxirynyrhlcrxl"
os.environ["SECRET_KEY"] = '12!34sad5_56'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@"\
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

Model = declarative_base()


class User(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Books(Model):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    isbn = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(String, nullable=False)

    @staticmethod
    def import_the_books_from_csv(path_to_csv, start_line, end_line):
        with open(path_to_csv, 'r') as books_file:
            global db
            read_file = csv.reader(books_file)
            for isbn, title, author, year in islice(read_file, start_line, end_line):
                if db.query(Books).filter(Books.isbn == isbn).first() is None:
                    current_book = Books(isbn=isbn, title=title, author=author, year=year)
                    db.add(current_book)
                    print(f"The {title} Book successfully added")
                else:
                    break
            else:
                db.commit()


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Model.metadata.create_all(engine)

if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), 'books.csv'), 'r') as books_file:
        read_file = csv.reader(books_file)
        len_lines = len(list(read_file))
        line_divider = int(len_lines/cpu_count())
        args_list = list()
        for core in range(cpu_count()):
            first_line = len_lines - line_divider
            args_list.append((os.path.join(os.getcwd(), 'books.csv'), first_line, len_lines))
            len_lines -= line_divider

        worker_1 = Process(target=Books.import_the_books_from_csv, args=args_list[0])
        worker_2 = Process(target=Books.import_the_books_from_csv, args=args_list[1])
        worker_3 = Process(target=Books.import_the_books_from_csv, args=args_list[2])
        worker_4 = Process(target=Books.import_the_books_from_csv, args=args_list[3])
        worker_1.start()
        worker_2.start()
        worker_3.start()
        worker_4.start()
        worker_1.join()
        worker_2.join()
        worker_3.join()
        worker_4.join()
