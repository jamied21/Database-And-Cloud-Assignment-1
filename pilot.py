class Pilot:
    def __init__(self, pilot_id = None, name = ''):
        self.pilot_id = pilot_id
        self.name = name

    def get_pilot_id(self):
        return self.pilot_id

    def set_pilot_id(self, pilot_id):
        self.pilot_id = pilot_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return "Name: {}".format(self.name)

