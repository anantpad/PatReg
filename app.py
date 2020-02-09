#set up server
#import packages
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import redirect, session, flash

#initialize
#this function initializes any application
app = Flask(__name__)
app.debug = True

#config
app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/pat_reg?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-aou9c.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)
print(mongo.db)

#route
@app.route("/", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        loginname = request.form["username"]
        password = request.form["password"]
        record = mongo.db.patient_info.find_one({"loginname": loginname, "password": password})
        print(record["loginname"])
        if record["loginname"] == loginname and record["password"] == password:
            return render_template("patient_reg.html", firstname = record["firstname"], lastname = record["lastname"])
        # username = request.form["username"]
        # password = request.form["password"]
        # if username == 'sridhar' and password == 'asdf':
        #     return redirect("/patientinfo")
        else:
            flash("Invalid Username or password")


@app.route("/patientinfo", methods = ['GET', 'POST'])
def patientinfo():
    if request.method == 'GET':
        return render_template("patient_reg.html")
    elif request.method == "POST":
        title = request.form["title"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        mi = request.form["mi"]
        patientid = request.form["patientid"]
        birthdate = request.form["birthdate"]
        gender = request.form["gender"]
        race = request.form["race"]
        ethnicity = request.form["ethnicity"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        country = request.form["country"]
        zip = request.form["zip"]
        hphone = request.form["hphone"]
        wphone = request.form["wphone"]
        mphone = request.form["mphone"]
        loginname = request.form["loginname"]
        password = request.form["password"]
        active = "Y"
        mongo.db.patient_info.insert_one(
            {"title":title, "firstname":firstname, "lastname":lastname, "mi":mi, "patientid":patientid,
             "birthdate":birthdate, "gender":gender, "race":race, "ethnicity":ethnicity,
             "address":address, "city":city, "state":state, "country":country,"zip":zip,
             "hphone":hphone, "wphone":wphone, "mphone":mphone, "loginname":loginname, "password":password})
        return redirect("/patientinfo")

#run
if __name__ == "__main__":
    app.run()