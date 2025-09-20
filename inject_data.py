import sqlite3

#Used to create the tables and inject mock data

db = sqlite3.connect("mydb.db")

cursor = db.cursor()
print("Db made")

cursor.execute("DROP TABLE IF EXISTS pilots")
cursor.execute("DROP TABLE IF EXISTS destinations")
cursor.execute("DROP TABLE IF EXISTS flights")

#Create initial tables
cursor.execute("CREATE TABLE pilots (pilot_id INTEGER NOT NULL, name TEXT, PRIMARY KEY (pilot_id))")

cursor.execute("CREATE TABLE destinations (destination_id INTEGER NOT NULL, country TEXT, city TEXT, PRIMARY KEY (destination_id))")

cursor.execute("CREATE TABLE flights (flight_id INTEGER NOT NULL, departure_time DATETIME, origin TEXT, status TEXT, pilot_id INTEGER NOT NULL, destination_id INTEGER NOT NULL, PRIMARY KEY (flight_id), FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id), FOREIGN KEY (destination_id) REFERENCES destinations(destination_id))")

#Inject mock data
cursor.execute ('''INSERT INTO pilots (name) VALUES
('Amelia Earhart'),
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


cursor.execute ('''INSERT INTO destinations (country, city) VALUES
('USA', 'New York'),
('UK', 'London'),
('France', 'Paris'),
('Japan', 'Tokyo'),
('Australia', 'Sydney'),
('Brazil', 'Rio de Janeiro'),
('South Africa', 'Cape Town'),
('UAE', 'Dubai'),
('Canada', 'Toronto'),
('Germany', 'Berlin'),
('Italy', 'Rome'),
('China', 'Beijing'),
('India', 'Delhi'),
('Mexico', 'Mexico City'),
('Spain', 'Madrid')''')


cursor.execute('''INSERT INTO flights (departure_time, origin, status, pilot_id, destination_id) VALUES
('2025-09-21 08:00:00', 'Los Angeles', 'Scheduled', 1, 1),
('2025-09-21 12:30:00', 'London', 'On Time', 2, 2),
('2025-09-21 15:00:00', 'Paris', 'Delayed', 3, 3),
('2025-09-22 09:45:00', 'Tokyo', 'Scheduled', 4, 4),
('2025-09-22 18:00:00', 'Sydney', 'Cancelled', 5, 5),
('2025-09-23 07:15:00', 'Rio de Janeiro', 'Scheduled', 6, 6),
('2025-09-23 11:00:00', 'Cape Town', 'On Time', 7, 7),
('2025-09-23 14:30:00', 'Dubai', 'Delayed', 8, 8),
('2025-09-24 10:00:00', 'Toronto', 'Scheduled', 9, 9),
('2025-09-24 16:45:00', 'Berlin', 'On Time', 10, 10),
('2025-09-25 06:00:00', 'Rome', 'Scheduled', 11, 11),
('2025-09-25 13:30:00', 'Beijing', 'Delayed', 12, 12),
('2025-09-25 19:15:00', 'Delhi', 'On Time', 13, 13),
('2025-09-26 08:20:00', 'Mexico City', 'Scheduled', 14, 14),
('2025-09-26 17:00:00', 'Madrid', 'Cancelled', 15, 15)
''')



db.commit()
cursor.close()