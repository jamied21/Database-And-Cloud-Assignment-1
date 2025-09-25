import sqlite3
from tabulate import tabulate
import pandas as pd
from flight import Flight
from datetime import datetime

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

class DBOperations:
  sql_create_table_firsttime = "create table if not exists " ## TODO: Make method that just copies the inject_data file

  sql_create_table = "create table TableName"

  sql_insert = '''INSERT INTO flights (departure_time, origin, status, pilot_id, destination_id) VALUES (?, ?, ?, ?, ?)'''
  sql_select_all = '''SELECT * FROM flights ORDER BY departure_time ASC'''
  sql_search = '''SELECT * FROM flights WHERE {} = ?'''
  sql_alter_data = ""
  sql_update_data = '''UPDATE flights SET {} = ? WHERE flight_id = ?'''
  sql_delete_data = '''DELETE FROM flights WHERE flight_id = ?'''
  sql_drop_table = ""
  sql_aggregate_data = ""

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
  # TODO: Test casing and spaces
  # TODO: Use a join to show Pilots' names and destination names
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      all_rows = self.cur.fetchall()
      column_names = [description[0] for description in self.cur.description]
      df = pd.DataFrame(all_rows, columns=column_names)
      print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

    ## TODO: Add search by date
  def search_data_menu(self):
     print(" Please Search for a flight using one of the following Criteria:")
     print(" 1. Flight ID")  ## Already created from inject_data file, db should carry over
     print(" 2. Pilot ID")
     print(" 3. Destination ID")

     criteria_selected = int(input("Enter criteria to search for: "))

     if criteria_selected == 1:
         selected_column = 'flight_id'
         output = int(input("Enter Flight ID: "))
         self.search_data(output, selected_column)
     elif criteria_selected == 2:
         selected_column = 'pilot_id'
         output = int(input("Enter Pilot ID: "))
         self.search_data(output, selected_column)
     elif criteria_selected == 3:
         selected_column = 'destination_id'
         output = int(input("Enter Destination ID: "))
         self.search_data(output, selected_column)
     else:
         print("Invalid Choice")

  def search_data(self, id_input, table_column):
    try:
      self.get_connection()
      self.cur.execute(self.sql_search.format(table_column), (id_input,))
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

  def aggregate_data(self):
    try:
      self.get_connection()

      print("Summarise flight data by:")
      print(" 1. Destination")
      print(" 2. Pilot")
      print(" 3. Flight Status")

      input_choice = int(input("Enter your choice as a number: "))

      if input_choice == 1:
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], destinations.city AS [City] FROM flights INNER JOIN destinations ON flights.destination_id = destinations.destination_id GROUP BY destinations.city"
      elif input_choice == 2:
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], pilots.name AS [Pilot] FROM flights INNER JOIN pilots ON flights.pilot_id = pilots.pilot_id GROUP BY pilots.name"
      elif input_choice == 3:
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], flights.status AS [Status] FROM flights GROUP BY flights.status"

      self.cur.execute(self.sql_aggregate_data)
      all_rows = self.cur.fetchall()
      column_names = [description[0] for description in self.cur.description]
      df = pd.DataFrame(all_rows, columns=column_names)
      print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
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


## TODO: Validate status choices e.g check they from On Time, Scheduled, Delayed.
# Also ensure consistency in casing and space so if user enters all lower case it is set to the correct format e.g delayed to Delayed on time to On Time

## TODO: Validate if int and catch errors if not

## TODO: Add method for display data

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