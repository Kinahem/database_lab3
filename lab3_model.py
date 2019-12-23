import psycopg2
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

import tables

data_types = {'Author':['str', 'date', 'date'],
           'Books':['str', 'str', 'str', 'bool'],
           'Customers':['str', 'str', 'str'],
           'Publisher':['str', 'str'],
           'Author_Books':['str', 'str', 'date'],
           'Books_Customers':['str', 'date', 'money', 'str']
           }  

           
class Database():
    engine = None
    Base = tables.Base

    def __init__(self):
        try:
            url = "postgresql://postgres:qwerty@localhost:5432/Online_book_store"
            self.engine = db.create_engine(url)
            self.connection = self.engine.connect()
            #self.table_names = self.Base.metadata.tables.keys()
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            print(error)
            exit()
    
    
    def connect_db(self):
        try:
            Session = sessionmaker(bind=self.engine) 
            session = Session()  
            res = session
        except (Exception, psycopg2.Error) as error:
            res = False
            print(error)
        return res 
            
    
    def select(self, table):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        try:
            res = session.query(my_table).all()
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
    
    
    def insert(self, table, table_columns, values):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        dtype = data_types[table]
        for i in range(len(dtype)):
            if dtype[i] == 'bool':
                if values[i] in ['true', 'True', 'y', 'yes', '1']:
                    values[i] = True
                else:
                    values[i] = False
        new_row = my_table(*values)
        try:
            session.add(new_row)
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
        
        
    def delete(self, table, where = ""):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        filter = {f"{where[0]}" : f"{where[1]}"}
        try:
            session.query(my_table).filter_by(**filter).delete()
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
    
    
    def update(self, table, set = "", where = ""):
        session = self.connect_db()
        if not session: return False
        my_table = getattr(tables, table)
        filter = {f"{where[0]}" : f"{where[1]}"}
        values = {f"{set[0]}" : f"{set[1]}"}
        try:
            session.query(my_table).filter_by(**filter).update(values)
            res = True
        except (Exception, psycopg2.Error, SQLAlchemyError) as error:
            res = False
            print(error)
        session.commit()
        return res
   
   
def connect_db():
    try:
        res = psycopg2.connect(host="localhost", port="5432", 
                                database="Online_book_store", user="postgres", 
                                password='qwerty')
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    return res 

    
def select(table, fields = "*", where = ""):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT " + fields + " FROM " + table + ' ' + where)
        res = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res
    

def random_author(num):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("insert into author (author_pen_name, born, died) select * FROM rand_author({})".format(num))
        res = True
    except (Exception, psycopg2.Error) as error:
        res = False
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res

    
def full_text_search(table, where, mode):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        if mode == '1':
            cursor.execute("select * from {} where {}".format(table, where))
            res = cursor.fetchall()
        elif mode == '2':
            cursor.execute("select * from {} where not ({})".format(table, where))
            res = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        res = None
        print(error)
    conn.commit()
    cursor.close()
    conn.close()
    return res



    

# select_stmt = select([user_table.c.username, user_table.c.fullname]).\
            # where(user_table.c.username == 'ed')

#result = engine.execute("select title from books")
            


    
    
# if __name__ == "__main__":
    # my_db = Database()
    # print(my_db.get_from_table(tables.Publisher))
    
if __name__ == "__main__":
    res = connect_db()
    if not res: exit()
    engine, session, metadata = res
    books = db.Table('books', metadata, autoload=True, autoload_with=engine)
    # session.execute(books.insert().values({'title': "some name", 'genre': "some genre", 
                           # 'publisher': "Hachette Livre", 'available': 1}))
    #query1 = db.delete(books).where(books.c['title'] == 'some name')
    query1 = db.update(books, values={books.c['genre']: 'b'}).\
                where(books.c['title'] == 'd')
    query = db.select([books]).where(books.c['available'] == '1')
    session.execute(query1)
    try:
        res_proxy = session.execute(query)
    except (Exception, psycopg2.Error, SQLAlchemyError) as error:
        print(error)
        exit()
    res_set = res_proxy.fetchall()
    for i in res_set:
        print(i)
    session.commit()
    session.close()
        
        