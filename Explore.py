import sqlite3  # Part of standard python library

filename = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10.rmtree'

def list_tables():
    conn = sqlite3.connect(filename)  # Throws error if file doesn't exist
    cursor = conn.cursor()
    cursor.execute("SELECT name from sqlite_master WHERE type = 'table'")
    table_list = cursor.fetchall()
    table_names = [t[0] for t in table_list]
    table_names.sort()
    for name in table_names:
        print(name)
    cursor.close()
    conn.close()

# I ran this code and verified that the list of tables matches
# the data dictionary at https://sqlitetoolsforrootsmagic.com/rm9-data-dictionary/

def list_table_columns(table: str, indent: int=0):
    conn = sqlite3.connect(filename)  # Throws error if file doesn't exist
    cursor = conn.cursor()
    result = cursor.execute(f"PRAGMA table_info('{table}')").fetchall()
    # [0] index (ignored)
    # [1] name
    # [2] type (INTEGER, TEXT, FLOAT, BLOB, BIGINT)
    # [3] notnull (if True, column must not be null)
    # [4] dflt_value (None or default value)
    # [5] pk (primary key if non-zero)
    column_names = list(zip(*result))[1]
    types = list(zip(*result))[2]
    max_len = max([len(name) for name in column_names])
    max_type = max([len(dtype) for dtype in types])
    for column in result:
        pad = ' ' * indent
        name = column[1].ljust(max_len)
        dtype = column[2].ljust(max_type)
        msg = ''
        if column[3]:
            msg += ' NOT NULL'
        if column[4] is not None:
            msg += f' DEFAULT({column[4]})'
        if column[5]:
            msg += ' PRIMARY KEY'
        print(pad, name, dtype, msg)
    cursor.close()
    conn.close()

def list_tables_and_columns():
    conn = sqlite3.connect(filename)  # Throws error if file doesn't exist
    cursor = conn.cursor()
    cursor.execute("SELECT name from sqlite_master WHERE type = 'table'")
    table_list = cursor.fetchall()
    # Close DB before calling other functions
    cursor.close()
    conn.close()
    table_names = [t[0] for t in table_list]
    table_names.sort()
    for name in table_names:
        print(name)
        list_table_columns(name, indent=5)

# list_tables()
# list_table_columns("PlaceTable")
list_tables_and_columns()