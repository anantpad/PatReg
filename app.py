#set up server
#import packages
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import redirect, session, flash

#initialize
#this function initializes any application
app = Flask(__name__)
app.debug = True

app.secret_key = "sri"

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
        error = None
        loginname = request.form["username"]
        password = request.form["password"]
        session["loggedin"] = loginname
        # record = mongo.db.patient_info.find_one({"loginname": loginname, "password": password})
        # print(record["loginname"])
        # if record["loginname"] == loginname and record["password"] == password:
        #     return render_template("patient_reg.html", firstname = record["firstname"], lastname = record["lastname"])
        if loginname == 'sridhar' and password == 'asdf1234':
            flash("Logged in Successfully")
            return redirect("/patlist")
        else:
            error = "Invalid credentials"
            flash(error)
            return render_template("login.html", error = error)

@app.route("/patient", methods = ['GET', 'POST'])
def patlogin():
    if request.method =='GET':
        return render_template("patientLogin.html")
    else:
        loginname = request.form["username"]
        password = request.form["password"]
        record = mongo.db.patient_info.find_one({"loginname": loginname, "password": password})
        print(record["loginname"])
        patientid = record['patientid']
        redirect("/edit")

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
        email = request.form["email"]
        website = request.form["website"]
        mongo.db.patient_info.insert_one(
            {"title":title, "firstname":firstname, "lastname":lastname, "mi":mi, "patientid":patientid,
             "birthdate":birthdate, "gender":gender, "race":race, "ethnicity":ethnicity,
             "address":address, "city":city, "state":state, "country":country,"zip":zip,
             "hphone":hphone, "wphone":wphone, "mphone":mphone, "email":email, "website": website, "active":"Y"})
        flash("Patient Created Successfully")
        return redirect("/patlist")

@app.route("/patlist", methods = ['GET', 'POST'])
def patlist():
    if request.method == 'GET':
        patientList = mongo.db.patient_info.find({})
        print(patientList)
        return render_template("pat_list.html", patientList = patientList)

@app.route("/delete", methods = ['GET', 'POST'])
def delete():
    if request.method == 'GET':
        patientid = request.args['patientid']
        mongo.db.patient_info.delete_one({'patientid':patientid})
        flash("Selected Patient Record deleted")
        return redirect("/patlist")

@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method == 'GET':
        patientid = request.args['patientid']
        record = mongo.db.patient_info.find_one({"patientid":patientid})
        title = record["title"]
        firstname = record["firstname"]
        lastname = record["lastname"]
        mi = record["mi"]
        patientid = record["patientid"]
        birthdate = record["birthdate"]
        gender = record["gender"]
        race = record["race"]
        ethnicity = record["ethnicity"]
        address = record["address"]
        city = record["city"]
        state = record["state"]
        country = record["country"]
        zip = record["zip"]
        hphone = record["hphone"]
        wphone = record["wphone"]
        mphone = record["mphone"]
        email = record["email"]
        website = record["website"]
        print(address)
        return render_template("editpatientreg.html", title = title, firstname = firstname, lastname = lastname, mi = mi, patientid = patientid,
                               birthdate = birthdate, gender = gender, race = race, ethnicity = ethnicity, address = address, city = city, state = state, country = country, zip = zip,
                               hphone = hphone, wphone = wphone, mphone = mphone, email = email, website = website)
    elif request.method == 'POST':
        patientid = request.form["patientid"]
        title = request.form["title"]
        mi = request.form["mi"]
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
        email = request.form["email"]
        website = request.form["website"]
        mongo.db.patient_info.update_one(
            {"patientid": patientid},{"$set":{"title": title, "mi": mi, "gender": gender, "race": race,"ethnicity": ethnicity,
                                             "address": address,"city": city, "state": state, "country": country, "zip": zip,
                                             "hphone": hphone, "wphone": wphone, "mphone": mphone, "email": email, "website": website}})
        flash("Patient Record edited Successfully")
        return redirect("/patlist")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    flash(session["loggedin"] + " " + "Logged Out Successfully")
    session.pop("loggedin", None)
    print(session)
    return redirect("/")

#run
if __name__ == "__main__":
    app.run()