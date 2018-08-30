from flask import Flask, request,render_template,redirect
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.json import jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from gzlrbackend import gasguzlrbackend 

app=Flask(__name__)

class loginForm(Form):
    userid = TextField('userID:')

class mpgForm(Form):
    tripmiles=TextField('tripmiles')
    fillupGallons=TextField('tankGallons')
    

@app.route('/test')
def sqlversion(version=gasguzlrbackend().getVersion()):
    return render_template('welcome.html',data=version)

@app.route('/')
def landing():
    return render_template('welcome.html')

@app.route('/newuser')
def newuser():
    userid=gasguzlrbackend().genuserid()
    gasguzlrbackend().adduser(userid)
    return render_template('newuser.html',newuserid=userid)

@app.route('/login', methods=['GET','POST'])
def userlogin():
    form = loginForm(request.form)

    if request.method == 'POST':
  
        if(gasguzlrbackend().verifyuser(request.form['login'])):
            return redirect('/mpg')
        else:
            return redirect('/login')
    return render_template('login.html',form=form)

@app.route('/mpg',methods=['GET','POST'])
def mpgapp():
    form=mpgForm(request.form)
    vehcid=gasguzlrbackend().genvehicleid()
    
    if request.method == 'POST':
        

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'])
        return redirect('/mpg')
    else:
        mpgcount=gasguzlrbackend().countMPGEntries(vehcid)
        if(mpgcount == 0):
            return render_template('mpg.html',mpgcount=mpgcount)
        else:
            mpgdata=gasguzlrbackend().getMPGData(vehcid)
            return render_template('mpg.html',data=mpgdata,mpgcount=mpgcount)
if __name__ == '__main__':
    app.run(port='5002')