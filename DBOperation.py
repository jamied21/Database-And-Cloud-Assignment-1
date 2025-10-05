import sqlite3
from tabulate import tabulate
import pandas as pd
import re
from destination import Destination
from flight import Flight
from datetime import datetime
from pilot import Pilot

class DBOperations:
  sql_create_table_firsttime = "create table if not exists "

  sql_insert_flight = '''INSERT INTO flights (departure_time, status, pilot_id, origin_id, destination_id) VALUES (?, ?, ?, ?, ?)'''
  sql_insert_pilot= '''INSERT INTO pilots (name) VALUES (?)'''
  sql_insert_destination = '''INSERT INTO destinations (airport, country, city) VALUES (?, ?, ?)'''

  sql_select_all = '''SELECT flights.*, destinations.city AS [Destination], pilots.name AS [Pilot Name] FROM flights INNER JOIN pilots ON flights.pilot_id = pilots.pilot_id INNER JOIN destinations ON flights.destination_id = destinations.destination_id ORDER BY departure_time ASC'''
  sql_search = '''SELECT flights.*, destinations.city AS [Destination], pilots.name AS [Pilot Name] FROM flights INNER JOIN pilots on flights.pilot_id = pilots.pilot_id INNER JOIN destinations on flights.destination_id = destinations.destination_id WHERE flights.{} = ? '''
  sql_update_data = '''UPDATE {} SET {} WHERE {} = ?'''
  sql_delete_data = '''DELETE FROM flights WHERE flight_id = ?'''

  def __init__(self):
    try:
      self.conn = sqlite3.connect("mydb.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
    except Exception as e:
        print("Unexpected error:", e)
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
        print("Unexpected error:", e)
    finally:
      self.conn.close()

  """
      Creates a record of either a flight, pilot or destination depending on user's choice
  """
  def insert_data(self):
    try:
      self.get_connection()

      # Ensures non-existent foreign keys are not entered
      self.cur.execute("PRAGMA foreign_keys = ON")

      print(" Which table do you want to insert into? Please ")
      print(" 1. Flights")
      print(" 2. Pilots")
      print(" 3. Destinations")

      #Validate user's choice
      while True:
          user_input = input("Enter your choice ")
          if user_input in ['1','2','3']:
              break
          print("Invalid choice, please enter '1' or '2' or '3'")

      #Create a record depending in the input selected
      if  user_input == '1':
          flight = Flight()
          flight.set_departure_time(self.get_valid_departure_date_and_time())
          flight.set_status(self.get_valid_flight_status())
          flight.set_pilot_id(self.get_valid_id("Enter Pilot ID: "))
          flight.set_origin_id(self.get_valid_id("Enter Origin ID: "))
          flight.set_destination_id(self.get_valid_id("Enter Destination ID: "))
          self.cur.execute(self.sql_insert_flight, tuple(str(flight).split("\n")))

      elif user_input == '2':
          pilot = Pilot()
          pilot.set_name(self.get_valid_string_input("Enter Pilot Name:"))
          self.cur.execute(self.sql_insert_pilot, (pilot.get_name(),))

      elif user_input == '3':
          destination = Destination()
          destination.set_airport(self.get_valid_airport_code("Enter Airport Code: "))
          destination.set_country(self.get_valid_string_input("Enter Country:"))
          destination.set_city(self.get_valid_string_input("Enter City:"))
          self.cur.execute(self.sql_insert_destination, (destination.get_airport(), destination.get_country(), destination.get_city()))

      else:
          print("Invalid input")

      self.conn.commit()
      print("Inserted data successfully")

    #Catch any FK constraints or other constraints from the Flight's table
    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e):
            print("The Origin ID and Destination ID cannot be the same")
        elif "FOREIGN KEY constraint failed" in str(e):
            print("The Pilot ID, Origin ID or Destination ID do not exist")
        else:
            print("Something went wrong when trying to insert data")
    except Exception as e:
        print("Unexpected error:", e)
    finally:
      self.conn.close()

  """
       Shows the entire Flights table and adds the Pilot and Destination City names
  """
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      all_rows = self.cur.fetchall()
      column_names = [description[0] for description in self.cur.description]
      self.display_results(all_rows, column_names)

    except Exception as e:
        print("Unexpected error:", e)
    finally:
      self.conn.close()

  """
       Handles Search Data menu
  """
  def search_data_menu(self):
     print(" Please Search for a flight using one of the following Criteria:")
     print(" 1. Flight ID")
     print(" 2. Pilot ID")
     print(" 3. Destination ID")
     print(" 4. Departure Time")

     #Validate user choice
     while True:
         criteria_selected = input("Enter your choice ").strip()
         if criteria_selected in ['1', '2', '3', '4']:
             break
         print("Invalid choice, please enter '1' or '2' or '3' or '4'")

     #Search for record based on the criteria selected
     if criteria_selected == '1':
         selected_column = 'flight_id'
         output = self.get_valid_id("Enter Flight ID: ")
         self.search_data(output, selected_column)
     elif criteria_selected == '2':
         selected_column = 'pilot_id'
         output = self.get_valid_id("Enter Pilot ID: ")
         self.search_data(output, selected_column)
     elif criteria_selected == '3':
         selected_column = 'destination_id'
         output = self.get_valid_id("Enter Destination ID: ")
         self.search_data(output, selected_column)
     elif criteria_selected == '4':
         selected_column = 'departure_time'
         output = self.get_valid_departure_date()
         self.search_data(output, selected_column)

  """ Searches for the record based on a id and table chosen
       
    Args:
        id_input (int): The id of the record
        table_column (str): The column name of the table

    Returns:
       dataframe: A panda dataframe containing record searched for based on the criteria
       
  """
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
        print("Unexpected error:", e)
    finally:
      self.conn.close()

  """ 
      Counts number of flights per Destination, Pilot or flight status
      
      Returns:
           dataframe: A panda dataframe of the number of flights grouped by Destination ID, Pilot ID or flight status
  """
  def aggregate_data(self):
    try:
      self.get_connection()

      print("Summarise flight data by:")
      print(" 1. Destination")
      print(" 2. Pilot")
      print(" 3. Flight Status")

      while True:
          input_choice = input("Enter your choice as a number: ").strip()
          if input_choice in ['1', '2', '3']:
              break
          print("Invalid choice, please enter '1' or '2' or '3'")

      if input_choice == '1':
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], destinations.city AS [City] FROM flights INNER JOIN destinations ON flights.destination_id = destinations.destination_id GROUP BY destinations.city"
      elif input_choice == '2':
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], pilots.name AS [Pilot] FROM flights INNER JOIN pilots ON flights.pilot_id = pilots.pilot_id GROUP BY pilots.name"
      elif input_choice == '3':
          self.sql_aggregate_data = "SELECT COUNT(*) AS [Number of Flights], flights.status AS [Status] FROM flights GROUP BY flights.status"

      self.cur.execute(self.sql_aggregate_data)
      all_rows = self.cur.fetchall()
      column_names = [description[0] for description in self.cur.description]
      self.display_results(all_rows, column_names)

    except Exception as e:
        print("Unexpected error:", e)
    finally:
        self.conn.close()

  """ 
        Updates flight, pilot or a destination record
    """
  def update_data(self):
    try:
      self.get_connection()

      # Ensures non-existent foreign keys are not entered
      self.cur.execute("PRAGMA foreign_keys = ON")
      print("Which table would you like to update?")
      print(" 1. Flights")
      print(" 2. Pilots")
      print(" 3. Destinations")

      while True:
          input_choice = input("Enter your choice as a number: ").strip()
          if input_choice in ['1', '2', '3']:
              break
          print("Invalid choice, please enter '1' or '2' or '3'")

      if input_choice == '1':
          self.update_flights()
      if input_choice == '2':
          self.update_pilots()
      if input_choice == '3':
          self.update_destinations()

      ## TODO: Print previous pilot, destination and then result? e.g John Cena -> Jane Doe

    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e):
            print("Error: The Origin ID and Destination ID cannot be the same")
        elif "FOREIGN KEY constraint failed" in str(e):
            print("Error: The Pilot ID, Origin ID or Destination ID do not exist")
        else:
            print("Something went wrong when updating the data")
    except Exception as e:
        print("Unexpected error:", e)
    finally:
      self.conn.close()

  """ 
        Searches for flight ID and then updates flight record, can update multiple columns at once or select just one column
        
        Takes input as comma separated numerical values
  """
  def update_flights(self):

      while True:
          flight_id = self.get_valid_id("Enter Flight ID: ")
          if self.check_if_record_exists("flights","flight_id",flight_id):
              break
          else:
              print(f"No flight found with ID: {flight_id}. Please try again.")

      #Choice of columns to update
      print("Which data would you like to update?")
      print(" 1. Departure Time")
      print(" 2. Origin ID")
      print(" 3. Status")
      print(" 4. Pilot ID")
      print(" 5. Destination ID")

      valid_flight_choices = ['1', '2', '3', '4', '5']

      choices = self.get_valid_choices(valid_flight_choices)
      column_and_values_to_update = {}

      #Get columns to update and new values to insert into the record
      for choice in choices:
          if choice == '1':
              column = "departure_time"
              new_value = self.get_valid_departure_date_and_time()
              column_and_values_to_update.update({column: new_value})
          elif choice == '2':
              column = "origin_id"
              new_value = self.get_valid_id("Enter ID: ")
              column_and_values_to_update.update({column: new_value})
          elif choice == '3':
              column = "status"
              new_value = self.get_valid_flight_status()
              column_and_values_to_update.update({column: new_value})
          elif choice == '4':
              column = "pilot_id"
              new_value = self.get_valid_id("Enter ID: ")
              column_and_values_to_update.update({column: new_value})
          elif choice == '5':
              column = "destination_id"
              new_value = self.get_valid_id("Enter ID: ")
              column_and_values_to_update.update({column: new_value})

      columns = ", ".join([f"{col} = ?" for col in column_and_values_to_update.keys()])
      values = list(column_and_values_to_update.values())
      values.append(flight_id)

      self.cur.execute(self.sql_update_data.format('flights',columns, 'flight_id'), tuple(values))
      self.conn.commit()
      if self.cur.rowcount != 0:
          print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
          print("Cannot find this record in the database")

  """ 
        Searches for destination ID and updates destination record, can update multiple columns at once or select just one column

        Takes input as comma separated numerical values
  """
  def update_destinations(self):
      while True:
          destination_id = self.get_valid_id("Enter Destination ID: ")
          if self.check_if_record_exists("destinations","destination_id",destination_id):
              break
          else:
              print(f"No destination found with ID: {destination_id}. Please try again.")

      print("Which data would you like to update?")
      print(" 1. Airport")
      print(" 2. Country")
      print(" 3. City")

      valid_destination_choices = ['1', '2', '3']

      choices = self.get_valid_choices(valid_destination_choices)

      column_and_values_to_update = {}
      for choice in choices:
          if choice == '1':
              column = "airport"
              new_value = self.get_valid_airport_code("Enter Airport Code: ")
              column_and_values_to_update.update({column: new_value})
          elif choice == '2':
              column = "country"
              new_value = self.get_valid_string_input("Enter Country: ")
              column_and_values_to_update.update({column: new_value})
          elif choice == '3':
              column = "city"
              new_value = self.get_valid_string_input("Enter City: ")
              column_and_values_to_update.update({column: new_value})

      columns = ", ".join([f"{col} = ?" for col in column_and_values_to_update.keys()])
      values = list(column_and_values_to_update.values())
      values.append(destination_id)

      self.cur.execute(self.sql_update_data.format('destinations', columns,'destination_id'), tuple(values))
      self.conn.commit()
      if self.cur.rowcount != 0:
          print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
          print("Cannot find destination record in the database")

  """ 
        Searches for pilot ID and updates pilot record, updates pilot name
  """
  def update_pilots(self):

      while True:
          pilot_id = self.get_valid_id("Enter Pilot ID: ")
          if self.check_if_record_exists("pilots", "pilot_id", pilot_id):
              break
          else:
              print(f"No Pilot found with ID: {pilot_id}. Please try again.")

      new_pilot_name = self.get_valid_string_input("Enter Pilot Name: ")

      self.cur.execute(self.sql_update_data.format('pilots', 'name = ?','pilot_id'), (new_pilot_name, pilot_id))
      self.conn.commit()
      if self.cur.rowcount != 0:
          print(str(self.cur.rowcount) + "Row(s) affected.")
      else:
          print("Cannot find pilot record in the database")

## TODO: Need to check if can be done for Pilot
  """ 
        Deletes a flight record based on flight ID entered by the user
  """
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

  """ Display the results of the record or records
       
    Args:
        data (any): data returned from the SQL query
        table_column (list): The column name of the table

    Returns:
       dataframe: A panda dataframe of the results of the SQL query
       
  """
  def display_results(self,data, columns):
      if data:
          df = pd.DataFrame(data, columns=columns)
          print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
      else:
          print("No records available.")

  """ 
      Ensures departure date and time that is entered by the user is in YYYY-MM-DD HH:MM format
  """
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

  """ 
      Ensures departure date and time that is entered by the user is in YYYY-MM-DD format
  """
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

  """ Ensures Id entered by the user is an integer
  
       Args:
            input_message (str): Custom user input message for the user
    
        Returns:
           integer: The id entered by the user
  """
  def get_valid_id(self,input_message):
      while True:
          try:
              user_input = int(input(input_message).strip())
              return user_input
          except ValueError:
              print("Invalid input. Please enter a valid integer for ID.")

  """ Ensures Flight Status entered by the user is from the available choices of Delayed, Scheduled or On Time
         
         Returns:
            string: The flight status entered by the user
   """
  def get_valid_flight_status(self):
      valid_choices = ["Delayed", "On Time", "Scheduled","Cancelled"]
      while True:
          user_input = input("Enter Flight Status: ").strip().lower().title()

          if user_input in valid_choices:
              return user_input
          else:
              print("Please enter a status of either 'Delayed', 'On Time', 'Scheduled' or 'Cancelled' ")

  """ Ensures input entered by the user is a valid string with no numbers or special characters

       Args:
            input_message (str): Custom user input message for the user

        Returns:
           string: The input entered by the user
  """
  def get_valid_string_input(self, input_message):
      regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
      while True:

              user_input = input(input_message).strip()
              if user_input == "":
                  print("Input cannot be empty.")
              elif any(char.isdigit() for char in user_input):
                  print("Invalid input. The input contain numbers.")
              elif regex.search(user_input):
                  print("Invalid Input. The input contains special characters")
              else:
                  return user_input.lower().title()

  """ Ensures input entered by the user is a valid Airport code with no numbers or special characters

        Args:
             input_message (str): Custom user input message for the user

         Returns:
            string: The airport code entered by the user
   """
  def get_valid_airport_code(self, input_message):
      regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
      while True:
          user_input = input(input_message).strip()

          if user_input == "":
              print("Input cannot be empty.")
          elif len(user_input) != 3:
              print("Airport Code must be 3 characters long.")
          elif regex.search(user_input):
              print("Invalid Input. The input contains special characters")
          elif any(char.isdigit() for char in user_input):
              print("Invalid input. The input contain numbers.")
          elif self.check_if_airport_exists(user_input):
              print("Airport already exists.")
          else:
              return user_input

  """ Checks if the record exists

         Args:
              table (str): Table being checked
              column (str): Column being checked
              record_id (int): Record ID being checked

          Returns:
             boolean: True if the record exists in the table, false otherwise
    """
  def check_if_record_exists(self,table,column,record_id):
      try:
          sql_query = "SELECT * FROM {} WHERE {} = ?"
          self.cur.execute(sql_query.format(table,column), (record_id,))
          result = self.cur.fetchone()
          return result is not None
      except Exception as e:
          print(f"Error checking if record exists: {e}")

  """ Checks if the record exists

         Args:
              airport (str): Airport Code being checked for existence
          Returns:
             boolean: True if the airport code already exists in the destinations table, false otherwise
    """
  def check_if_airport_exists(self,airport):
      try:
          self.cur.execute("SELECT * FROM destinations WHERE airport = ?", (airport,))
          result = self.cur.fetchone()
          return result is not None
      except Exception as e:
          print(f"Error checking if airport exists: {e}")


  """ Checks if the record exists

         Args:
              valid_choices (list): List of valid choices/options that can be entered by the user
            
          Returns:
             list: list of valid input that has been entered by the user, otherwise error message
    """
  def get_valid_choices(self,valid_choices):
      while True:
          user_input = input("Enter one or more column to update as a number separated by a comma e.g 1,2,3: ").strip()
          if len(user_input) == 0:
              print("Input cannot be empty.")
              continue
          elif any(c not in "0123456789, " for c in user_input):
              print("Invalid input. Only numbers and commas are allowed.")
          choices = user_input.split(",")
          invalid_choices = [c for c in choices if c not in valid_choices]
          if len(invalid_choices) > 0:
              print("Invalid choices: " + ", ".join(invalid_choices))
          else:
              unique_choices = sorted(set(choices))
              return unique_choices

