class Flight:
    def __init__(self, flight_id = None, departure_time = '', origin = '', status = '', pilot_id = 0, destination_id = 0):
        self.flight_id = flight_id
        self.departure_time = departure_time
        self.origin = origin
        self.status = status
        self.pilot_id = pilot_id
        self.destination_id = destination_id

    def get_flight_id(self):
        return self.flight_id

    def set_flight_id(self, flight_id):
        self.flight_id = flight_id

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        self.origin = origin

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_pilot_id(self):
        return self.pilot_id

    def set_pilot_id(self, pilot_id):
        self.pilot_id = pilot_id

    def get_destination_id(self):
        return  self.destination_id

    def set_destination_id(self, destination_id):
        self.destination_id = destination_id

    def __str__(self):
        return  str(self.departure_time) + "\n" + self.origin + "\n" + self.status + "\n" + str(self.pilot_id) + "\n" + str(self.destination_id)