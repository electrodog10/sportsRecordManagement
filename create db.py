import peewee

database = peewee.SqliteDatabase("db.db")


########################################################################
class Activity(peewee.Model):
    """
    ORM model of the Artist table
    """
    name = peewee.CharField()

    class Meta:
        database = database


########################################################################
class Record(peewee.Model):
    """
    ORM model of album table
    """
    activity = peewee.ForeignKeyField(Activity)
    record = peewee.CharField()
    year = peewee.CharField()
    person = peewee.CharField()
    moreInfo = peewee.CharField()

    class Meta:
        database = database




if __name__ == "__main__":

    try:
        Record.create_table()
    except peewee.OperationalError:
        print "Album table already exists!"

