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
  sql_select_all = '''SELECT flights.*, destinations.city AS [Destination], pilots.name AS [Pilot Name] FROM flights INNER JOIN pilots ON flights.pilot_id = pilots.pilot_id INNER JOIN destinations ON flights.destination_id = destinations.destination_id ORDER BY departure_time ASC'''
  sql_search = '''SELECT flights.*, destinations.city AS [Destination], pilots.name AS [Pilot Name] FROM flights INNER JOIN pilots on flights.pilot_id = pilots.pilot_id INNER JOIN destinations on flights.destination_id = destinations.destination_id WHERE flights.{} = ? '''
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

  def create_tables_and_inject_mock_data(self):
    try:
      self.get_connection()

      self.cur.execute("DROP TABLE IF EXISTS pilots")
      self.cur.execute("DROP TABLE IF EXISTS destinations")
      self.cur.execute("DROP TABLE IF EXISTS flights")

      # Create initial tables
      self.cur.execute("CREATE TABLE pilots (pilot_id INTEGER NOT NULL, name TEXT, PRIMARY KEY (pilot_id))")

      self.cur.execute(
          "CREATE TABLE destinations (destination_id INTEGER NOT NULL, airport CHAR(3) NOT NULL UNIQUE, country TEXT, city TEXT, PRIMARY KEY (destination_id))")

      self.cur.execute(
          "CREATE TABLE flights (flight_id INTEGER NOT NULL, departure_time DATETIME, status TEXT, pilot_id INTEGER NOT NULL, origin_id INTEGER NOT NULL, destination_id INTEGER NOT NULL, PRIMARY KEY (flight_id), FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id), FOREIGN KEY (origin_id) REFERENCES destinations(destination_id), FOREIGN KEY (destination_id) REFERENCES destinations(destination_id), CHECK (origin_id <> destination_id))")

      # Inject mock data
      self.cur.execute('''INSERT INTO pilots (name)
                        VALUES ('Amelia Earhart'),
                               ('Charles Lindbergh'),
                               ('Sally Ride'),
                               ('Yuri Gagarin'),
                               ('Neil Armstrong'),
                               ('Buzz Aldrin'),
                               ('Bessie Coleman'),
                               ('Howard Hughes'),
                               ('Chesley Sullenberger'),
                               ('Eileen Collins'),
                               ('Jean Batten'),
                               ('Valentina Tereshkova'),
                               ('John Glenn'),
                               ('Richard Branson'),
                               ('Elon Musk')''')

      self.cur.execute('''
                       INSERT INTO destinations (airport, country, city)
                       VALUES ('JFK', 'USA', 'New York'),
                              ('LHR', 'UK', 'London'),
                              ('CDG', 'France', 'Paris'),
                              ('HND', 'Japan', 'Tokyo'),
                              ('SYD', 'Australia', 'Sydney'),
                              ('GIG', 'Brazil', 'Rio de Janeiro'),
                              ('CPT', 'South Africa', 'Cape Town'),
                              ('DXB', 'UAE', 'Dubai'),
                              ('YYZ', 'Canada', 'Toronto'),
                              ('BER', 'Germany', 'Berlin'),
                              ('FCO', 'Italy', 'Rome'),
                              ('PEK', 'China', 'Beijing'),
                              ('DEL', 'India', 'Delhi'),
                              ('MEX', 'Mexico', 'Mexico City'),
                              ('MAD', 'Spain', 'Madrid')
                       ''')

      self.cur.execute('''
                       INSERT INTO flights (departure_time, status, pilot_id, origin_id, destination_id)
                       VALUES ('2025-09-21 08:00:00', 'Scheduled', 1, 2, 1),
                              ('2025-09-21 12:30:00', 'On Time', 2, 1, 2),
                              ('2025-09-21 15:00:00', 'Delayed', 3, 3, 4),
                              ('2025-09-22 09:45:00', 'Scheduled', 4, 4, 5),
                              ('2025-09-22 18:00:00', 'Cancelled', 5, 5, 6),
                              ('2025-09-23 07:15:00', 'Scheduled', 6, 6, 7),
                              ('2025-09-23 11:00:00', 'On Time', 7, 7, 8),
                              ('2025-09-23 14:30:00', 'Delayed', 8, 8, 9),
                              ('2025-09-24 10:00:00', 'Scheduled', 9, 9, 10),
                              ('2025-09-24 16:45:00', 'On Time', 10, 10, 11),
                              ('2025-09-25 06:00:00', 'Scheduled', 11, 11, 12),
                              ('2025-09-25 13:30:00', 'Delayed', 12, 12, 13),
                              ('2025-09-25 19:15:00', 'On Time', 13, 13, 14),
                              ('2025-09-26 08:20:00', 'Scheduled', 14, 14, 15),
                              ('2025-09-26 17:00:00', 'Cancelled', 15, 15, 1)
                       ''')

      self.conn.commit()
      print("Tables and Mock data injected successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      # Ensures non-existent foreign keys are not entered
      self.cur.execute("PRAGMA foreign_keys = ON")

      flight = Flight()
      flight.set_departure_time(self.get_valid_departure_date_and_time())
      flight.set_origin(input("Enter Flight Origin: ").strip().title())
      flight.set_status(self.get_valid_flight_status())
      flight.set_pilot_id(self.get_valid_id("Enter Pilot ID: "))
      flight.set_destination_id(self.get_valid_id("Enter Destination ID: "))

      self.cur.execute(self.sql_insert, tuple(str(flight).split("\n"))) ### Need to insert multiple values in one statment

      self.conn.commit()
      print("Inserted data successfully")

    except sqlite3.IntegrityError:
        print("Error: The Pilot ID or Destination ID does not exist")
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
      column_names = [description[0] for description in self.cur.description]
      self.display_results(all_rows, column_names)

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_data_menu(self):
     print(" Please Search for a flight using one of the following Criteria:")
     print(" 1. Flight ID")
     print(" 2. Pilot ID")
     print(" 3. Destination ID")
     print(" 4. Departure Time")

     try:
         criteria_selected = int(input("Enter criteria to search for: ").strip())
         if criteria_selected == 1:
             selected_column = 'flight_id'
             output = self.get_valid_id("Enter Flight ID: ")
             self.search_data(output, selected_column)
         elif criteria_selected == 2:
             selected_column = 'pilot_id'
             output = self.get_valid_id("Enter Pilot ID: ")
             self.search_data(output, selected_column)
         elif criteria_selected == 3:
             selected_column = 'destination_id'
             output = self.get_valid_id("Enter Destination ID: ")
             self.search_data(output, selected_column)
         elif criteria_selected == 4:
             selected_column = 'departure_time'
             output = self.get_valid_departure_date()
             self.search_data(output, selected_column)
         else:
             print("Invalid Choice")
     except ValueError:
         print("Invalid input type. Please enter a number for IDs")

  def search_data(self, id_input, table_column):
    try:
      self.get_connection()
      if table_column == 'departure_time':
          sql_search_date = ''' SELECT flights.*, destinations.city AS [Destination], pilots.name AS [Pilot Name] FROM flights INNER JOIN pilots on flights.pilot_id = pilots.pilot_id INNER JOIN destinations on flights.destination_id = destinations.destination_id WHERE flights.{} LIKE ?'''
          self.cur.execute(sql_search_date.format(table_column), (id_input + '%',))
      else:
          self.cur.execute(self.sql_search.format(table_column), (id_input,))

      result = self.cur.fetchall()
      columns = [description[0] for description in self.cur.description]
      print("\n")
      self.display_results(result, columns)

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
      self.display_results(all_rows, column_names)

    except Exception as e:
       print(e)
    finally:
        self.conn.close()

  def update_data(self):
    try:
      self.get_connection()

      # Ensures non-existent foreign keys are not entered
      self.cur.execute("PRAGMA foreign_keys = ON")

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
          new_value = self.get_valid_departure_date_and_time()
      elif choice == 4 or choice == 5:
          new_value = self.get_valid_id("Enter ID: ")
      elif choice == 3:
          new_value = self.get_valid_flight_status()
      else:
          new_value = input("Enter new value:").strip().title()

      self.cur.execute(self.sql_update_data.format(column_to_update), (new_value, flight_id))
      self.conn.commit()
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except sqlite3.IntegrityError:
        print("Error: The Pilot ID or Destination ID does not exist")
    except Exception as e:
        print(e)
    finally:
      self.conn.close()

  def delete_data(self):
    try:
      self.get_connection()
      flight_id = self.get_valid_id("Enter Flight ID to delete: ")

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

  def display_results(self,data, columns):
      if data:
          df = pd.DataFrame(data, columns=columns)
          print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
      else:
          print("No records available.")

  def get_valid_departure_date_and_time(self):
      while True:
          user_input = input("Enter Departure Time (YYYY-MM-DD HH:MM): ")
          try:
              # Seconds are not used for input
              dt = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
              return dt.strftime("%Y-%m-%d %H:%M:00")
          except ValueError:
              print("Invalid Date or Time. Please use the format YYYY-MM-DD HH:MM.")
          except Exception as e:
              print("Unexpected error:", e)

  def get_valid_departure_date(self):
      while True:
          user_input = input("Enter Departure Date YYYY-MM-DD: ")
          try:
              dt = datetime.strptime(user_input, "%Y-%m-%d")
              return dt.strftime("%Y-%m-%d")
          except ValueError:
              print("Invalid Date. Please use the format YYYY-MM-DD.")
          except Exception as e:
              print("Unexpected error:", e)

  def get_valid_id(self,input_message):
      while True:
          try:
              user_input = int(input(input_message).strip())
              return user_input
          except ValueError:
              print("Invalid input. Please enter a valid integer for ID.")

  def get_valid_flight_status(self):
      valid_choices = ["Delayed", "On Time", "Scheduled","Cancelled"]
      while True:
          user_input = input("Enter Flight Status: ").strip().lower().title()

          if user_input in valid_choices:
              return user_input
          else:
              print("Please enter a status of either 'Delayed', 'On Time', 'Scheduled' or 'Cancelled' ")
