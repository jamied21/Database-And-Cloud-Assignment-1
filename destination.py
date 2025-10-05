class Destination:
    def __init__(self, destination_id = None, airport = '', country = '', city = ''):
        self.destination_id = destination_id
        self.airport = airport
        self.country = country
        self.city = city

    def get_destination_id(self):
        return self.destination_id

    def set_destination_id(self,destination_id):
      self.destination_id = destination_id

    def set_airport(self, airport):
        self.airport = airport

    def get_airport(self):
        return self.airport

    def get_country(self):
        return self.country

    def set_country(self,country):
        self.country = country

    def get_city(self):
        return self.city

    def set_city(self,city):
        self.city = city

    def __str__(self):
        return "Destination ID: {}, Airport {}, Country: {}, City {}".format( self.airport, self.country, self.city)