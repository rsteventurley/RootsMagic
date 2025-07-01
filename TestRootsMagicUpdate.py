import sqlite3
import shutil
import datetime

def copy_file() -> str:
    file = 'data/rmtest.rmtree'
    copy = 'data/rmtest.sqlite'
    shutil.copyfile(file, copy)
    return copy

def open_db(file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(file)
    conn.enable_load_extension(True)
    conn.load_extension('extensions/unifuzz64.dll')
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn: sqlite3.Connection):
    conn.close()

def name_sort(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "SELECT NameID, Given, Surname, UTCModDate FROM NameTable ORDER BY Surname, Given"
    result = cursor.execute(sql).fetchall()
    cursor.close()
    print_names(result)

def place_sort(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sql = "SELECT PlaceID, Name FROM PlaceTable WHERE PlaceType=0 ORDER BY Name"
    result = cursor.execute(sql).fetchall()
    cursor.close()
    print_places(result)

def update_name(conn: sqlite3.Connection):
    cursor = conn.cursor()
    mod_date = (datetime.datetime.now(datetime.timezone.utc) -
                datetime.datetime(1899, 12, 30, 0, 0, 0, tzinfo=datetime.timezone.utc))
    mod_days = mod_date.total_seconds()/86400.0  # 86400 seconds in 24 hours
    sql = "UPDATE NameTable SET Given = ?, UTCModDate = ? WHERE NameID = ?"
    cursor.execute(sql, ("röbert staffan", mod_days, 2))
    conn.commit()
    cursor.close()

def print_names(rows: list[dict]):
    print("\nNames")
    for row in rows:
        mod_date = (datetime.timedelta(days = row['UTCModDate']) +
                    datetime.datetime(1899, 12, 30, 0, 0, 0, tzinfo=datetime.timezone.utc))
        local_date = mod_date.astimezone()
        print(f"{row['NameID']}: {row['Given']} {row['Surname']} {local_date}")

def print_places(rows: list[dict]):
    print("\nPlaces")
    for row in rows:
        print(f"{row['PlaceID']}: {row['Name']}")

filename = copy_file()
db = open_db(filename)
name_sort(db)
place_sort(db)
update_name(db)
name_sort(db)
close_db(db)