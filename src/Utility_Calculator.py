class Utility_Calculator():
    def __init__(self, direct_parameters, weather_paramters):
        self.direct_parameters=direct_parameters
        self.weather_paramters = weather_paramters

    def set_derived_paramters(self):

        self.derived_parameters = None

    def get_utility_distribution(self, crop, utility):
        return utility.calculate_utility(crop, self.direct_parameters, self.weather_paramters)
