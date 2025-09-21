from DBOperation import DBOperations


class FlightInfo:

  def __init__(self):
    self.flightID = 0
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''

  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_origin(self, flightOrigin):
    self.flight_origin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flight_destination = flightDestination

  def set_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flight_origin(self):
    return self.flightOrigin

  def get_flight_destination(self):
    return self.flightDestination

  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)


# The main function will parse arguments.
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Create table FlightInfo")
  print(" 2. Insert data into FlightInfo")
  print(" 3. Select all data from FlightInfo")
  print(" 4. Search a flight")
  print(" 5. Update data some records")
  print(" 6. Delete data some records")
  print(" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print("Invalid Choice")
