import os
from lab3_controller import tables, columns
      
  
def show_main_menu():
    print('''\nChoose what to do:
    1. Select
    2. Insert
    3. Delete
    4. Update
    5. Full text search
    6. Available books
    7. All books of author
    8. Random author
    9. Clear screen
    0. Exit''')
    
  
def fts_mode():
    print('''\nChose full text search mode: 
    1. Required word entry
    2. Word is not included
    0. Go back''')
    

def continue_or_back():
    print('''\nDo you want to continue or go back:
    1. Continue
    0. Go back''')
    
    
def print_or_back():
    print('''\nDo you want to output next results or go back:
    1. Output next
    0. Go back''')
    

def table_columns_names(table):
    table_columns = columns[tables[table]]
    for i in range(len(table_columns)):
        print(str(i+1) + ". " + table_columns[i])
    print("0. Go back")

    
def tables_names():
    print("\nChoose table:")
    for k, v in tables.items():
        print("{}. {}".format(k, v))
    print("0. Go back")
        
    
def print_table(table, notes):
    if not notes: 
        print('\nNo data')
        return
    print()
    table_columns = columns[tables[table]]
    for note in notes:
        for i in range(len(note)):
            print(table_columns[i] + ' -', note[i])           
        print('-'*40)      
 
 
def print_orm_table(notes):
    if not notes: 
        print('\nNo data')
        return
    for note in notes:
        print(note)         
        print('-'*40)    