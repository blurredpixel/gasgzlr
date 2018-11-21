import pyodbc
import random
import string
import datetime


class gasguzlrbackend():

    def connecttodb(self):
        conn = pyodbc.connect('DSN=gzlr;UID=gzlr;PWD=AUhf2LX%!8??mbDc')
        return conn

    
    def genuserid(self):
        userid = ''.join(random.choices(
            string.ascii_letters + string.digits, k=8))
        return userid

    def adduser(self,userid):
       
        createdate = datetime.datetime.now().strftime('%Y%m%d')

        query = '''
        

        INSERT INTO users(userID,dateCreated) VALUES(?,?)
        
        '''
        cursor = self.connecttodb().cursor()
        try:
        
            cursor.execute(query, (userid, createdate))
            cursor.commit()
        except:
           print("error in user add")
        
        

    def addmpgData(self, vehicleid, tankmiles, fillgallons,calcmpg):

        query = '''
      

        INSERT INTO mpgdata(vehicleID,tankMiles,fillGallons,calcMPG) VALUES(?,?,?,?)'''
        cursor = self.connecttodb().cursor()
        
        try:
            cursor.execute(query, (vehicleid, tankmiles, fillgallons, calcmpg))
            cursor.commit()
        except:
            print("error in mpg data add")
        
    def getmpgData(self, vehid):
    
        query = '''
        
        SELECT * FROM mpgdata WHERE vehicleID = ?
        '''
       
        cursor = self.connecttodb().cursor()
        
        try:
            
            cursor.execute(query, (vehid))
            rows=cursor.fetchall()
                
                
        
            return rows
        except:
            print("error in mpg data retrieval ")

    def updateMPGData(self, vehicleid, tankmiles, fillgallons, calcmpg):
        query = '''
        UPDATE mpgdata
        SET tankMiles=?,fillGallons=?,calcMPG=?
        WHERE vehicleID = ? 
        
        '''

        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query, (tankmiles, fillgallons, calcmpg, vehicleid))
        except:
            print("error in vehicle data update")

    def deleteMPGData(self, vehicleid):
        query = '''
        DELETE FROM mpgdata
        WHERE vehicleID = ?
        
        '''

        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query, (vehicleid))
        except:
            print("error in MPG data delte")
    

    def deleteuserdata(self, userid):
        query = '''
        DELETE FROM users
        WHERE userID = ?
        
        '''

        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query, (userid))
        except:
            print("error in user data delte")

    def genvehicleid(self):
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return id

    def addvehicle(self, userid, make, model, year, otherOptions="none", color="none"):
        query = '''
        

        INSERT INTO vehicles(vehicleID,userID,vehicleMake,vehicleModel,vehicleYear,color,otherOptions) VALUES(?,?,?,?,?,?,?)'''

        cursor = self.connecttodb().cursor()
        vehicleid=''.join(random.choices(string.ascii_letters + string.digits, k=8))
        try:
            cursor.execute(query, (vehicleid, userid, make,
                                   model, year, color, otherOptions))
        except:
            print("error in vehicle data add")

    def newaddvehicle(self,userid,vehicleid):
        query=        '''
            INSERT INTO newvehicles(vehicleid,userid) VALUES(?,?)
        '''  
        cursor = self.connecttodb().cursor()
        
        try:
            cursor.execute(query, (vehicleid, userid))
            cursor.commit()
        except:
            print("error in vehicle data add")

    def deletevehicle(self, vehicleid):
        query = '''
        DELETE FROM vehicles
        WHERE vehicleID = ?
        
        '''

        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query, (vehicleid))
        except:
            print("error in vehicle data delete")

    def updatevehicle(self, userid, make, model, year, vehicleid, otherOptions="none", color="none"):
        query = '''
        UPDATE vehicles
        SET vehicleMake=?,vehicleModel=?,vehicleYear=?,color=?,otherOptions=?
        WHERE vehicleID = ? AND userID = ?
        
        '''

        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query, (make, model, year, color,
                                   otherOptions, vehicleid, userid))
        except:
            print("error in vehicle data update")

    def verifyuser(self,userid):
        query='''
        SELECT * FROM [gasgzlr].[dbo].[users]
        WHERE userID = ? 
        '''
        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query,(userid))
            rows=cursor.fetchone()
        except:
            print("error in user verification _ backend")
        return str(rows.userID)==userid
        
    def authuser(self,userid):
        query='''
        UPDATE users
        SET auth=?
        WHERE userID=?
        '''
        cursor = self.connecttodb().cursor()
        try:
            cursor.execute(query,'1',userid)
            cursor.commit()
        except:
            print("error in user authentication__ backend")




    def countMPGEntries(self,userid):
        query='''
        SELECT gasgzlr.dbo.users.userID, gasgzlr.dbo.newvehicles.vehicleid,gasgzlr.dbo.mpgdata.tankMiles
        ,gasgzlr.dbo.mpgdata.fillGallons,gasgzlr.dbo.mpgdata.calcMPG


        FROM [gasgzlr].[dbo].[users] join gasgzlr.dbo.newvehicles on gasgzlr.dbo.users.userID=gasgzlr.dbo.newvehicles.userid 
        join gasgzlr.dbo.mpgdata on gasgzlr.dbo.newvehicles.vehicleid =gasgzlr.dbo.mpgdata.vehicleID

        WHERE
        gasgzlr.dbo.users.userID=? 
        '''
        cursor = self.connecttodb().cursor()
        c=cursor.execute(query,(userid))
        try:
            rows=c.fetchall()
        except:
            print("error in mpg entries retrieval__backend")
        data=[]
        for row in rows:
            data.append(row)

        return len(data)
    
    def getvehicle(self,userid):
        query='''
        select vehicleid from dbo.newvehicles where userid=?
        '''
        cursor = self.connecttodb().cursor()
        try:
            c=cursor.execute(query,(userid))
            rows=c.fetchone()
        except:
            print("error in vehicle lookup__backend")
       

        return rows