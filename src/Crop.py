
class Crop:
    def __init__(self, names, commodity_code, sowing_period, harvest_period, data_files, cycle_time, last_year_yields, actual_yield):
        self.names=names                                #Name of the Crop
        self.sowing_period = sowing_period              #sowing period list will contain all the months in which a crop can be grown
        self.data_files = data_files                    #file contains the data for the crop
        self.commodity_code = commodity_code            #commodity code for the crop
        self.cycle_time = cycle_time
        self.harvest_period = harvest_period            #harvest period list will contain all the months in which a crop can be harvest      
        self.last_year_yields = last_year_yields
        self.actual_yield = actual_yield
