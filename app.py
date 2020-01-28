#set up server
#import packages
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import redirect

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
        username = request.form["username"]
        password = request.form["password"]
        if username == 'sridhar' and password == 'asdf':
            return redirect("/patientinfo")


@app.route("/patientinfo", methods = ['GET', 'POST'])
def patientinfo():
    if request.method == 'GET':
        # name = "Sridhar"
        return render_template("patient_reg.html") #, firstname = name)
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        mi = request.form["mi"]
        patientid = request.form["patientid"]
        birthdate = request.form["birthdate"]
        gender = request.form["gender"]
        race = request.form["race"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        country = request.form["country"]
        zip = request.form["zip"]
        loginname = request.form["loginname"]
        password = request.form["password"]
        mongo.db.patient_info.insert_one(
            {"firstname":firstname, "lastname":lastname, "mi":mi, "patientid":patientid, "birthdate":birthdate, "gender":gender, "race":race, "address":address, "city":city, "state":state, "country":country,"zip":zip, "loginname":loginname, "password":password})
        return redirect("/patientinfo")

#run
if __name__ == "__main__":
    app.run()