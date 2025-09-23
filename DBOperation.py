import sqlite3
from tabulate import tabulate
import pandas as pd
from flight import Flight
from destination import Destination
from pilot import Pilot

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = "create table if not exists "

  sql_create_table = "create table TableName"

  sql_insert = '''INSERT INTO flights (departure_time, origin, status, pilot_id, destination_id) VALUES (?, ?, ?, ?, ?)'''
  sql_select_all = '''SELECT * FROM flights ORDER BY departure_time ASC'''
  sql_search = "select * from flights where FlightID = ?"
  sql_alter_data = ""
  sql_update_data = ""
  sql_delete_data = ""
  sql_drop_table = ""

  def __init__(self):
    try:
      self.conn = sqlite3.connect("mydb.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("mydb.db")
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table)
      self.conn.commit()
      print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      flight = Flight()
      flight.set_departure_time(input("Enter Departure Time: "))
      flight.set_origin(input("Enter Flight Origin: "))
      flight.set_status(input("Enter Status: "))
      flight.set_pilot_id(int(input("Enter Pilot ID: ")))
      flight.set_destination_id(int(input("Enter Destination ID: ")))

      self.cur.execute(self.sql_insert, tuple(str(flight).split("\n"))) ### Need to insert multiple values in one statment

      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


# Use a join to show Pilots name and destination name
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      all_rows = self.cur.fetchall()
      df = pd.DataFrame(all_rows, columns=['Flight ID', 'Departure Time', 'Origin', 'Status', 'Pilot ID', 'Destination ID'])
      print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


    ### Search by variety of criteria e.g destination, Pilot Id or Name and flight Id
    ### Will need to update search query to adjust for this
  def search_data(self):
    try:
      self.get_connection()

      # give user choice of criteria to search by e.g destination, pilot, flight and status


      flight_id = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple(str(flight_id)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Origin: " + detail)
          elif index == 2:
            print("Flight Destination: " + detail)
          else:
            print("Status: " + str(detail))
      else:
        print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


def summarise_date(self):
    try:
      self.get_connection()
      # TODO: Add aggregate queries e.g count, average, min and max

    except Exception as e:
       print(e)
    finally:
        self.conn.close()


#   def update_data(self):
#     try:
#       self.get_connection()
#
#       # Update statement
#
#       if result.rowcount != 0:
#         print(str(result.rowcount) + "Row(s) affected.")
#       else:
#         print("Cannot find this record in the database")
#
#     except Exception as e:
#       print(e)
#     finally:
#       self.conn.close()
#
#
# # Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.
#
#   def delete_data(self):
#     try:
#       self.get_connection()
#
#       if result.rowcount != 0:
#         print(str(result.rowcount) + "Row(s) affected.")
#       else:
#         print("Cannot find this record in the database")
#
#     except Exception as e:
#       print(e)
#     finally:
#       self.conn.close()