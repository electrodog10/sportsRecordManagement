import peewee

database = peewee.SqliteDatabase("db.db")


########################################################################
class Users(peewee.Model):
    email = peewee.CharField()
    passHash = peewee.CharField()
    person = peewee.CharField()
    class Meta:
        database = database


########################################################################
class Activity(peewee.Model):
    activityName = peewee.CharField()
    class Meta:
        database = database


########################################################################
class Record(peewee.Model):
    activity = peewee.ForeignKeyField(Activity, related_name='foreignField')
    record = peewee.CharField()
    year = peewee.CharField()
    person = peewee.CharField()
    number = peewee.CharField()
    moreInformation = peewee.CharField()

    class Meta:
        database = database


if __name__ == "__main__":
    try:
        Activity.create_table()
    except peewee.OperationalError:
        print "Artist table already exists!"

    try:
        Record.create_table()
    except peewee.OperationalError:
        print "Album table already exists!"