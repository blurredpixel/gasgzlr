from flask import Flask, request,render_template,redirect,flash,session,abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.json import jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField,SelectField
from gzlrbackend import gasguzlrbackend 
import os
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource





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



def dataviz(data):
    x=[]
    y=[]
    for row in data:
        x.append(str(row.fillGallons))
        y.append(str(row.calcMPG))


    p=figure(x_range=x,plot_width=445,plot_height=225,x_axis_label='Tank gallons',y_axis_label='MPG')
    p.vbar(x=x,top=y,width=0.9)
    return p
  

# this returns and renders the main page
@app.route('/')
def landing():
    return render_template('welcome.html')
#this displays the new user page and submits
#the new user to the backend
@app.route('/newuser')
def newuser():
    userid=gasguzlrbackend().genuserid()
    gasguzlrbackend().adduser(userid)
    return render_template('newuser.html',newuserid=userid)
#login page which accepts a get to load it and a post for processing

@app.route('/login', methods=['GET','POST'])
def userlogin():
    form = loginForm(request.form)

    if request.method == 'POST':
        username = request.form['login']
        if(gasguzlrbackend().verifyuser(request.form['login'])):
            session['logged_in']= True #this is important for displaying elements on main app page
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
        

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'],mpgcalc)
        gasguzlrbackend().newaddvehicle(username,vehcid)
      
        url="/mpg/"+username
        return redirect(url)
    else:
        try:
            if session['logged_in']:
                mpgcount=gasguzlrbackend().countMPGEntries(username)
                
                if(mpgcount == 0):
                    
                    return render_template('mpg.html',mpgcount=mpgcount)
                else:
                    
                    vehcid=gasguzlrbackend().getvehicle(username) #vehicle assoc with username
                    
                    mpgdata=gasguzlrbackend().getmpgData(vehcid.vehicleid) #gets row object
                    vizscript,vizdiv=components(dataviz(mpgdata))
                    
                    
                    return render_template('mpg.html',data=mpgdata,mpgcount=mpgcount,user=username,vehicleid=vehcid,vizscript=vizscript,vizdiv=vizdiv)
            else:
                return redirect('/login')
        except Exception as err: #if not logged in throws an exception
            print(err)
            return redirect('/')

@app.route('/mpg/<username>/<vehcid>/new', methods=['GET','POST'])
def newmpgentry(username,vehcid):
    if request.method == 'POST':
        #vehcid=gasguzlrbackend().genvehicleid()
        mpgcalc=float(request.form['tripmiles'])/float(request.form['tankGallons'])
        

        gasguzlrbackend().addmpgData(vehcid,request.form['tripmiles'],request.form['tankGallons'],mpgcalc)
        gasguzlrbackend().newaddvehicle(username,vehcid)
      
        url="/mpg/"+username
        return redirect(url)
    else:

        
            
        vehcid=gasguzlrbackend().getvehicle(username)
        
        mpgdata=gasguzlrbackend().getmpgData(vehcid.vehicleid)
        
        
        return render_template('newmpg.html',data=mpgdata,user=username,vehicleid=vehcid)

@app.route('/logout')
def logout():
    session['logged_in']=False
    return redirect('/')

if __name__ == '__main__':
    
    app.run(port='5002',host="0.0.0.0")