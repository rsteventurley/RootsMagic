import sqlite3
import os

def empty_file() -> str:
    file = 'data/testcase.sqlite'
    if os.path.exists(file):
        os.remove(file)
    return file

def open_db(file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(file)
    conn.enable_load_extension(True)
    conn.load_extension('extensions/unifuzz64.dll')
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn: sqlite3.Connection):
    conn.close()

def create_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = """CREATE TABLE person (
        ID INT PRIMARY KEY,
        Name TEXT COLLATE RMNOCASE,
        Age BIGINT,
        Birthplace TEXT COLLATE RMNOCASE,
        Dead INT DEFAULT 0);"""
    cursor.execute(sql)
    sql = "INSERT INTO person (ID, Name, Age, Birthplace) VALUES(?, ?, ?, ?)"
    sql2 = "INSERT INTO person (ID, Name, Age, Birthplace, Dead) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, (1, "Steve Turley", 71, "Monterey Park"))
    cursor.execute(sql, (2, "Deon Turley", 69, "Palo Alto"))
    cursor.execute(sql2, (7, "Robert Starling Turley", 95, "glendive", True))
    cursor.execute(sql, (9, "robert staffan turley", 46, "Stoneham"))
    cursor.execute(sql, (11, "robert wilson turley", 24, "Altoona"))
    cursor.execute(sql, (13, "röbert staffan turley", 47, "Windham"))
    cursor.execute(sql, (15, "rubert staffan turley", 49, "California"))
    conn.commit()
    cursor.close()

def name_sort(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "SELECT ROWID, * FROM person ORDER BY Name"
    result = cursor.execute(sql).fetchall()
    cursor.close()
    print_rows("Sorted by Name", result)

def place_sort(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "SELECT ROWID, * FROM person ORDER BY Birthplace"
    result = cursor.execute(sql).fetchall()
    cursor.close()
    print_rows("Sorted by Place", result)

def update_name(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "UPDATE person SET Name = ? WHERE ID = ?"
    cursor.execute(sql, ("röbert staffan turley", 9))
    conn.commit()
    cursor.close()

def print_rows(title: str, rows: list[dict]):
    print(f"\n{title}")
    for row in rows:
        print(f"{row['ROWID']} ID:{row['ID']:<2} Name:{row['Name']:<22} Place:{row['Birthplace']}")

filename = empty_file()
db = open_db(filename)
create_db(db)
name_sort(db)
place_sort(db)
update_name(db)
name_sort(db)
close_db(db)