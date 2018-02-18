#import required libraries
import peewee
from flask import Flask, render_template, request, url_for, redirect
#import WTforms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import flask_login
from passlib.hash import pbkdf2_sha256
#from Flask_Login import LoginManager, login_user, login_required, logout_user
#initalize flask stuff
app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f37567d441f2b6176a'
#connect Peewee to our Sqlite database
database = peewee.SqliteDatabase("db.db")


#####################     Login Stuff   ###################################
def hashPass(plainText):
    hash = pbkdf2_sha256.hash(plainText)
    return hash

#add to database
def addUser(name,emailIn,passIn):
    from models import Users
    #hash the password like grandma makes a hashbrown egg dish
    hash = hashPass(passIn)
    #create user
    user = Users.create(email = emailIn,
                        passHash = hash,
                        person = name
                        )
    user.save()
def checkuserExists(emailIn):
    from models import Users
    #see if email exists in database
    user = Users.select().where(Users.email == emailIn)
    if user.exists():
        #if the user exists flag it as true
        flag = True
    else:
        #if the user doesn't exist flag them at not existing
        flag = False
    return flag
def getUser(id):
    from models import Users
    user = Users.select().where(Users.id == id).get()
    #create the inner dictionary
    innerString={}
    #create an innner dictionary key and value based on database and classes defined in models.py
    innerString["name"] = user.person
    innerString['email']= user.email
    innerString['id'] = user.id

    return innerString
def checkPW(email,password):
    from models import Users
    user = Users.select().where(Users.email == email).get()
    hash = user.passHash
    if pbkdf2_sha256.verify(password, hash) == True:
        flag = True
    else:
        flag = False
    return flag
def changeUser(field, valueIn, urlPassed):
    #import the Activity from models.py
    from models import Users
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    user = Users.select().where(Users.id == urlPassed).get()
    #modify values based on database and classes defined in models.py
    if field == "name":
        user.person = valueIn
        user.save()
    if field == "email":
        user.email = valueIn
        user.save()
    if field == "password":
        hash = hashPass(valueIn)
        user.passHash = hash
        user.save()

def deleteUser(urlPassed):
    from models import Users
    user = Users.get(Users.id==urlPassed)
    user.delete_instance()
#addUser('lewis@lewisproductions.com','lions')
#getUser('lewis@lewisproductions.com','lions')
#flask login  initialization
login_manager = flask_login.LoginManager()

login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if checkuserExists(email) != True:
        return

    user = User()
    user.id = email
    return user



#####################     Classes   ####################################
class editForm(FlaskForm):
    name = StringField('Name')
    activity = StringField('Activity')
    record = StringField('Record')
    year = StringField('Year')
    number = StringField('Number')
    moreInfo = StringField('More Information')
    password = StringField('Password')
    email = StringField('Email')
    search = StringField('Search')


#####################     Functions   ####################################
def showAll():
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    #start dictionary
    bigDictionary = {}
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for rawActivity in Record.select().join(Activity):
        #create the inner dictionary
        innerString={}
        #create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity']=rawActivity.activity.activityName
        innerString["record"]=rawActivity.record
        innerString["number"]=rawActivity.number
        innerString["year"]=rawActivity.year
        innerString["moreInformation"]=rawActivity.moreInformation
        innerString["id"]=rawActivity.id
        #add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x:innerString})
        x = x + 1

    # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
    # return the dictionary
    return bigDictionary
#searchDatabase based on activity passed
def searchDBActivity(urlPassed):
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    #start dictionary
    bigDictionary = {}
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for rawActivity in Record.select().join(Activity).where(Activity.activityName == urlPassed):
        #create the inner dictionary
        innerString={}
        #create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity']=rawActivity.activity.activityName
        innerString["record"]=rawActivity.record
        innerString["number"]=rawActivity.number
        innerString["year"]=rawActivity.year
        innerString["moreInformation"]=rawActivity.moreInformation
        innerString["id"]=rawActivity.id
        #add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x:innerString})
        x = x + 1

# searchDatabase based on activity passed
def search(urlPassed):
    # import the Activity and Record model from models.py
    from models import Activity, Record
    # start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    # start dictionary
    bigDictionary = {}
    # search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for rawActivity in Record.select().join(Activity).where(Record.person.contains(urlPassed)):

        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.activityName==urlPassed)
    for rawActivity in Record.select().join(Activity).where((Activity.activityName.contains(urlPassed)) & (Record.person.contains('Joe'))):

        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.record.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.number.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.year.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.moreInformation.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    return bigDictionary
# searchDatabase based on activity passed
def searchFilteredActivity(activityin,urlPassed):
    # import the Activity and Record model from models.py
    from models import Activity, Record
    # start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    # start dictionary
    bigDictionary = {}
        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.activityName==urlPassed)
    for rawActivity in Record.select().join(Activity).where(Record.person.contains(urlPassed)):

        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        if activityin == rawActivity.activity.activityName:
            bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.record.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        if activityin == rawActivity.activity.activityName:
            bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.number.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        if activityin == rawActivity.activity.activityName:
            bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.year.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        if activityin == rawActivity.activity.activityName:
            bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    for rawActivity in Record.select().join(Activity).where(Record.moreInformation.contains(urlPassed)):
        # create the inner dictionary
        innerString = {}
        # create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity'] = rawActivity.activity.activityName
        innerString["record"] = rawActivity.record
        innerString["number"] = rawActivity.number
        innerString["year"] = rawActivity.year
        innerString["moreInformation"] = rawActivity.moreInformation
        innerString["id"] = rawActivity.id
        # add this smaller dictionary to our bigger dictionary (and increase the counter)
        if activityin == rawActivity.activity.activityName:
            bigDictionary.update({x: innerString})
        x = x + 1

        # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
        # return the dictionary
    return bigDictionary
#searchDatabase based on activity passed
def searchDBActivity(urlPassed):
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    #start dictionary
    bigDictionary = {}
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for rawActivity in Record.select().join(Activity).where(Activity.activityName == urlPassed):
        #create the inner dictionary
        innerString={}
        #create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity']=rawActivity.activity.activityName
        innerString["record"]=rawActivity.record
        innerString["number"]=rawActivity.number
        innerString["year"]=rawActivity.year
        innerString["moreInformation"]=rawActivity.moreInformation
        innerString["id"]=rawActivity.id
        #add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x:innerString})
        x = x + 1

    # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
    # return the dictionary
    return bigDictionary
def displaybyID(idIn):
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    #start dictionary
    bigDictionary = {}
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for rawActivity in Record.select().where(Record.id == idIn):
        #create the inner dictionary
        innerString={}
        #create an innner dictionary key and value based on database and classes defined in models.py
        innerString["name"] = rawActivity.person
        innerString['activity']=rawActivity.activity.activityName
        innerString["record"]=rawActivity.record
        innerString["number"]=rawActivity.number
        innerString["year"]=rawActivity.year
        innerString["moreInformation"]=rawActivity.moreInformation
        innerString["id"]=rawActivity.id
        #add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x:innerString})
        x = x + 1
    # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
    # return the dictionary
    return bigDictionary
def getactivityName(urlPassed):
    from models import Activity, Record
    record = Record.select().where(Record.id == urlPassed).get()
    name = record.activity.activityName
    return name
def changeRecord(id,name,activity,record,year,number,moreInfo):
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    rawActivity = Record.select().where(Record.id == id).get()
    #get the id of the activity that was changed
    newactivityID = Activity.get(Activity.activityName == activity)

        #modify values based on database and classes defined in models.py
    if name != "None" or "" or None:
        rawActivity.person = name
        rawActivity.save()
    if activity != "None" or "" or None:
        rawActivity.activity_id = newactivityID.id
        rawActivity.save()
    if record != "None" or "" or None:
        rawActivity.record = record
        rawActivity.save()
    if number != "None" or "" or None:
        rawActivity.number = number
        rawActivity.save()
    if year != "None" or "" or None:
        rawActivity.year = year
        rawActivity.save()
    if moreInfo != "None" or "" or None:
        rawActivity.moreInformation = moreInfo
        rawActivity.save()

def addRecord(nameIn,activityIn,recordIn,yearIn,numberIn,moreInfoIn):
    #import the Activity and Record model from models.py
    from models import Activity, Record
    #get the ID of the record that is selected
    activityID = Activity.get(Activity.activityName == activityIn)
    #create record
    record = Record.create(person = nameIn,
                    activity = activityID.id,
                    record = recordIn,
                    number = numberIn,
                    year = yearIn,
                    moreInformation = moreInfoIn)
    record.save()



    #    rawActivity.activity.activityName = activity
    #    rawActivity.update()



def changeActivity(urlPassed, name):
    #import the Activity from models.py
    from models import Activity
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    rawActivity = Activity.select().where(Activity.activityName == urlPassed).get()
        #modify values based on database and classes defined in models.py

    if name != "None" or "" or None:
        rawActivity.activityName = name
        rawActivity.save()
def getActivities():
    from models import Activity
#below is to create a new one
    # new_activity = Activity.create(name="Water Polo")
    # create a list. A dictionary isn't needed because we only have one type of values
    activitiesList = []
    #iterate through activities in database
    for Activity in Activity.select():
        #get activity name and add it to list
        activityName = Activity.activityName
        activitiesList.append(activityName)
    #return the activity list in a list format
    return activitiesList
def getUsers():
    #import the Activity and Record model from models.py
    from models import Users
    #start counter for dictionary so it can increrase the key for the bigger dictionary that contains individual dictionaries
    x = 0
    #start dictionary
    bigDictionary = {}
    #search for record based on activity name. Iterate through to get all values. Activity is a Foreign key so note special handling for that
    for user in Users.select():
        #create the inner dictionary
        innerString={}
        #create an innner dictionary key and value based on database and classes defined in models.py
        innerString["id"] = user.id
        innerString['email']=user.email
        innerString['person']=user.person
        #add this smaller dictionary to our bigger dictionary (and increase the counter)
        bigDictionary.update({x:innerString})
        x = x + 1

    # stuff for getting foreign key. This is so when I forget I can look back here. recordforActivity = Record.get(Record.activity.name==urlPassed)
    # return the dictionary
    return bigDictionary
def deleteActivity(activityIn):
    from models import Activity
    recordtoDelete = Activity.get(Activity.activityName==activityIn)
    recordtoDelete.delete_instance()
def deleteRecord(id):
    from models import Record
    recordtoDelete = Record.get(Record.id==id)
    recordtoDelete.delete_instance()
def addActivity(activityIn):
    from models import Activity
    activity = Activity.create(activityName=activityIn)
    activity.save()

#####################     Flask Routes   ####################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    if checkPW(email,password) == True:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/protected')
@flask_login.login_required
def protected():
    return redirect(url_for('admin'))
    #flask_login.current_user.id


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))



#route for index
@app.route('/', methods=['GET', 'POST'])

def index():
    #call activities function
    activitiesList = getActivities()
    #return index template and pass activities to show up
    return render_template('index.html', activities=activitiesList)

@app.route('/admin/users', methods=['GET', 'POST'])
@flask_login.login_required
def users():
    #call activities function
    users = getUsers()
    #return index template and pass activities to show up
    return render_template('users.html', users=users)

@app.route('/admin/user/<urlPassed>', methods=['GET', 'POST'])
@flask_login.login_required
def editUser(urlPassed):
    form = editForm()
    databaseQuery = getUser(urlPassed)
    if request.method == 'POST':
        name = form.name.data
        if name != '':
            changeUser('name',name,urlPassed)
        email = form.email.data
        if email != '':
            changeUser('email', email, urlPassed)
        password = form.password.data
        if password != '':
            changeUser('password', password, urlPassed)
        return redirect(url_for('users'))
    return render_template('edituser.html', databaseQuery=databaseQuery, form=form)
@app.route('/admin/user/new', methods=['GET', 'POST'])
@flask_login.login_required
def newUser():
    form = editForm()
    if request.method == 'POST':
        name = form.name.data
        if name == '':
            return "Please fill out the name field. Press the back button in your browser to return."
        email = form.email.data
        if email == '':
            return "Please fill out the email field. Press the back button in your browser to return."
        password = form.password.data
        if password == '':
            return "Please fill out the password field. Press the back button in your browser to return."
        addUser(name,email,password)
        return redirect(url_for('users'))
    return render_template('newuser.html', form=form)

#delete activity
@app.route('/admin/user/delete/<urlPassed>')
@flask_login.login_required
def deleteuserView(urlPassed):
    deleteUser(urlPassed)
    return redirect(url_for('users'))

#main admin


@app.route('/admin/', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
    form = editForm()
    databaseQuery = showAll()
    activitiesList = getActivities()
    if request.method == 'POST':
        search = form.search.data
        print(search)
        return redirect(url_for('adminSearch', urlPassed=search))

    return render_template('admin.html', databaseQuery=databaseQuery, activities=activitiesList, form=form)
@app.route('/view/', methods=['GET', 'POST'])
def view():
    form = editForm()
    databaseQuery = showAll()
    activitiesList = getActivities()
    if request.method == 'POST':
        search = form.search.data
        print(search)
        return redirect(url_for('searchView', urlPassed=search))

    return render_template('view.html', databaseQuery=databaseQuery, activities=activitiesList, form=form)
#main admin
@app.route('/view/<urlPassed>', methods=['GET', 'POST'])
@flask_login.login_required
def viewFiltered(urlPassed):

    databaseQuery = searchDBActivity(urlPassed)
    activitiesList = getActivities()
    return render_template('view.html', databaseQuery=databaseQuery, activities=activitiesList)

#main admin
@app.route('/admin/<urlPassed>', methods=['GET', 'POST'])
@flask_login.login_required
def adminFiltered(urlPassed):
    form = editForm()
    databaseQuery = searchDBActivity(urlPassed)
    activitiesList = getActivities()
    if request.method == 'POST':
        search = form.search.data
        print(search)
        return redirect(url_for('adminSearchFiltered', urlPassed=search, activity=urlPassed))
    return render_template('admin.html', databaseQuery=databaseQuery, activities=activitiesList, form=form)

#create a flask route with a dynamically generated url -
@app.route('/admin/search/<urlPassed>/')
def adminSearch(urlPassed):
    activitiesList = getActivities()
    #query our database with the URL argument provided to search by activity
    databaseQuery = search(urlPassed)
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('admin.html', databaseQuery=databaseQuery, urlPassed=urlPassed, activities=activitiesList)



#create a flask route with a dynamically generated url aka urlPassed
@app.route('/admin/search/<activity>/<urlPassed>/')
def adminSearchFiltered(urlPassed,activity):
    activitiesList = getActivities()
    #query our database with the URL argument provided to search by activity
    databaseQuery = searchFilteredActivity(activity,urlPassed)
    print(databaseQuery)
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('admin.html', databaseQuery=databaseQuery, urlPassed=urlPassed, activities=activitiesList)


#modify categories
@app.route('/admin/edit/modifycategory', methods=['GET', 'POST'])
@app.route('/admin/edit/modifycategory', methods=['GET', 'POST'])
@flask_login.login_required
def modifycategory():
    activitiesList = getActivities()
    return render_template('categorymain.html',  activities=activitiesList)

@app.route('/admin/edit/add', methods=['GET', 'POST'])
@flask_login.login_required
def addcategoryView():
    # load a form class in
    form = editForm()
    # if the form is submitted, see if it is blank and submit it to the function
    if request.method == 'POST':
        name = form.name.data
        if name == '':
            name = "None"
        # change the activity in the database based on what is provided by URL
        addActivity(name)
        return redirect(url_for('modifycategory'))
    activitiesList = getActivities()
    return render_template('addCategory.html',  activities=activitiesList, form=form)


@app.route('/admin/edit/new', methods=['GET', 'POST'])
@flask_login.login_required
def addrecordView():
    # load a form class in
    form = editForm()
    # if the form is submitted, see if it is blank and submit it to the function
    if request.method == 'POST':
        name = form.name.data
        if name == '':
            name = "None"
        activity = form.activity.data
        if activity == '':
            activity = "None"
        record = form.record.data
        if record == '':
            record = "None"
        year = form.year.data
        if year == '':
            year = "None"
        number = form.number.data
        if number == '':
            number = "None"
        moreInfo = form.moreInfo.data
        if moreInfo == '':
            moreInfo = "None"

        addRecord(name,activity,record,year,number,moreInfo)
        return redirect(url_for('admin'))
    activitiesList = getActivities()
    return render_template('new.html',  activities=activitiesList, form=form)



#modify individual category
@app.route('/admin/edit/modifycategory/<urlPassed>', methods=('GET', 'POST'))
@flask_login.login_required
def modifyIndividualCategory(urlPassed):
    #load a form class in
    form = editForm()
    # if the form is submitted, see if it is blank and submit it to the function
    if request.method == 'POST':
        name = form.name.data
        if name == '':
            name = "None"
        # change the activity in the database based on what is provided by URL
        changeActivity(urlPassed, name)
        return redirect(url_for('modifycategory'))
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('modifyCategory.html', urlPassed=urlPassed, form=form)\
#delete activity
@app.route('/admin/edit/modifycategory/delete/<urlPassed>')
@flask_login.login_required
def deleteCategory(urlPassed):
    deleteActivity(urlPassed)
    return redirect(url_for('modifycategory'))

#create a flask route with a dynamically generated url -
@app.route('/<urlPassed>')
def unknown_page(urlPassed):
    #query our database with the URL argument provided to search by activity
    databaseQuery = searchDBActivity(urlPassed)
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('results.html', databaseQuery=databaseQuery, urlPassed=urlPassed)
#create a flask route with a dynamically generated url -
@app.route('/search/<urlPassed>')
def searchView(urlPassed):
    #query our database with the URL argument provided to search by activity
    databaseQuery = search(urlPassed)
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('resultsView.html', databaseQuery=databaseQuery, urlPassed=urlPassed)
#delete record
@app.route('/admin/edit/delete/<urlPassed>', methods=('GET', 'POST'))
@flask_login.login_required
def delete_record(urlPassed):
  deleteRecord(urlPassed)
  return redirect(url_for('admin'))

#edit individual record
@app.route('/admin/edit/<urlPassed>', methods=('GET', 'POST'))
@flask_login.login_required
def edit_page(urlPassed):
    #get activities
    activitiesList = getActivities()
    #display the record based on ID
    databaseQuery = displaybyID(urlPassed)
    form = editForm()
    currentActivity = getactivityName(urlPassed)
    if request.method == 'POST':
        name = form.name.data
        if name == '':
            name = "None"
        activity = form.activity.data
        if activity == '':
            activity = "None"
        record = form.record.data
        if record == '':
            record = "None"
        year = form.year.data
        if year == '':
            year = "None"
        number = form.number.data
        if number == '':
            number = "None"
        moreInfo = form.moreInfo.data
        if moreInfo == '':
            moreInfo = "None"

        changeRecord(urlPassed,name,activity,record,year,number,moreInfo)
        return redirect(url_for('admin'))
    #render html page with results and pass on the databaseQuery dictionary and url passed so it shows the name at the top
    return render_template('editIndividual.html', databaseQuery=databaseQuery, urlPassed=urlPassed, activities=activitiesList, form=form, currentActivity=currentActivity)



if __name__ == '__main__':
    app.run(debug=True)
