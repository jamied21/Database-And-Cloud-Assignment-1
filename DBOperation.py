import sqlite3
from tabulate import tabulate
import pandas as pd
from flight import Flight
from datetime import datetime
from destination import Destination
from pilot import Pilot

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = "create table if not exists "

  sql_create_table = "create table TableName"

  sql_insert = '''INSERT INTO flights (departure_time, origin, status, pilot_id, destination_id) VALUES (?, ?, ?, ?, ?)'''
  sql_select_all = '''SELECT * FROM flights ORDER BY departure_time ASC'''
  sql_search = '''SELECT * FROM flights WHERE {} = ?'''
  sql_alter_data = ""
  sql_update_data = '''UPDATE flights SET {} = ? WHERE flight_id = ?'''
  sql_delete_data = '''DELETE FROM flights WHERE flight_id = ?'''
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

  # TODO: Use a join to show Pilots' names and destination names
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

  def search_data_menu(self):
     print(" Please Search for a flight using one of the following Criteria:")
     print(" 1. Flight ID")  ## Already created from inject_data file, db should carry over
     print(" 2. Pilot ID")
     print(" 3. Destination ID")

     criteria_selected = int(input("Enter criteria to search for: "))

     if criteria_selected == 1:
         column = 'flight_id'
         output = int(input("Enter Flight ID: "))
         self.search_data(output, column)
     elif criteria_selected == 2:
         column = 'pilot_id'
         output = int(input("Enter Pilot ID: "))
         self.search_data(output, column)
     elif criteria_selected == 3:
         column = 'destination_id'
         output = int(input("Enter Destination ID: "))
         self.search_data(output, column)
     else:
         print("Invalid Choice")

    ### Search by variety of criteria e.g destination, Pilot Id or Name and flight Id
    ### Will need to update search query to adjust for this
  def search_data(self, id_input, column):
    try:
      self.get_connection()
      self.cur.execute(self.sql_search.format(column), (id_input,))
      result = self.cur.fetchone()
      print("\n\n")

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

  @staticmethod
  def get_valid_departure_time():
      while True:
          user_input = input("Enter Departure Time (YYYY-MM-DD HH:MM): ")
          try:
              # Seconds are not used for input
              dt = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
              return dt.strftime("%Y-%m-%d %H:%M:00")
          except ValueError:
              print("Invalid format. Please use the format YYYY-MM-DD HH:MM.")
          except Exception as e:
              print("Unexpected error:", e)


  def update_data(self):
    try:
      self.get_connection()

      flight_id = int(input("Enter Flight ID to update: "))

      print("Which data would you like to update?")
      print(" 1. Departure Time")
      print(" 2. Origin")
      print(" 3. Status")
      print(" 4. Pilot ID")
      print(" 5. Destination ID")

      choice = int(input("Enter your choice "))
      column_to_update = ''

      if choice == 1:
          column_to_update = "departure_time"
      elif choice == 2:
          column_to_update = "origin"
      elif choice == 3:
          column_to_update = "status"
      elif choice == 4:
          column_to_update = "pilot_id"
      elif choice == 5:
          column_to_update = "destination_id"
      else:
          print("Invalid Choice")

      if choice == 1:
          new_value = self.get_valid_departure_time()
      elif choice == 4 or choice == 5:
          new_value = int(input("Enter ID: "))
      else:
          new_value = input("Enter new value:")

      self.cur.execute(self.sql_update_data.format(column_to_update), (new_value, flight_id))
      self.conn.commit()
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


## TODO: Validate status choices

## TODO: Validate if int and catch


# Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.

  def delete_data(self):
    try:
      self.get_connection()
      flight_id = int(input("Enter Flight ID to delete: "))

      self.cur.execute(self.sql_delete_data, (flight_id,))
      self.conn.commit()

      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()