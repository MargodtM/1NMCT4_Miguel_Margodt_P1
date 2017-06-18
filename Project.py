from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from DbClass import DbClass


app = Flask(__name__)



@app.route('/')
def overview():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        list_pics = Db_layer.getPictures(userLoggedIn)
        return render_template('overview.html', pics=list_pics)

@app.route('/login', methods=['POST'])
def login():
    Db_layer = DbClass()
    result = Db_layer.checkCredentials(request.form['username'],request.form['password'])
    if not result:
        flash('wrong password')
    else:
        global userLoggedIn
        userLoggedIn = result[0]
        session['logged_in'] = True
    return overview()

@app.route('/picdetails/<picid>')
def picdetails(picid):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        result = Db_layer.getPictureDetails(picid)
        return render_template('picdetails.html',pic=result)

@app.route('/deletePic', methods=['POST'])
def deletePic():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        pic_to_delete = int(request.form['pic_to_delete'])
        Db_layer.deletePicture(pic_to_delete)
        return redirect('/')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return overview()

@app.route("/cameras")
def cameras():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        list_cams = Db_layer.getCameras(userLoggedIn)
        return render_template('cameras.html', cameras=list_cams)

@app.route("/camdetails/<cameraid>")
def camdetails(cameraid):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        result = Db_layer.getCameraDetails(cameraid)
        return render_template('camdetails.html', cam=result)

@app.route("/editplace", methods=['POST'])
def editplace():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Db_layer = DbClass()
        cameraid = int(request.form['camid'])
        newplace = request.form['newplace']
        Db_layer.editPlace(cameraid,newplace)
        return redirect('cameras')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/register", methods=['POST'])
def register():
    Db_layer = DbClass()
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    Db_layer.setNewUser(fname, lname, str(email), password)
    return overview()

@app.route("/addcamera", methods=['POST'])
def addcamera():
    Db_layer = DbClass()
    camid = str(request.form['camid'])
    Db_layer.addCamera(camid,str(userLoggedIn))
    return cameras()

if __name__ == '__main__':

    # port = int(os.environ.get("PORT", 8080))
    # host = "0.0.0.0"

    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
