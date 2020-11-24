
###############################################
#File not complete yet. Talked to TA, he said submitting incomplete file is okay.
#I am submitting the three test files as well so I have enough material that can be reviewed.
###########################################
from smokeDRpi import *
from fridgeRpi import *
from switchRPi import  *
import sqlite3
from sqlite3 import Error


#connect to database
dbconnect = sqlite3.connect("myDatabaseServer.db");
#access coloumns by name
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

###Creates database server table where all values displayed on the app will be stored.###
def create_table():
    cursor.execute('''create table if not exists server(userID Integer, sensorID Integer, Temperature ℃ Real, Humanity rH Real, currentState text, CO2 Real, Methane Real) ''');
    dbconnect.commit();


def add_IDValues(val):
    # insert into table
    cursor.execute('''insert into server values (?,?)''',(userID, sensorID));
    dbconnect.commit();

###Updates value in the database server###
def update_value(val):

    #Takes in the userID and ServerID
    #This will be used to look up their corresponding values from the database
    IDs =[]
    IDs[0] = val[0]
    IDs[1] = val [1]

    #insert into table
    cursor.execute('''insert into server values (?,?,?,?,?,?,?)''',(userID, sensorID, temperature, humidity, currentState, CO2, methane));
    dbconnect.commit();
    cursor.execute('SELECT * FROM server');


    #close connection
    dbconnect.close();





if __name__ == '__main__':
    #create table
    create_table()
    #add user IDs and sensorIDs in database, can be called for as many products
    add_IDValues(1, 2)
    add_IDValues(5, 7)
    add_IDValues(9, 12)
    #esatablish connection with all three pis
    establishConnection()
    #read from ThingSpeak every 10 secs
    #update values in database
    update_value(read_data_thingspeakRpiOne().split(","))
    update_value(read_data_thingspeakRpiTwo().split(","))
    update_value(read_data_thingspeakRpiThree().split(","))




