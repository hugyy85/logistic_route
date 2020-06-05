import peewee
from playhouse.migrate import *


DB = peewee.SqliteDatabase('../addresses.sqlite3')
migrator = SqliteMigrator(DB)

is_manual_corrected = peewee.BooleanField(default=False)

column_name = 'is_manual_corrected'
migrate(
    migrator.add_column('Address', column_name, is_manual_corrected),
    migrator.add_column('DistanceBetweenAddress', column_name, is_manual_corrected)
)

print(f'MIGRATION: add column {column_name} at table Address')
print(f'MIGRATION: add column {column_name} at table DistanceBetweenAddress')