# RootsMagic
Python SQLite Interface to RootsMagic Database

## Author
Steve Turley, rsteventurley@gmail.com

## Version
For Version 10.0.7.0

## References
Data Dictionary\
https://sqlitetoolsforrootsmagic.com/rm9-data-dictionary/

Spreadsheet\
https://docs.google.com/spreadsheets/d/1VenU0idUAmkbA9kffazvj5RX_dZn6Ncn/edit?gid=552819953#gid=552819953

## Scripts
* `Explore.py` Checks structure of database against documented data dictionary.
    It has methods to list all tables, to list columns of a single table,
    and to list all columns of all tables.
* `AuditPlaces.py` Prints statistics about the contents of the PlaceTable table.