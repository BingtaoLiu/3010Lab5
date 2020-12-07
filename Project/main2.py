from main_ReadWrite import *
import sqlite3
import socket
import time

###SERVER DETAILS###
PORT = 8080
SERVER = "192.168.0.34"
ADDR = (SERVER, PORT)
HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Close"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn, addr):
   # connected = True
   # while connected:
   print("Msg receiving....")
   msg = conn.recv(HEADER).decode(FORMAT)
   print(msg)
   print("[Msg RECEIVED ]")
   #if msg == DISCONNECT_MESSAGE:
       #connected = False
   conn.close()
   return msg


def send_to_client(conn, addr, sendmsg):
    message = sendmsg.encode(FORMAT)
    conn.send(message)
    conn.close()



####Comparing ID values in database####
def comp_values(uID, sID):
    valInServer = False
    a = int(uID)
    b = int(sID)
    # connect to database
    dbconnect = sqlite3.connect("myDatabaseServer.db")
    # access coloumns by name
    dbconnect.row_factory = sqlite3.Row
    cursor = dbconnect.cursor()
    print("Connected to SQLite")

    sqlite_select_query = """SELECT * from server"""
    cursor.execute(sqlite_select_query)
    # fetch all the rows and then compare
    records = cursor.fetchall()

    for row in records:
        if (a == row[0]):
            if (b  == row[1] and valInServer == False):
                print("value in server")
                valInServer = True
                return True

    cursor.close()
    dbconnect.close()
    print("The Sqlite connection is closed")

last_entry_id1 = 0

last_entry_id3 = 0

###Updates value in the database server###
def update_Value(val, conn, addr):
   global last_entry_id1
   global last_entry_id3
   #contains the values needed to update
   temp = val[0].split(",")
   print(val)
   if (len(temp) == 4):
        print(temp[1])
        a = int(temp[1])
        b = int(temp[0])
        print(a)
        print(b)
        try:
            # connect to database
            dbconnect = sqlite3.connect("myDatabaseServer.db")
            # access coloumns by name
            dbconnect.row_factory = sqlite3.Row
            cursor = dbconnect.cursor()
            print("Connected to SQLite")

            # We check the sensor IDs to see if they were 1, 2 or 3 and depending on the sensor we go into the if condition
            # sensorID 1 represents the temperature and humidity sensor

            if (a == 1 ):

                print(last_entry_id1)
                if(last_entry_id1 != val[1]):
                    print(last_entry_id1)
                    last_entry_id1 = val[1]
                    sqlite_update_query = """Update server set Temperature = ?, Humidity = ? where userID = ? and sensorID = ?"""
                    columnValues = (temp[2], temp[3], temp[0], temp[1])
                    cursor.execute(sqlite_update_query, columnValues)
                    dbconnect.commit()
                    tempa = [str(a),temp[2] ,temp[3]]
                    msg_to_app = ",".join(tempa)
                    send_to_client(conn, addr, msg_to_app)
                    cursor.close()

            # sensorID 3 represents the CO2 and methane sensor
            elif (a == 3):
                if(last_entry_id3 != val[1]):
                    last_entry_id3 = val[1]
                    sqlite_update_query = """Update server set CO2 = ?, Methane = ? where userID = ? and sensorID = ?"""
                    columnValues = (temp[2], temp[3], temp[0], temp[1])
                    cursor.execute(sqlite_update_query, columnValues)
                    dbconnect.commit()
                    tempb = [temp[1],temp[2] ,temp[3]]
                    msg_to_app = ",".join(tempb)
                    send_to_client(conn, addr, msg_to_app)
                    print("CO2 and Methane values updated successfully")
                    cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
            return 0
        finally:
            if (dbconnect):
                dbconnect.close()
                print("sqlite connection is closed")


###Updates value in the database server###
def update_Switch(val, conn, addr):
   #contains the values needed to update
   temp = val.split(",")
   print(temp)
   uid = int(temp[0])
   sid = int(temp[1])
   try:
            # connect to database
            dbconnect = sqlite3.connect("myDatabaseServer.db")
            # access coloumns by name
            dbconnect.row_factory = sqlite3.Row
            cursor = dbconnect.cursor()
            print("Connected to SQLite")
            # We check the sensor IDs to see if they were 1, 2 or 3 and depending on the sensor we go into the if condition
            # sensorID 1 represents the temperature and humidity sensor

            # sensorID 2 represents the wifi enabled switch sensor
            if (sid == 2):
                    sqlite_update_query = """Update server set currentState = ? where userID = ? and sensorID = ?"""
                    columnValues = (temp[2], uid, sid)
                    cursor.execute(sqlite_update_query, columnValues)
                    dbconnect.commit()
                    print("Current State of the switch updated successfully")
                    write_data_thingspeakRpiTwo(temp[0], temp[1], temp[2])
                    cursor.close()



   except sqlite3.Error as error:
       print("Failed to update multiple columns of sqlite table", error)
       return 0
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
        if dbconnect:
            dbconnect.close()
            print("sqlite connection is closed")


def add_IDValues(uID, sID):
    print("In add value function")
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
        # fetch all the rows and then compare
        records = cursor.fetchall()

        for row in records:
            if uID == row[0]:
                if sID == row[1] and valInServer is False:
                    valInServer = True

        if valInServer is False:
            # insert into table
            sqlite_insert_with_param = """INSERT INTO server
                              (userID, sensorID) 
                              VALUES (?, ?);"""

            data_tuple = (uID, sID)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            dbconnect.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if dbconnect:
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
        # fetch all the rows and then compare
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
        if dbconnect:
            dbconnect.close()
            print("The Sqlite connection is closed")


if __name__ == '__main__':
    # create table if not exists
    create_Table()
    # add user IDs and sensorIDs in database, can be called for as many products we add the first userID 10 and since
    # it is using the Temperature and humidity sensor the sensorID assigned to it is 1
    add_IDValues(10, 1)
    # we add the second userID 20 and since it is using the wifi enabled switch sensor the sensorID assigned to it is 2
    add_IDValues(20, 2)
    print("value added")
    # we add the third userID 30 and since it is using the CO2 and methane sensor the sensorID assigned to it is 3
    add_IDValues(30, 3)
    print_Table()

    # establish connection with Users
    establishConnectionFridgePi()
    establishConnectionSwitchPi()
    establishConnectionSmokePi()

    print("[STARTING] server is starting..")
    connected1 = True
    server.listen()
    while connected1:
        conn, addr = server.accept()
        server.setblocking(1)
        print("Client Connected")
        data1 = read_data_thingspeakRpiOne()
        data3 = read_data_thingspeakRpiThree()
        update_Value(data1, conn, addr)
        print("FPI values updated")
        #conn.close()
        #time.sleep(5)
        conn, addr = server.accept()
        print("Client Connected Again")
        update_Value(data3, conn, addr)
        print("SmPI values updated")
        time.sleep(5)
        conn, addr = server.accept()
        print("Client Connected Again")
        ###Get on or off value from client and update server
        data2 = handle_client(conn, addr)
        #Checks if a disconnect msg was sent from the client, if so get out of loop else update value in db and ts
        if data2 == DISCONNECT_MESSAGE:
            connected1 = False
        else:
        #make string and send to database to be updated
            rpiS_list = [str(20),str(2), data2]
            print(rpiS_list)
            join_stringS = ",".join(rpiS_list)
            print(join_stringS)
            update_Switch(join_stringS, conn, addr)
            print("SwPI values updated")



    print_Table()


