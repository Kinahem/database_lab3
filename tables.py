import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    author_pen_name = db.Column(db.String, primary_key=True)
    born = db.Column(db.DateTime)
    died = db.Column(db.DateTime)
    
    books_of_author = db.orm.relationship("Books", secondary="author_books")
    
    def __init__(self, author_pen_name, born, died):
        self.author_pen_name = author_pen_name
        self.born = born
        self.died = died
    
    def __repr__(self):
        return (f'author_pen_name - {self.author_pen_name}\n'
                f'born - {self.born}\n'
                f'died - {self.died}')
                           

class Books(Base):
    __tablename__ = 'books'
    title = db.Column(db.String, primary_key=True)
    genre = db.Column(db.String)
    publisher = db.Column(db.String, db.ForeignKey('publisher.title'))
    available = db.Column(db.Boolean)
    
    author_of_book = db.orm.relationship("Author", secondary="author_books")
    customer_of_book = db.orm.relationship("Customers", secondary="books_customers") 
    
    def __init__(self, title, genre, publisher, available):
        self.title = title
        self.genre = genre
        self.publisher = publisher
        self.available = available
    
    def __repr__(self):
        return (f'title - {self.title}\n'
                f'genre - {self.genre}\n'
                f'publisher - {self.publisher}\n'
                f'available - {self.available}')
                    
                
class Customers(Base):
    __tablename__ = 'customers'
    name = db.Column(db.String, primary_key=True)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)

    book_of_customer = db.orm.relationship("Books", secondary="books_customers") 
    
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email
    
    def __repr__(self):
        return (f'name - {self.name}\n'
                f'phone_number - {self.phone_number}\n'
                f'email - {self.email}')
 
 
class Publisher(Base):
    __tablename__ = 'publisher'
    title = db.Column(db.String, primary_key=True)###
    address = db.Column(db.String)
    
    def __init__(self, title, address):
        self.title = title
        self.address = address
    
    def __repr__(self):
        return (f'title - {self.title}\n'
                f'address - {self.address}')
 
 
class Author_Books(Base):
    __tablename__ = 'author_books'    
    author_pen_name = db.Column(db.String, db.ForeignKey('author.author_pen_name'))
    book_title = db.Column(db.String, db.ForeignKey('books.title'))
    publication_date = db.Column(db.DateTime)
    
    author_of_book = db.orm.relationship(Author, backref=db.orm.backref('author_books', cascade="all, delete-orphan"))
    books_of_author = db.orm.relationship(Books, backref=db.orm.backref('author_books', cascade="all, delete-orphan"))
    
    __table_args__ = (db.PrimaryKeyConstraint('author_pen_name', 'book_title', name='author_books_pkey'),)
    
    def __init__(self, author_pen_name, book_title, publication_date):
        self.author_pen_name = author_pen_name
        self.book_title = book_title
        self.publication_date = publication_date
    
    def __repr__(self):
        return (f'author_pen_name - {self.author_pen_name}\n'
                f'book_title - {self.book_title}\n'
                f'publication_date - {self.publication_date}')
 
 
class Books_Customers(Base):
    __tablename__ = 'books_customers'
    customer = db.Column(db.String, db.ForeignKey('customers.name'))
    purchase_date = db.Column(db.DateTime)
    price = db.Column(db.Numeric)
    book_title = db.Column(db.String, db.ForeignKey('books.title'))

    customer_of_book = db.orm.relationship(Customers, backref=db.orm.backref('books_customers', cascade="all, delete-orphan"))
    book_of_customer = db.orm.relationship(Books, backref=db.orm.backref('books_customers', cascade="all, delete-orphan"))
    
    __table_args__ = (db.PrimaryKeyConstraint('customer', 'book_title', name='books_customers_pkey'),)
    
    def __init__(self, customer, purchase_date, price, book_title):
        self.customer = customer
        self.purchase_date = purchase_date
        self.price = price
        self.book_title = book_title
    
    def __repr__(self):
        return (f'customer - {self.customer}\n'
                f'purchase_date - {self.purchase_date}\n'
                f'price - {self.price}\n'
                f'book_title - {self.book_title}')
 
 