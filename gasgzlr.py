from flask import Flask, request,render_template,redirect,flash,session,abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.json import jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField,SelectField
from gzlrbackend import gasguzlrbackend 
import os

app=Flask(__name__)
app.secret_key=os.urandom(12)

class loginForm(Form):
    userid = TextField('userID:')

class mpgForm(Form):
    tripmiles=TextField('tripmiles')
    fillupGallons=TextField('tankGallons')
    
class vehicleForm(Form):
    vehiclemake=SelectField('vehiclemake')
    vehiclemodel=SelectField('vehiclemodel')
    vehicleyear=TextField('vehicleyear')
    vehiclecolor=SelectField('vehiclecolor')

class User():
    def is_active(self):
        return True
    def get_id(self):
        pass #working on actual login


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
        username = request.form['login']
        if(gasguzlrbackend().verifyuser(request.form['login'])):
            session['logged_in']= True
            url="/mpg/"+username
            return redirect(url) 
        else:
            return redirect('/login')
    return render_template('login.html',form=form)

@app.route('/mpg/<username>',methods=['GET','POST'])
def mpgapp(username):
    #form=mpgForm(request.form)
    
    
    if request.method == 'POST':
        
        vehcid=gasguzlrbackend().genvehicleid()
        mpgcalc=float(request.form['tripmiles'])/float(request.form['tankGallons'])
        print(request.form['tripmiles'])
        print(request.form['tankGallons'])
        print(mpgcalc)

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'],mpgcalc)
        gasguzlrbackend().newaddvehicle(username,vehcid)
      
        url="/mpg/"+username
        return redirect(url)
    else:
        try:
            if session['logged_in']:
                mpgcount=gasguzlrbackend().countMPGEntries(username)
                print(mpgcount)
                if(mpgcount == 0):
                    
                    return render_template('mpg.html',mpgcount=mpgcount)
                else:
                    
                    vehcid=gasguzlrbackend().getvehicle(username)
                    print(vehcid.vehicleid)
                    mpgdata=gasguzlrbackend().getmpgData(vehcid.vehicleid)
                    print(mpgdata)
                    return render_template('mpg.html',data=mpgdata,mpgcount=mpgcount,user=username,vehicleid=vehcid)
            else:
                return redirect('/login')
        except:
            return redirect('/')

@app.route('/mpg/<username>/<vehcid>/new', methods=['GET','POST'])
def newmpgentry(username,vehcid):
    if request.method == 'POST':
        #vehcid=gasguzlrbackend().genvehicleid()
        mpgcalc=float(request.form['tripmiles'])/float(request.form['tankGallons'])
        print(request.form['tripmiles'])
        print(request.form['tankGallons'])
        print(mpgcalc)

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'],mpgcalc)
        gasguzlrbackend().newaddvehicle(username,vehcid)
      
        url="/mpg/"+username
        return redirect(url)
    else:

        
            
        vehcid=gasguzlrbackend().getvehicle(username)
        print(vehcid.vehicleid)
        mpgdata=gasguzlrbackend().getmpgData(vehcid.vehicleid)
        print(mpgdata)
        return render_template('newmpg.html',data=mpgdata,user=username,vehicleid=vehcid)

@app.route('/logout')
def logout():
    session['logged_in']=False
    return redirect('/')

if __name__ == '__main__':
    
    app.run(port='5002')