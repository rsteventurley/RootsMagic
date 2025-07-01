import sqlite3

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

class Event:
    def __init__(self, record: dict):
        self.ID = record['EventID']
        self.place = record['PlaceID']

def read_places(filename: str):
    with sqlite3.connect(filename) as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        result = cursor.execute("SELECT * from PlaceTable").fetchall()
    return result

def read_events(filename: str):
    with sqlite3.connect(filename) as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        result = cursor.execute("SELECT * from EventTable").fetchall()
    return result

file = 'C:/Users/hp/Documents/RootsMagic/deonandsteve10b.rmtree'
data = read_places(file)
places = [Place(row) for row in data if row['PlaceType'] == 0]
place_dict = {row['PlaceID']:Place(row) for row in data}
print(f"found {len(places)} user defined places")
print("\nFirst 10 user places:")
for p in places[:10]:
    print(p.name)
print("\nPlaces with fsID or anID != 0")
fs_zeroes = [Place(row) for row in data if row['fsID'] != 0 and row['fsID'] is not None]
an_zeroes = [Place(row) for row in data if row['anID'] != 0 and row['anID'] is not None]
print(f"\tfound {len(fs_zeroes)} FS places and {len(an_zeroes)} AN places")
# Check CREF of masterID on first element of fs_zeroes and an_zeroes (same)
first_fs = fs_zeroes[0]
# I'm not sure what master means in this case
master = [Place(row) for row in data if row['PlaceID'] == first_fs.masterID]
print(f"found {len(master)} place master matches")

# Check consistency between event places and PlaceTable
event_data = read_events(file)
events = [Event(row) for row in event_data]
missing_count = 0
for event in events:
    if event.place > 0 and event.place not in place_dict:
        missing_count += 1
print(f"\n{missing_count} events without corresponding places")

# Search for Sweden-like countries
s_set = set()
for place in places:
    country = place.name.split()[-1]
    # Add variations of Sweden, but not Switzerland
    if country.startswith(('Sw', 'Sv')) and not country.startswith('Swi'):
        s_set.add(country)

print(s_set)