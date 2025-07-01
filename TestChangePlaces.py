import sqlite3
import shutil
import os

def copy_file() -> str:
    file = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10.rmtree'
    file_copy = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10b.rmtree'
    if os.path.exists(file_copy):
        os.remove(file_copy)
    shutil.copyfile(file, file_copy)
    return file_copy

def open_db(file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(file)
    conn.enable_load_extension(True)
    conn.load_extension('extensions/unifuzz64.dll')
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn: sqlite3.Connection):
    conn.close()

def place_sort(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "SELECT PlaceID, Name FROM PlaceTable WHERE PlaceType=0 AND Name LIKE ? ORDER BY Name LIMIT 10"
    result = cursor.execute(sql, ("%Sweden",)).fetchall()
    cursor.close()
    print_places(result)

def update_place(conn: sqlite3.Connection):
    print("\nupdating place")
    cursor = conn.cursor()
    sql = "UPDATE PlaceTable SET Name = ?, Reverse = ? WHERE PlaceID = ?"
    cursor.execute(sql, ("Arsio Norregard, Jönköping, Sweden",
                         "Sweden, Jönköping, Arsio Norregard", 2043))
    conn.commit()
    cursor.close()

def print_places(rows: list[dict]):
    print("\nPlaces")
    for row in rows:
        print(f"{row['PlaceID']}: {row['Name']}")

def check_reverse():
    file_copy = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10b.rmtree'
    conn = open_db(file_copy)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "SELECT Reverse FROM PlaceTable WHERE PlaceID = 2043"
    result = cursor.execute(sql).fetchall()
    print('Reverse is',result[0]['Reverse'])
    cursor.close()
    conn.close()

check_reverse()
filename = copy_file()
db = open_db(filename)
place_sort(db)
update_place(db)
place_sort(db)
close_db(db)