class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "YOUR USERNAME",
            "passwd": "YOUR PASSWORD",
            "db": "snapguard"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getPictures(self,gebruiker):
        # Query zonder parameters
        sqlQuery = "SELECT g.GebruikerID, c.CameraID, f.Naam, f.Datumtijd, f.FotoID From tblgebruiker as g inner join tblgebruikercamera as gb on g.GebruikerID = gb.GebruikerID inner join tblcamera as c on gb.CameraID = c.CameraID inner join tblfoto as f on c.CameraID = f.CameraID WHERE g.GebruikerID = '"+str(gebruiker)+"' ORDER BY Datumtijd DESC;"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getPictureDetails(self, picid):
        # Query met parameters
        sqlQuery = "SELECT * FROM tblfoto WHERE FotoID ='"+picid+"'"
        # Combineren van de query en parameter


        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getCameraDetails(self, cameraid):
        sqlQuery = "SELECT * FROM tblcamera WHERE CameraID ='"+cameraid+"'"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def setNewUser(self, fname, lname, email, password):
        # Query met parameters
        sqlQuery = "INSERT INTO tblgebruiker (Naam, Voornaam, Email, Password) VALUES ('%s','%s','%s','%s')" % (lname,fname,email,password)
        # Combineren van de query en parameter
        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def checkCredentials(self, email, password):
        sqlQuery = "SELECT * FROM tblgebruiker WHERE Email='" + email + "' AND Password='" + password + "';"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getCameras(self, gebruiker):
        sqlQuery = "SELECT tblcamera.CameraID, tblcamera.Plaats, tblcamera.Resolutie FROM tblgebruikercamera INNER JOIN tblcamera on tblcamera.CameraID = tblgebruikercamera.CameraID INNER JOIN tblgebruiker on tblgebruiker.GebruikerID = tblgebruikercamera.GebruikerID WHERE tblgebruikercamera.GebruikerID = '"+str(gebruiker)+"';"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def deletePicture(self, pic_to_delete):
        sqlQuery = "DELETE FROM tblfoto WHERE FotoID=%d" % pic_to_delete
        self.__cursor.execute(sqlQuery)
        self.__cursor.close()
        self.__connection.commit()

    def editPlace(self, place_to_edit, new_place):
        sqlQuery = "UPDATE tblcamera SET Plaats = '%s' WHERE CameraID = %d" % (new_place,place_to_edit)
        self.__cursor.execute(sqlQuery)
        self.__cursor.close()
        self.__connection.commit()

    def addCamera(self, camid, userid):
        sqlQuery= "INSERT INTO tblgebruikercamera(GebruikerID, CameraID) VALUES (%s, %s)" % (userid,camid)
        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def takePicture(self,name,datetime,camid):
        sqlQuery = "INSERT INTO tblfoto(Naam, Datumtijd, CameraID) VALUES ('%s', '%s', '%s')" % (name, datetime, camid)
        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()
