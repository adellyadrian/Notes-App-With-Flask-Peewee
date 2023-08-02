from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, ForeignKeyField, AutoField
import sqlite3


db = SqliteDatabase('database.db')


class BaseModel(Model):  # Main Base Model Class
    class Meta:
        database = db


class Contact(BaseModel):  # Contact, that inherit BaseModel, has same Meta class, and table name with 6 parameters
    id = PrimaryKeyField(null=False)
    first_name = CharField(max_length=100, null=False)
    second_name = CharField(max_length=100, null=False)
    email = CharField(max_length=100, null=False)
    username = CharField(max_length=100, null=False)
    password = CharField(max_length=100, null=False)

    class Meta:
        table_name = 'contact'


class Notes(BaseModel):
    id = AutoField(primary_key=True, null=False)
    headline = CharField(max_length=100, null=False)
    content_post = CharField(max_length=100, null=False)

    class Meta:
        table_name = 'notes'
