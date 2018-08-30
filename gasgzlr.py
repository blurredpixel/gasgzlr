from flask import Flask, request,render_template,redirect
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.json import jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField,SelectField
from gzlrbackend import gasguzlrbackend 

app=Flask(__name__)

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
            url="/mpg/"+username
            return redirect(url) 
        else:
            return redirect('/login')
    return render_template('login.html',form=form)

@app.route('/mpg/<username>',methods=['GET','POST'])
def mpgapp(username):
    #form=mpgForm(request.form)
    vehcid=gasguzlrbackend().genvehicleid()
    
    if request.method == 'POST':
        mpgcalc=float(request.form['tripmiles'])/float(request.form['tankGallons'])
        print(request.form['tripmiles'])
        print(request.form['tankGallons'])
        print(mpgcalc)

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'],mpgcalc)
       
      
        url="/mpg/"+username
        return redirect(url)
    else:
        mpgcount=gasguzlrbackend().countMPGEntries(username)
        print(mpgcount)
        if(mpgcount == 0):
            return render_template('mpg.html',mpgcount=mpgcount)
        else:
            mpgdata=gasguzlrbackend().getMPGData(vehcid)
            return render_template('mpg.html',data=mpgdata,mpgcount=mpgcount,user=username)

@app.route('/vehicle/<username>',methods=['GET','POST'])
def vehicleapp(username):
    #form=mpgForm(request.form)
    vehcid=gasguzlrbackend().genvehicleid()
    
    if request.method == 'POST':
        mpgcalc=float(request.form['tripmiles'])/float(request.form['tankGallons'])
        print(request.form['vehiclemake'])
        print(request.form['vehiclemodel'])
        print(mpgcalc)

        gasguzlrbackend().addvehicle(username,request.form['vehiclemake'],request.form['vehiclemodel'],request.form['vehicleyear'])
       
      
        url="/vehicle/"+username
        return redirect(url)
    else:
        vehiclecount=gasguzlrbackend().vehiclecount(username) #TODO
        print(mpgcount)
        if(vehiclecount == 0):
            return render_template('newvehicle.html',vehiclecount=vehiclecount)
        else:
            mpgdata=gasguzlrbackend().getMPGData(vehcid)
            return render_template('newvehicle.html',data=mpgdata,vehiclecount=vehiclecount,user=username)



if __name__ == '__main__':
    app.run(port='5002')