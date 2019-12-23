import os
import re

tables = {'1':'Author', 
          '2':'Books', 
          '3':'Customers', 
          '4':'Publisher',
          '5':'Author_Books',
          '6':'Books_Customers'
          }

columns = {'Author':['author_pen_name', 'born', 'died'],
           'Books':['title', 'genre', 'publisher', 'available'],
           'Customers':['name', 'phone_number', 'email'],
           'Publisher':['title', 'address'],
           'Author_Books':['book_title', 'author_pen_name', 'publication_date'],
           'Books_Customers':['customer', 'purchase_date', 'price', 'book_title']
           }

fts_columns = {'Author':['author_pen_name'],
               'Books':['title', 'genre', 'publisher'],
               'Customers':['name', 'email'],
               'Publisher':['title', 'address'],
               'Author_Books':['book_title', 'author_pen_name'],
               'Books_Customers':['customer', 'book_title']
               }
              

import lab3_model as model
import lab3_view as view

DB = model.Database()
              
def available_books():
    return(model.select("books, author, author_books", "author.author_pen_name, books.title", 
                        "WHERE books.available = 'true' AND author_books.book_title = books.title \
                         AND author_books.author_pen_name = author.author_pen_name"))

                         
def book_of_author(author_pen_name, bool):
    for name in author_pen_name:
        try:
            yield model.select("books, author, author_books", "author.author_pen_name, books.title", 
                            "WHERE (books.available = '1' OR books.available = '{}') \
                             AND author_books.book_title = books.title \
                             AND author_books.author_pen_name = author.author_pen_name \
                             AND (author.author_pen_name ILIKE '{}' \
                             OR author.author_pen_name ILIKE '{}')".format(bool, name.strip() + " %", "% " + name.strip()))
        except (Exception, psycopg2.Error) as error:
            print(error)
            return
                    
                
def insert_into_table(table_num):
    table = tables[table_num]
    table_columns = columns[table]
    values = []
    try:
        for i in range(len(table_columns)):
            answer = input(table_columns[i] + ' = ')
            values.append(answer)
    except Exception as error:
        print(error)
        return
    print("INSERT INTO " + table + " VALUES(" + ', '.join(values) + ')')
    view.continue_or_back()
    continue_or_back = input() 
    if continue_or_back == '1':
        res = DB.insert(table, table_columns, values)
        return res
    elif continue_or_back == '0':
        return
    else:
        print("No such option. Check your input")
        
        
def delete_from_table(table_num):
    table = tables[table_num]
    table_columns = columns[table]
    while True:
        print("Choose column to delete by:")
        view.table_columns_names(table_num)
        chosen_column_num = input()
        if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
            chosen_column = table_columns[int(chosen_column_num)-1]
            print("Input value: ")
            print("DELETE FROM {} WHERE {} = ...".format(table, chosen_column))
            value = input()
            print("DELETE FROM {} WHERE {} = {}".format(table, 
                   chosen_column, value))
            view.continue_or_back()
            continue_or_back = input() 
            if continue_or_back == '1':
                where = [chosen_column, value]
                res = DB.delete(table, where)
                return res
            elif continue_or_back == '0':
                return
            else:
                print("No such option. Check your input")
        elif chosen_column_num == '0':
            return
        else:
            print("No such option. Check your input")

            
def update_table(table_num):
    table = tables[table_num]
    table_columns = columns[table]
    while True:
        print("Choose column to update:")
        view.table_columns_names(table_num)
        chosen_column_num = input()
        if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
            set_column = table_columns[int(chosen_column_num)-1]
            print("Input value: ")
            print("UPDATE {} SET {} = ...".format(table, set_column))
            set_value = input()
            print("Choose column to update by:")
            view.table_columns_names(table_num)
            chosen_column_num = input()
            if re.match(r'^[1-{}]{}$'.format(len(table_columns), "{1}"), 
                    chosen_column_num):
                where_column = table_columns[int(chosen_column_num)-1]
                print("Input value: ")
                print("UPDATE {} SET {} = {} WHERE {} = ...".format(table, 
                      set_column, set_value, where_column))
                where_value = input()
                print("UPDATE {} SET {} = {} WHERE {} = {}".format(table, 
                      set_column, set_value, where_column, where_value))
                view.continue_or_back()
                continue_or_back = input() 
                if continue_or_back == '1':
                    set = [set_column, set_value]
                    where = [where_column, where_value]
                    res = DB.update(table, set, where)
                    return res
                elif continue_or_back == '0':
                    return
                else:
                    print("No such option. Check your input")
            elif chosen_column_num == '0':
                return
            else:
                print("No such option. Check your input")       
        elif chosen_column_num == '0':
            return
        else:
            print("No such option. Check your input")       
  
  
def fts_table(text, mode, table_num):
    table = tables[table_num]
    to_tsvector = fts_columns[table]
    where = ' || '.join("to_tsvector(coalesce({}, ''))".format(w) 
                   for w in to_tsvector)
    where += " @@ plainto_tsquery('{}')".format(text)
    return(model.full_text_search(table, where, mode))
        
  
def main_menu():
    while True:
        view.show_main_menu()
        option = input()
        if re.match(r'^[1-5]{1}$', option):
            while True:
                    view.tables_names()
                    chosen_table = input()
                    if re.match(r'^[1-6]{1}$', chosen_table):
                        table = tables[chosen_table]
                        if option == '1':
                            notes = DB.select(table)
                            view.print_orm_table(notes)
                        elif option == '2':
                            res = insert_into_table(chosen_table)
                            if not res:
                                print("Data wasn't inserted")
                            else:
                                print("Successfully inserted")
                        elif option == '3':
                            res = delete_from_table(chosen_table)
                            if not res:
                                print("Data wasn't deleted")
                            else:
                                print("Operation successfull")
                        elif option == '4':
                            res = update_table(chosen_table)
                            if not res:
                                print("Data wasn't updated")
                            else:
                                print("Operation successfull")
                        elif option == '5':
                            text = input("Input text to search: ")
                            view.fts_mode()
                            mode = input()
                            if re.match(r'^[1,2]{1}$', mode):
                                notes = fts_table(text, mode, chosen_table)
                                view.print_table(chosen_table, notes) 
                            elif continue_or_back == '0':
                                break
                            else:
                                print("No such option. Check your input")
                    elif chosen_table == '0':
                        break
                    else:
                        print("No such option. Check your input")
                    view.continue_or_back()
                    continue_or_back = input()
                    if continue_or_back == '1':
                        continue
                    elif continue_or_back == '0':
                        break
                    else:
                        print("No such option. Check your input")
        elif option == '6':
            view.print_table('2', available_books())            
        elif option == '7':
            author = input("Input authors names separated with comma: ")
            author = author.split(',')
            bool = input("Output only available books? (y/n): ")
            for book_list in book_of_author(author, bool):
                view.print_table('2', book_list)
        elif option == '8':
            num_of_rand = input("How many random authors insert?\n")
            res = model.random_author(num_of_rand)
            if not res:
                print("Data wasn't updated")
            else:
                print("Successfully updated")
        elif option == '9':
            os.system("cls")
        elif option == '0':
            exit()
        else:
            print("No such option. Check your input")
      
    
if __name__ == "__main__":
    main_menu()