import peewee
import os

DB = peewee.SqliteDatabase(os.path.abspath('addresses.sqlite3'))


class Address(peewee.Model):
    name = peewee.CharField(null=False, unique=True)
    lat = peewee.FloatField()
    lng = peewee.FloatField()
    is_manual_corrected = peewee.BooleanField(default=False)

    class Meta:
        database = DB

    def manual_correct_address_coordinates(self, address, lat, lng, city='Новосибирск'):
        """
        Ручная корректировка адреса. Добавлена, для переназначения адресов в ручную,
        :param address: Адрес как в базе данных
        :param lat: долгота
        :param lng: широта
        :param city: город, так как в базе имена начинаются с названия города
        :return: Обновляет значения  широты и долготы, и удаляет все значения из таблицы дистанций
        """
        query = self.select().where(Address.name == f'{city} {address}')
        if query.exists():
            query_update = (self.update({Address.lat: lat, Address.lng: lng, Address.is_manual_corrected: True})
                            .where(Address.name == f'{city} {address}')
                            .execute())
            delete_old_query_distance = DistanceBetweenAddress.delete().where(
                (DistanceBetweenAddress.address_id == query.get().id) |
                (DistanceBetweenAddress.next_address_id == query.get().id))
            delete_old_query_distance.execute()

        else:
            raise Exception('Address does not exists')


class DistanceBetweenAddress(peewee.Model):
    address_id = peewee.ForeignKeyField(Address)
    next_address_id = peewee.ForeignKeyField(Address)
    distance = peewee.FloatField()
    is_manual_corrected = peewee.BooleanField(default=False)

    class Meta:
        database = DB


if not Address.table_exists() and not DistanceBetweenAddress.table_exists():
    Address.create_table()
    DistanceBetweenAddress.create_table()

