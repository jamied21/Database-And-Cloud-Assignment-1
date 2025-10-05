# Database-And-Cloud-Assignment-1

A simple **Python console application** to manage flights, pilots, and destinations using **SQLite** as the database. The system allows users to **create, read, update, delete, search, and summarise flight-related data**. Includes mock data for initial testing.

## Features

* **Reset database with mock data**
* **Add new record**: Flights, Pilots, or Destinations
* **View all flights** with pilot and destination information
* **Search flights** by Flight ID, Pilot ID, Destination ID, or Departure Time
* **Update record**: Flights, Pilots, or Destinations
* **Delete record** with safety checks for pilots and destinations used in flights
* **Aggregate data**: Count flights by Pilot, Destination, or Flight Status

## Requirements

* Python **3.8+**
* SQLite (built into Python standard library)
* Python libraries:

  * `pandas`
  * `tabulate`



## Getting Started

**Install dependencies**

```bash
pip install pandas tabulate
```

Run the main script:

```bash
python main.py
```

A menu will appear in the console:

```
 Menu:
**********
 1. Reset data to mock data
 2. Create a new flight, destination or pilot record
 3. View all Flights
 4. Search a flight
 5. Update a flight, destination or pilot record
 6. Delete a flight, destination or pilot record
 7. Summarise data
 8. Exit
```

Enter the corresponding number to perform the action.

## Notes

* **Database file:** `mydb.db` is created automatically in the project directory.
* **Data validation:** Input fields are validated to ensure correct data types, formats, and foreign key constraints.
* **Airport codes:** Must be 3-letter codes and unique.
* **Flight constraints:** Origin and destination cannot be the same.
