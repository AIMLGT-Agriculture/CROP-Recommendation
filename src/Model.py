import streamlit as st
import Crop
import Distribution
import math
import pandas as pd
import re
import Crop_Price
import Utils
import Direct_Parameters
import Derived_Parameters
import Modifiedprice
import numpy as np
import pickle
from pickle import load, dump

import keras
import pandas as pd
import numpy as np
import math
from google.colab import drive
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten
from keras.layers import Input, LSTM, Dense, Dropout, TimeDistributed
import tensorflow as tf
import matplotlib.pyplot as plt
from pickle import dump, load
from sklearn.preprocessing import StandardScaler

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from datetime import date
import urllib
import urllib.parse
import csv
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.action_chains import ActionChains
#from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

class Model():
    def __init__(self):
        pass

    def get_prediction(self, crop, location, time):
        pass
        #return an object of Distribution




class Yield_last_year(Model):
    def __init__(self, n=1):
        self.type = "Yield"
        self.unit = "Tonnes/Hectare"
        self.n = n

    def get_crop_names(self, name):
        name = name.lower()
        res = re.findall( r'\w+|[^\s\w]+', name)
        return res

    def str_compare(self, str1, str2):
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        if str1 == str2:
            return True
        else:
            return False



    def get_prediction(self, crop, direct, derived):

        crop_names = crop.names
        #print("Crop Names = ",crop_names)
        crop_names = [s.lower() for s in crop_names]
        year = direct.time["Year"]
        state = direct.location["State"]
        district = direct.location["District"]
        season = direct.time["Season"]
        sample = pd.read_csv(crop.data_files[self.type])

        #print("file_name = ", crop.data_files[self.type])
        print(crop_names, year, state, district, season)
        #print("Length = ", len(sample))
        #print(sample.head())
        
        last_years = list(np.arange(year - self.n, year , 1))


        production = []
        area = []

        i=0
        flag = 0
        while i<len(sample):
            if  len([value for value in crop_names if value in self.get_crop_names(sample.iloc[i]["Crop"])])>=1 and self.str_compare(sample.iloc[i]["State_Name"],state) and self.str_compare(sample.iloc[i]["District_Name"],district) and sample.iloc[i]["Crop_Year"] in last_years and self.str_compare(season,sample.iloc[i]["Season"]):
                # print("Yield Data Found")
                production.append(sample.iloc[i]["Production"])
                area.append(sample.iloc[i]["Area"])
                #print(sample.iloc[i]["Crop_Year"])
                flag = 1
            i+=1
        
        
        if flag == 0:
            print("Yield data unavailable for ",crop_names[0])
            st.error("Yield data unavailable for ",crop_names[0])
            crop_yield = None
            std_dev = None

        crop_yield = []

        for i in range(len(production)):
            crop_yield.append(production[i] / area[i])

        crop_yield = np.array(crop_yield)

        return Distribution.Distribution(np.mean(crop_yield),np.max(crop_yield),np.min(crop_yield),np.std(crop_yield),self.unit)


# m = Yield_last_year()
# crop = Crop.Crop(['Rice','Paddy'], 3,['January','February','June','July'],[],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":105,"max":150})
# crop_list = [crop]
# start_time = "January"
# state = "Uttar Pradesh"
# district = "AGRA"
# market = "Agra"
# year = 2013
# season = "Kharif"

# dp = Direct_Parameters.Direct_Parameters(crop_list, start_time, state, district, market, year, season)


# d = m.get_prediction(crop, dp)
# d.show()





class Cost_production_last_year(Model):

    def __init__(self):
        self.type = "Production Cost"
        self.unit = "Tonne"

    def get_prediction(self, crop, direct, derived):
        year = direct.time["Year"]

        if year == 2009:
            cost_of_production = {'Onion':5239.4,'Potato':1473.0,'Maize':6059.6,'Rice':3973.6,'Wheat':4069.3,'Barley':3550.6, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':10807, 'Gram Raw':0, 'Groundnut' : 13547.0} # Per Tonne Note: Cost multiply by 10
        elif year == 2010:# 2010-11
            cost_of_production = {'Onion':5239.4,'Potato':1473.0,'Maize':3794.6,'Rice':3900.6,'Wheat':3974.3,'Barley':3840.6, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':8780, 'Gram Raw':0, 'Groundnut' : 14136.0} # Per Tonne Note: Cost multiply by 10
        elif year == 2011:
            cost_of_production = {'Onion':3097.3,'Potato':2669.1,'Maize':5330.5,'Rice':4795.5,'Wheat':4488.7,'Barley':3878.4, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':8083, 'Gram Raw':0, 'Groundnut' : 16000.0}
        elif year == 2012:
            cost_of_production = {'Onion':3231.9,'Potato':3089.7,'Maize':6089.3,'Rice':4861.8,'Wheat':5206.9,'Barley':5575.6, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0} # Per Tonne Note: Cost multiply by 10
        elif year == 2013:
            cost_of_production = {'Onion':9038.2,'Potato':4652.6,'Maize':6047.0,'Rice':5091.4,'Wheat':5201.6,'Barley':5295.9, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0}
        elif year == 2014:
            cost_of_production = {'Onion':9038.2,'Potato':5124.3,'Maize':6868.6,'Rice':7350.2,'Wheat':7109.3,'Barley':7345.3, 'Jowar' : 9381.6, 'Bajra':4353.8, 'Masur Dal':11458.5, 'Gram Raw':28878.1, 'Groundnut' : 18432.0 }
        elif year == 2015:
            cost_of_production = {'Onion':9038.2,'Potato':3312.6,'Maize':5822.6,'Rice':7723.5,'Wheat':6808.7,'Barley':5691.3, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0}
        return Distribution.Distribution(cost_of_production[crop.names[0]],cost_of_production[crop.names[0]],cost_of_production[crop.names[0]],0, self.unit)

class Cost_cultivation_last_year(Model):

    def __init__(self):
        self.type = "Cultivation Cost"
        self.unit = "Hectare"

    def get_prediction(self, crop, direct, derived):
        year = direct.time["Year"]

        if year == 2009:
            cost_of_cultivation = {'Onion':29980.48,'Potato':37156.91,'Maize':11642.64,'Rice':15690.64,'Wheat':16331.69,'Barley':11814.24, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':6227, 'Gram Raw':0, 'Groundnut' : 19025} # Per Hectare
        elif year == 2010: # Cost of cultivation for the year 2010 - 2011
            cost_of_cultivation = {'Onion':29980.48,'Potato':37156.91,'Maize':8274.64,'Rice':15490.64,'Wheat':17806.69,'Barley':15879.24, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':7728, 'Gram Raw':0, 'Groundnut' : 29003.55} # Per Hectare
        elif year == 2011:
            cost_of_cultivation = {'Onion':45933.17,'Potato':39326.56,'Maize':10134.22,'Rice':19867.22,'Wheat':20430.17,'Barley':16721.64, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':8135, 'Gram Raw':0, 'Groundnut' : 25000.55}
        elif year == 2012:
            cost_of_cultivation = {'Onion':40430.20,'Potato':47566.33,'Maize':12181.20,'Rice':21001.71,'Wheat':21846.68,'Barley':20253.06, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0} # Per Hectare
        elif year == 2013:
            cost_of_cultivation = {'Onion':40991.55,'Potato':68600.35,'Maize':13375.28,'Rice':22884.43,'Wheat':22375.77,'Barley':19109.28, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0}
        elif year == 2014:
            cost_of_cultivation = {'Onion':40991.55,'Potato':96760.77,'Maize':11152.48,'Rice':29137.86,'Wheat':24254.03,'Barley':20595.45, 'Jowar' : 17960.77, 'Bajra':14473.21, 'Masur Dal':11044.66, 'Gram Raw':16102.38, 'Groundnut' : 26912.55}
        elif year == 2015:
            cost_of_cultivation = {'Onion':40991.55,'Potato':61690.11,'Maize':16445.42,'Rice':29679.37,'Wheat':26916.80,'Barley':16295.13, 'Jowar' : 0, 'Bajra':0, 'Masur Dal':0, 'Gram Raw':0}
        return Distribution.Distribution(cost_of_cultivation[crop.names[0]],cost_of_cultivation[crop.names[0]],cost_of_cultivation[crop.names[0]],0, self.unit)


class Price_last_year(Model):

    def __init__(self):
        self.type = "Price"
        self.unit = "Quintal"
        self.range = 7

    def str_compare(self, str1, str2):
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        if str1 == str2:
            return True
        else:
            return False


    def get_prediction(self, crop, direct, derived): # add the derived class parameter here

        commodity = crop.names[0]
        #print("Commodity = ",commodity)
        ccode = str(crop.commodity_code)
        #print("Commodity Code = ",ccode)
        #file name to save the commodity-price data
        file_name = "price_"+commodity+".csv"
        #Fixing the From data in the same format

        """
        month_details = {"January" : [0,"Jan"], "February" : [1,"Feb"], "March" : [2,"Mar"], "April" : [3,"Apr"],
        "May":[4,"May"], "June" : [5,"Jun"], "July" : [6,"Jul"], "August" : [7,"Aug"], "September" : [8,"Sep"],
        "October":[9,"Oct"],"November" : [10,"Nov"], "December" : [11,"Dec"]}

        month_dict = {0:"January", 1:"February", 2:"March", 3:"April", 4:"May", 5:"June", 6:"July",
        7:"August",8:"September",9:"October",10:"November",11:"December"}

        """

        year = direct.time["Year"]
        #print("year = ",year)
        predicted_year = year - 1
        #print("pred_year = ",predicted_year)

        """
        month = direct.time["Month"]
        #print("month = ",month)
        month_no = month_details[month][0]
        #print("month_no = ",month_no)

        

        cycle_time = (crop.cycle_time["min"]+crop.cycle_time["max"])/2
        #print("cycle_time = ", cycle_time)

        sell_month_no = month_no + math.ceil(cycle_time/30)
        #print("sell_month_no = ", sell_month_no)

        if(sell_month_no > 11):
            predicted_year += 1
        #print("predicted_year", predicted_year)

        sell_month_no = sell_month_no % 12
        #print("sell_month_no = ", sell_month_no)
        sell_month = month_details[month_dict[sell_month_no]][1]
        #print("sell_month = ", sell_month)

        """

        fromDate = "1-"+str((crop.harvest_period[0])[0:3])+"-"+str(predicted_year)
        toDate = "28-"+str((crop.harvest_period[-1])[0:3])+"-"+str(predicted_year)

        #print("fromDate = ", fromDate)
        #print("toDate = ", toDate)

        """

        main_url = "https://www.agmarknet.gov.in/" #website url
        PATH = "chromedriver" #path for chrome web driver

        csv_file = open(file_name,"w")
        headers = "State,State_Code,District,District_Code,Market,Market_Code,Commodity,Commodity_Code,Variety,Grade,Min_Price,Max_Price,Modal_Price,Date\n"
        csv_file.write(headers) #writing the headers in csv file
        """

        market_data = pd.read_csv("../data/market.csv")

        i = 0

        state = direct.location["State"]
        district = direct.location["District"]
        market = direct.location["Market"]

        #print("state = ", state)
        #print("district = ", district)
        #print("market = ", market)



        
        while True:
            if self.str_compare(market_data.iloc[i]["state"], state) and self.str_compare(market_data.iloc[i]["district"], district) and self.str_compare(market_data.iloc[i]["market"], market):
                scode = market_data.iloc[i]["state code"]
                dcode = market_data.iloc[i]["district code"]
                mcode = market_data.iloc[i]["market code"]

                # print("found it")
                # print("scode = ", scode)
                # print("dcode = ",dcode)
                # print("mcode = ",mcode)
                break
            i += 1

        return Modifiedprice.fun1(state,scode,district,dcode,market,mcode,commodity,ccode,fromDate,toDate)


class Price_Current_year(Model):

    def __init__(self):
        self.type = "Price"
        self.unit = "Quintal"
        self.range = 7

    def str_compare(self, str1, str2):
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        if str1 == str2:
            return True
        else:
            return False


    def get_prediction(self, crop, direct, weather): # add the derived class parameter here

        commodity = crop.names[0]
        #print("Commodity = ",commodity)
        ccode = str(crop.commodity_code)
        #print("Commodity Code = ",ccode)
        #file name to save the commodity-price data
        file_name = "price_"+commodity+".csv"
        #Fixing the From data in the same format

        """
        month_details = {"January" : [0,"Jan"], "February" : [1,"Feb"], "March" : [2,"Mar"], "April" : [3,"Apr"],
        "May":[4,"May"], "June" : [5,"Jun"], "July" : [6,"Jul"], "August" : [7,"Aug"], "September" : [8,"Sep"],
        "October":[9,"Oct"],"November" : [10,"Nov"], "December" : [11,"Dec"]}

        month_dict = {0:"January", 1:"February", 2:"March", 3:"April", 4:"May", 5:"June", 6:"July",
        7:"August",8:"September",9:"October",10:"November",11:"December"}

        """

        year = direct.time["Year"]



        if commodity == 'Masur Dal': # Change this condition if data is available
            year = 2013
        if commodity == 'Maize': # Change this condition if data is available
            year = 2012
        if commodity == 'Groundnut':
            year = 2017
        #print("year = ",year)
        predicted_year = year
        #print("Price of Year = ", predicted_year)
        #print("pred_year = ",predicted_year)

        """
        month = direct.time["Month"]
        #print("month = ",month)
        month_no = month_details[month][0]
        #print("month_no = ",month_no)

        

        cycle_time = (crop.cycle_time["min"]+crop.cycle_time["max"])/2
        #print("cycle_time = ", cycle_time)

        sell_month_no = month_no + math.ceil(cycle_time/30)
        #print("sell_month_no = ", sell_month_no)

        if(sell_month_no > 11):
            predicted_year += 1
        #print("predicted_year", predicted_year)

        sell_month_no = sell_month_no % 12
        #print("sell_month_no = ", sell_month_no)
        sell_month = month_details[month_dict[sell_month_no]][1]
        #print("sell_month = ", sell_month)

        """

        fromDate = "1-"+str((crop.harvest_period[0])[0:3])+"-"+str(predicted_year)
        toDate = "28-"+str((crop.harvest_period[-1])[0:3])+"-"+str(predicted_year)

        #print("fromDate = ", fromDate)
        #print("toDate = ", toDate)

        """

        main_url = "https://www.agmarknet.gov.in/" #website url
        PATH = "chromedriver" #path for chrome web driver

        csv_file = open(file_name,"w")
        headers = "State,State_Code,District,District_Code,Market,Market_Code,Commodity,Commodity_Code,Variety,Grade,Min_Price,Max_Price,Modal_Price,Date\n"
        csv_file.write(headers) #writing the headers in csv file
        """

        market_data = pd.read_csv("/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/data/market.csv")

        # i = 0

        state = direct.location["State"]
        district = direct.location["District"]
        market = direct.location["Market"]

        #print("state = ", state)
        #print("district = ", district)
        #print("market = ", market)


        flag = 0
        
        # while True:
        for i in range(len(market_data)):
            if self.str_compare(market_data.iloc[i]["state"], state) and self.str_compare(market_data.iloc[i]["district"], district) and self.str_compare(market_data.iloc[i]["market"], market):
                scode = market_data.iloc[i]["state code"]
                dcode = market_data.iloc[i]["district code"]
                mcode = market_data.iloc[i]["market code"]
                flag = 1
                # print("found it")
                # print("scode = ", scode)
                # print("dcode = ",dcode)
                # print("mcode = ",mcode)
                break
            # i += 1
        if flag == 0:
            print("Price Data not available")
            st.error("Price Data not available")
            return Distribution.Distribution(None,None,None,None,None)
        return Modifiedprice.fun1(state,scode,district,dcode,market,mcode,commodity,ccode,fromDate,toDate)

        """

        def CreateSubUrl(State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode,FromDate,ToDate):
            url = "SearchCmmMkt.aspx?"
            url = url+"Tx_Commodity="+str(Ccode)
            url = url+"&Tx_State="+str(Scode)
            url = url+"&Tx_District="+str(Dcode)
            url = url+"&Tx_Market="+str(Mcode)
            url = url+"&DateFrom="+FromDate
            url = url+"&DateTo="+ToDate
            url = url+"&Fr_Date="+FromDate
            url = url+"&To_Date="+ToDate
            url = url+"&Tx_Trend=0"
            url = url+"&Tx_CommodityHead="+Commodity
            url = url+"&Tx_StateHead="+urllib.parse.quote_plus(State, safe='') #url encoding for state, district, market
            url = url+"&Tx_DistrictHead="+urllib.parse.quote_plus(District, safe='')
            url = url+"&Tx_MarketHead="+urllib.parse.quote_plus(Market, safe='')
            return url

        def GetDatafromMarket(driver,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode):
            print(State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode)
            IsFirstPage = True
            while True:
                page_source = driver.page_source
                page_soup = soup(page_source,"html.parser")
                SaveDatatoCSV(page_soup,IsFirstPage,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode)#Saving all data in the present page
                IsFirstPage = False
                present,pos=IsThereNextPage(page_soup) #Checking for the next page
                print("Is there another page? ",present," Position:",pos)
                if(not present):
                    break
                next_button = driver.find_element_by_xpath("//*[@id='cphBody_GridPriceData']/tbody/tr[52]/td/table/tbody/tr/td["+str(pos)+"]/input")
                actions = ActionChains(driver)
                actions.click(next_button)  #Clicking the next page button
                actions.perform()
                time.sleep(10)
                print("check")
            driver.quit()

        def IsThereNextPage(page_soup):
            #page_soup = soup(page_source,"html.parser")
            container = page_soup.find('td',{"colspan":"10"})  #Next page button element presence
            if container:
                buttons = container.findAll('td')
                i=1
                for button in buttons:
                    input_td = button.input
                    source_image = input_td["src"]
                    if(source_image) == "../images/Next.png":
                        return True,i
                    i+=1
                return False,0
            return False,0

        def SaveDatatoCSV(page_soup,IsFirstPage,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode):
            #page_soup = soup(page_source,"html.parser")try:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "cphBody_GridPriceData"))
                )
                container = page_soup.find(id="cphBody_GridPriceData")
                if(container):
                    price_container = container.findAll('tr') #finding the each row in commodity price table
                    price_container.pop(0)
                    if(IsFirstPage):
                        #print(price_container,len(price_container))
                        if(len(price_container) > 50):
                            price_container.pop(-1)
                            price_container.pop(-1)
                        elif(page_soup.find('td',{"colspan":"12"})):
                            price_container.pop(-1)
                else:
                    if len(price_container) > 0:
                        price_container.pop(-1)
                    if len(price_container) > 0:
                        price_container.pop(-1)
                for price_row in price_container:
                    details = price_row.findAll('td') #finding all columns in a row
                    data = State+","+Scode+","+District+","+Dcode+","+Market+","+Mcode+","+Commodity+","+Ccode
                    data = data+","+details[4].text.strip()+","+details[5].text.strip()
                    data = data+","+details[6].text.strip()+","+details[7].text.strip()
                    data = data+","+details[8].text.strip()+","+details[9].text.strip()
                    print(data)
                    csv_file.write(data+"\n") #writing the data to csv file
            finally:
                return
        """

        """



        sub_url = CreateSubUrl(state,scode,district.replace(":",","),dcode,market.replace(":",","),mcode,commodity,ccode,fromDate,toDate)
        url = main_url+sub_url
        print("URL = ", url)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(executable_path=PATH)
        driver.get(url)
        time.sleep(3)
        GetDatafromMarket(driver,state,scode,district,dcode,market,mcode,commodity,ccode)
        csv_file.close()

        p = pd.read_csv(file_name)
        print("price_"+commodity+"_Data")
        print(p.head())

        min_price = p.iloc[0]["Min_Price"]
        max_price = p.iloc[0]["Max_Price"]
        modal_price = p.iloc[0]["Modal_Price"]

        std_dev = (max_price-min_price)/4
        

        return Distribution.Distribution(modal_price, max_price, min_price, std_dev, self.unit)
        """

        


"""

p = Price_last_year()
onion = Crop.Crop(['Onion'], 23, ['December','January','July','August','October','November'],[],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"},{"min":80,"max":150})
crop_list = [onion]
start_time = "January"
state = "Uttar Pradesh"
district = "Agra"
market = "Agra"
year = 2015
season = "Kharif"

dp = Direct_Parameters.Direct_Parameters(crop_list, start_time, state, district, market, year, season)


d = p.get_prediction(onion, dp)
d.show()

"""






class CycleTime_last_year(Model):
    def __init__(self):
        self.type = "Cycle_Time"
        self.unit = "months"

    def get_prediction(self, crop, direct, weather):

        # cycletime_min={'Onion':80,'Potato':100,'Maize':100,'Rice':105,'Wheat':100,'Barley':130, 'Jowar' : 90, 'Bajra':60, 'Masur Dal':120, 'Gram Raw':90}
        # cycletime_max={'Onion':150,'Potato':120,'Maize':120,'Rice':150,'Wheat':120,'Barley':150, 'Jowar' : 115, 'Bajra':90, 'Masur Dal':145, 'Gram Raw':120}

        cycletime_min = crop.cycle_time['min']
        cycletime_max = crop.cycle_time['max']
        mean = (cycletime_min+cycletime_max)/2
        std_dev = (cycletime_max-cycletime_min)/4

        return Distribution.Distribution(mean/30,cycletime_max/30,cycletime_min/30,std_dev/30, self.unit)


class Yield_Ensemble_Model(Model):
    def __init__(self, n=1):
        self.type = "Yield"
        self.unit = "Tonnes/Hectare"
        self.n = n

    def get_crop_names(self, name):
        name = name.lower()
        res = re.findall( r'\w+|[^\s\w]+', name)
        return res

    def str_compare(self, str1, str2):
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        if str1 == str2:
            return True
        else:
            return False

    def get_prediction(self, crop, direct, weather):

        # Preparing test data

        crop_name = crop.names[0]

        test_data = []

        test_data.append(direct.location['Latitude'])
        test_data.append(direct.location['Longitude'])
        test_data.append(direct.time['Year'])

        test_data.extend(weather.rain)
        test_data.extend(weather.humidity)
        test_data.extend(weather.sunlight)
        test_data.extend(weather.temperature)
        test_data.extend(direct.aesr)
        test_data.extend(crop.last_year_yields)

        test_data = np.array(test_data)
        test_data = test_data.reshape(1, 34)

        standard_scaler = load(open('/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/Models and results for yield separate/'+crop_name+'/'+crop_name+'_scaler.pkl', 'rb'))

        # Standardzing the test data
        test_data = standard_scaler.transform(test_data)

        

        filename = '/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/Models and results for yield separate/'+crop_name+'/'+crop_name + '_Random_Forest_Model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

        results = loaded_model.predict(test_data)

        print("Random Forest Done")
        
        if direct.time['Season'] == "Kharif":
          filename = '/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/Models and results for yield separate/'+crop_name+'/'+crop_name + '_DL_Model.sav'
          loaded_model = pickle.load(open(filename, 'rb'))

          dl_model_result = loaded_model.predict(test_data)
          dl_model_result = dl_model_result.flatten()
          results = (results + dl_model_result)/2

        std_dev = np.std(crop.last_year_yields)
        
        

        return Distribution.Distribution(np.mean(results), np.mean(results) + std_dev, np.mean(results) - std_dev, 0, self.unit)


class Yield_Ensemble_Model_older(Model):
    def __init__(self, n=1):
        self.type = "Yield"
        self.unit = "Tonnes/Hectare"
        self.n = n

    def get_crop_names(self, name):
        name = name.lower()
        res = re.findall( r'\w+|[^\s\w]+', name)
        return res

    def str_compare(self, str1, str2):
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        if str1 == str2:
            return True
        else:
            return False




    def get_prediction(self, crop, direct, derived):
        Linear_Regression_model = pickle.load(open('../Models for yield prediction/Linear_Regression_model.sav', 'rb'))
        Polynomial_Regression_model = pickle.load(open('../Models for yield prediction/Polynomial_Regression_model.sav', 'rb'))
        Ridge_Regression_model = pickle.load(open('../Models for yield prediction/Ridge_Regression_model.sav', 'rb'))
        # RANSAC_Regression_model = pickle.load(open('../Models for yield prediction/RANSAC_Regression_model.sav', 'rb'))
        KNN_Regression_model = pickle.load(open('../Models for yield prediction/KNN_Regression_model.sav', 'rb'))
        Bayesian_Ridge_Regression_model = pickle.load(open('../Models for yield prediction/Bayesian_Ridge_Regression_model.sav', 'rb'))
        # SVM_Regression_model = pickle.load(open('../Models for yield prediction/SVM_Regression_model.sav', 'rb'))
        Decision_Tree_Regression_model = pickle.load(open('../Models for yield prediction/Decision_Tree_Regression_model.sav', 'rb'))
        Random_Forest_Regression_model = pickle.load(open('../Models for yield prediction/Random_Forest_Regression_model.sav', 'rb'))
        #Deep_Learning_model = pickle.load(open('../Models for yield prediction/Deep_Learning_model.sav', 'rb'))

        ML_Models = [Linear_Regression_model, Polynomial_Regression_model, Ridge_Regression_model, KNN_Regression_model, Bayesian_Ridge_Regression_model, Decision_Tree_Regression_model, Random_Forest_Regression_model]
        #DL_Models = [Deep_Learning_model]


        csv_file = open('example.csv',"w")
        headers = "Latitude,Longitude,Season_Kharif,Season_Rabi,Season_Summer,Season_Whole Year,Crop_Arhar/Tur,Crop_Bajra,Crop_Banana,Crop_Barley,Crop_Castor seed,Crop_Coriander,Crop_Cotton(lint),Crop_Dry chillies,Crop_Dry ginger,Crop_Garlic,Crop_Ginger,Crop_Gram,Crop_Groundnut,Crop_Guar seed,Crop_Jowar,Crop_Jute,Crop_Linseed,Crop_Maize,Crop_Masoor,Crop_Moong(Green Gram),Crop_Moth,Crop_Oilseeds total,Crop_Onion,Crop_Other  Rabi pulses,Crop_Other Kharif pulses,Crop_Peas & beans (Pulses),Crop_Potato,Crop_Ragi,Crop_Rapeseed &Mustard,Crop_Rice,Crop_Sannhamp,Crop_Sesamum,Crop_Small millets,Crop_Soyabean,Crop_Sugarcane,Crop_Sunflower,Crop_Sweet potato,Crop_Tobacco,Crop_Total foodgrain,Crop_Turmeric,Crop_Urad,Crop_Wheat,Crop_Year\n"
        csv_file.write(headers)
        csv_file.close()



        example = pd.read_csv("example.csv")

        example.loc[len(example)] = 0


        def findGeocode(city):  
            try:
                geolocator = Nominatim(user_agent="your_app_name")                 
                return geolocator.geocode(city)             
            except GeocoderTimedOut:                  
                return findGeocode(city)
        if findGeocode("Agra") != None:           
          loc = findGeocode("Agra")
          example.loc[0, "Latitude"] = loc.latitude
          example.loc[0, "Longitude"] = loc.longitude
         
        else:
          example.loc[0, "Latitude"] = 26.8467
          example.loc[0, "Longitude"] = 80.9462

        season = "Season_"+str(direct.time['Season'])
        crop_name = "Crop_"+str(crop.names[0])

        example.loc[0, season] = 1
        example.loc[0, crop_name] = 1
        example.loc[0, "Crop_Year"] = direct.time['Year']

        data_point = list(example.iloc[0])
        data_point = np.array(data_point).reshape((1,49))

        results = []
        for model in ML_Models:
          pred = model.predict(example)
          pred = pred.flatten()
          results.append(pred[0])

        # for model in DL_Models:
        #   pred = model.predict(data_point)
        #   pred = pred.flatten()
        #   results.append(pred[0])

        results = np.array(results)
        return Distribution.Distribution(np.mean(results), np.max(results), np.min(results), np.std(results), self.unit)



        
class Cost_PPF(Model):
    def __init__(self):
        pass

class Price_PPF(Model):
    def __init__(self):
        pass
