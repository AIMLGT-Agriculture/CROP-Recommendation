class Direct_Parameters():
    def __init__(self,crop_list,state,district, latitude, longitude, aesr, market, year, season):
        self.crop_list = crop_list  # Choice of crops that farmer wants to grow OR Crops selected by the government for a particular year
        self.location = {'Latitude':latitude, 'Longitude':longitude,'Market':market,'District':district,'State':state, 'Country':'India'}  # It contains the geographical location of the farmer
        self.time = {'Day':None, 'Year':year, 'Season':season}
        self.aesr = aesr
        
