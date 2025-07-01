import sqlite3
import os
import shutil
import datetime

class Place:
    def __init__(self, record: dict):
        self.ID = record['PlaceID']
        self.type = record['PlaceType'] # 0 from EditPerson, 1 LDS Temple, 2 Details
        self.name = record['Name']
        self.abbrev = record['Abbrev']
        self.norm = record['Normalized']
        self.latitude = record['Latitude']
        self.longitude = record['Longitude']
        self.masterID = record['MasterID'] # main place if detail place (2)
        self.note = record['Note']
        self.fsID = record['fsID']  # FamilySearch ID?
        self.anID = record['anID']  # Ancestry ID?
        self.modified = record['UTCModDate']  # Julian modification date
        self.reverse = record['Reverse']

class Event:
    def __init__(self, record: dict):
        self.ID = record['EventID']
        self.place = record['PlaceID']

def read_places(db: sqlite3.Connection):
    cursor = db.cursor()
    result = cursor.execute("SELECT * from PlaceTable").fetchall()
    cursor.close()
    return result

def read_events(db: sqlite3.Connection):
    cursor = db.cursor()
    result = cursor.execute("SELECT * from EventTable").fetchall()
    cursor.close()
    return result

def event_index(ev: list[Event]) -> dict[int, list[int]]:
    edict: dict[int, list[int]] = {}
    for e in ev:
        event_place = e.place
        if event_place > 0:
            if event_place in edict:
                edict[event_place].append(e.ID)
            else:
                edict[event_place] = [e.ID]
    return edict

def abbreviated_swedish_events(all_places: list[Place]) -> list[Place]:
    matches: list[Place] = []
    for abbreviated_place in all_places:
        country = abbreviated_place.name.split(',')[-1].strip()
        # Add variations of Sweden, but not Switzerland
        if country.startswith(('Sw', 'Sv')) and not country.startswith('Swi'):
            if country != "Sweden" and len(country.split()) ==1:
                matches.append(abbreviated_place)
    return matches

def abbreviated_jönköping_events(all_places: list[Place]) -> list[Place]:
    matches: list[Place] = []
    for pl in all_places:
        parts = pl.name.split(',')
        if len(parts) < 2:
            continue
        country = parts[-1].strip()
        if country == "Sweden":
            land = parts[-2].strip()
            if land.startswith(('Jo', 'Jn', 'Jönköpings')):
                matches.append(pl)
    return matches

def replace_country(abbrev_place: Place, db: sqlite3.Connection):
    old_location = abbrev_place.name
    parts = [p.strip() for p in old_location.split(',')]
    parts[-1] = "Sweden"
    new_location = ', '.join(parts)
    parts.reverse()
    reverse = ', '.join(parts)
    pid = abbrev_place.ID
    cursor = db.cursor()
    mod_date = (datetime.datetime.now(datetime.timezone.utc) -
                datetime.datetime(1899, 12, 30, 0, 0, 0, tzinfo=datetime.timezone.utc))
    mod_days = mod_date.total_seconds()/86400.0  # 86400 seconds in 24 hours
    sql = """
        UPDATE PlaceTable
        SET Name = ?, 
        Reverse = ?,
        UTCModDate = ?
        WHERE PlaceID = ?;
    """
    cursor.execute(sql, (new_location, reverse, mod_days, pid))
    # This sets the Reverse field to null forcing RM to reverse the places
    # again the next time that is requested.
    cursor.close()

def replace_county(abbrev_place: Place, db: sqlite3.Connection):
    old_location = abbrev_place.name
    parts = [loc.strip() for loc in old_location.split(',')]
    parts[-2] = 'Jönköping'
    new_location = ', '.join(parts)
    parts.reverse()
    reverse = ', '.join(parts)
    pid = abbrev_place.ID
    cursor = db.cursor()
    mod_date = (datetime.datetime.now(datetime.timezone.utc) -
                datetime.datetime(1899, 12, 30, 0, 0, 0, tzinfo=datetime.timezone.utc))
    mod_days = mod_date.total_seconds()/86400.0  # 86400 seconds in 24 hours
    sql = """
        UPDATE PlaceTable
        SET Name = ?, 
        Reverse = ?,
        UTCModDate = ?
        WHERE PlaceID = ?;
    """
    cursor.execute(sql, (new_location, reverse, mod_days, pid))
    # This sets the Reverse field to null forcing RM to reverse the places
    # again the next time that is requested.
    cursor.close()

def copied_file() -> str:
    file = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10.rmtree'
    copy = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10b.rmtree'
    if os.path.exists(copy):
        os.remove(copy)
    shutil.copyfile(file, copy)
    return copy

def open_db() -> sqlite3.Connection:
    file_copy = copied_file()
    db = sqlite3.connect(file_copy)
    db.enable_load_extension(True)
    db.load_extension('extensions/unifuzz64.dll')
    db.row_factory = sqlite3.Row
    return db

conn = open_db()
data = read_places(conn)
places = [Place(row) for row in data if row['PlaceType'] == 0]
place_dict = {row['PlaceID']:Place(row) for row in data}

event_data = read_events(conn)
events = [Event(row) for row in event_data]
event_dict = event_index(events)

abbrev_places = abbreviated_swedish_events(places)
if len(abbrev_places) > 0:
    print("replacing countries")
    for place in abbrev_places:
        replace_country(place, conn)
    conn.commit()
    # Reread places
    data = read_places(conn)
    places = [Place(row) for row in data if row['PlaceType'] == 0]
    place_dict = {row['PlaceID']:Place(row) for row in data}

abbrev_places = abbreviated_jönköping_events(places)
if len(abbrev_places) > 0:
    print("replacing counties")
    for item, place in enumerate(abbrev_places):
        print(f"updating {item}: {place.name}")
        replace_county(place, conn)
    conn.commit()

conn.close()