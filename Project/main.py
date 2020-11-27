from main_SmokePi import *
from main_FridgePi import *
from main_SwitchPi import  *
import time
import sqlite3


###Updates value in the database server###
def update_Value(val):

    try:
        # connect to database
        dbconnect = sqlite3.connect("myDatabaseServer.db")
        # access coloumns by name
        dbconnect.row_factory = sqlite3.Row
        cursor = dbconnect.cursor()
        print("Connected to SQLite")

        #We check the sensor IDs to see if they were 1, 2 or 3 and depending on the sensor we go into the if condition
        #sensorID 1 represents the temperature and humidity sensor
        if(val[1] == 1):
            sqlite_update_query = """Update server set Temperature = ?, Humidity = ? where userID = ? and sensorID = ?"""
            columnValues = (val[2], val[3], val[0], val[1])
            cursor.execute(sqlite_update_query, columnValues)
            dbconnect.commit()
            print("Temperature and Humidity values updated successfully")
            #dbconnect.commit()
            cursor.close()
        #sensorID 2 represents the wifi enabled switch sensor
        elif(val[1] == 2):
            sqlite_update_query = """Update server set currentState = ? where userID = ? and sensorID = ?"""
            columnValues = (val[2], val[0], val[1])
            cursor.execute(sqlite_update_query, columnValues)
            dbconnect.commit()
            print("Current State of the switch updated successfully")
            #dbconnect.commit()
            cursor.close()
        #sensorID 3 represents the CO2 and methane sensor
        elif(val[1] == 3):
            sqlite_update_query = """Update server set CO2 = ?, Methane = ? where userID = ? and sensorID = ?"""
            columnValues = (val[2], val[3], val[0], val[1])
            cursor.execute(sqlite_update_query, columnValues)
            dbconnect.commit()
            print("CO2 and Methane values updated successfully")
            #dbconnect.commit()
            cursor.close()


    except sqlite3.Error as error:
        print("Failed to update multiple columns of sqlite table", error)
    finally:
        if (dbconnect):
            dbconnect.close()
            print("sqlite connection is closed")



###Creates database server table where all values displayed on the app will be stored.###
def create_Table():

    try:
        # connect to database
        dbconnect = sqlite3.connect("myDatabaseServer.db")
        # access coloumns by name
        dbconnect.row_factory = sqlite3.Row
        cursor = dbconnect.cursor()
        print("Connected to SQLite")
        sqlite_create_table_query = '''create table if not exists server(
                                    userID Integer,
                                    sensorID Integer,
                                    Temperature Real,
                                    Humidity Real,
                                    currentState text,
                                    CO2 Real,
                                    Methane Real);'''
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        dbconnect.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if (dbconnect):
            dbconnect.close()
            print("sqlite connection is closed")





def add_IDValues(uID, sID):
    valInServer = False
    try:
        # connect to database
        dbconnect = sqlite3.connect("myDatabaseServer.db")
        # access coloumns by name
        dbconnect.row_factory = sqlite3.Row
        cursor = dbconnect.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from server"""
        cursor.execute(sqlite_select_query)
        #fetch all the rows and then compare
        records = cursor.fetchall()

        for row in records:
            if(uID == row[0]):
                if(sID == row[1] and valInServer == False):
                    valInServer = True

        if(valInServer == False):
            # insert into table
            sqlite_insert_with_param = """INSERT INTO server
                              (userID, sensorID) 
                              VALUES (?, ?);"""

            data_tuple = (uID, sID)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            dbconnect.commit();

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if (dbconnect):
            dbconnect.close()
            print("The Sqlite connection is closed")

def print_Table():
    try:
        # connect to database
        dbconnect = sqlite3.connect("myDatabaseServer.db")
        # access coloumns by name
        dbconnect.row_factory = sqlite3.Row
        cursor = dbconnect.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from server"""
        cursor.execute(sqlite_select_query)
        #fetch all the rows and then compare
        records = cursor.fetchall()

        for row in records:
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
            print(row[5])
            print(row[6])
            print("\n")


        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if (dbconnect):
            dbconnect.close()
            print("The Sqlite connection is closed")



if __name__ == '__main__':
    #create table if not exists
    create_Table()
    #add user IDs and sensorIDs in database, can be called for as many products
    #we add the first userID 10 and since it is using the Temperature and humidity sensor the sensorID assigned to it is 1
    add_IDValues(10, 1)
    # we add the second userID 20 and since it is using the wifi enabled switch sensor the sensorID assigned to it is 2
    add_IDValues(20, 2)
    # we add the third userID 30 and since it is using the CO2 and methane sensor the sensorID assigned to it is 3
    add_IDValues(30, 3)

    #establish connection with Users
    establishConnectionFridgePi()
    establishConnectionSwitchPi()
    establishConnectionSmokePi()

    while True:
        time.sleep(10)
        update_Value(read_data_thingspeakRpiOne().split(","))
        update_Value(read_data_thingspeakRpiTwo().split(","))
        update_Value(read_data_thingspeakRpiThree().split(","))


    print_Table()







