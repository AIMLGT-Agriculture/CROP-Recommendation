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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from datetime import date
import urllib.parse
import csv
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.action_chains import ActionChains
#from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fun1(state,scode,district,dcode,market,mcode,commodity,ccode,fromDate,toDate):

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
                              if(len(price_container) > 50): #Next page symbol presence conditon
      	                        price_container.pop(-1)
      	                        price_container.pop(-1)
                              elif(page_soup.find('td',{"colspan":"12"})): #No Data condition
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
                        #print(data)
                        csv_file.write(data+"\n") #writing the data to csv file

            finally:
                  return
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
      def GetDatafromMarket(driver,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode):
            #print(State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode)
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
      """

      main_url = "https://www.agmarknet.gov.in/" #website url
      PATH = "chromedriver" #path for chrome web driver

      csv_file = open(file_name,"w")
      headers = "State,State_Code,District,District_Code,Market,Market_Code,Commodity,Commodity_Code,Variety,Grade,Min_Price,Max_Price,Modal_Price,Date\n"
      csv_file.write(headers) #writing the headers in csv file

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
      """

      Commodity = str(commodity)
      Ccode = str(ccode)
      #file name to save the commodity-price data
      file_name = "price_"+Commodity+".csv"
      #Fixing the From data in the same format
      FromDate =str(fromDate)
      ToDate = str(toDate)

      main_url = "https://www.agmarknet.gov.in/" #website url
      # PATH = "/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/src/chromedriver.exe" #path for chrome web driver
      # PATH = "/content/chromedriver.exe"
      print("In Modified_Price.py file")

      csv_file = open(file_name,"w")
      headers = "State,State_Code,District,District_Code,Market,Market_Code,Commodity,Commodity_Code,Variety,Grade,Min_Price,Max_Price,Modal_Price,Date\n"
      csv_file.write(headers) #writing the headers in csv file

      Scode = str(scode)
      State = str(state) 
      Dcode = str(dcode)
      District = str(district)
      Market = str(market)
      Mcode = str(mcode)

      sub_url = CreateSubUrl(State,Scode,District.replace(":",","),Dcode,Market.replace(":",","),Mcode,Commodity,Ccode,FromDate,ToDate)
      url = main_url+sub_url
                  

      options = Options()
      options.add_argument('--headless')
      options.add_argument('--disable-gpu')  # Last I checked this was necessary.
      # driver = webdriver.Chrome(executable_path=PATH)

      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-dev-shm-usage')
      driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
      
      driver.get(url)
      time.sleep(3)
      GetDatafromMarket(driver,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode)
      csv_file.close()
      
      p = pd.read_csv(file_name)
      if len(p) == 0:
            print("Price Data Not Found:")
            return Distribution.Distribution(None, None, None, None, "Rupees per Tonne")

      # print("DATA")
      # print(p.head())

      price = list(p["Modal_Price"])
      price = np.array(price)

      return Distribution.Distribution(np.mean(price), np.max(price), np.min(price), np.std(price), "Rupees per Tonne")
      

      """
      Commodity = "Onion"
      Ccode = "23"
      #file name to save the commodity-price data
      file_name = "price_"+Commodity+".csv"
      #Fixing the From data in the same format
      FromDate ="1-May-2014"
      ToDate = "30-May-2014"

      main_url = "https://www.agmarknet.gov.in/" #website url
      PATH = "chromedriver" #path for chrome web driver

      csv_file = open(file_name,"w")
      headers = "State,State_Code,District,District_Code,Market,Market_Code,Commodity,Commodity_Code,Variety,Grade,Min_Price,Max_Price,Modal_Price,Date\n"
      csv_file.write(headers) #writing the headers in csv file

      Scode = "UP"
      State = "Uttar Pradesh" 
      Dcode = "1"
      District = "Agra"
      Market = "Agra"
      Mcode = "314"

      sub_url = CreateSubUrl(State,Scode,District.replace(":",","),Dcode,Market.replace(":",","),Mcode,Commodity,Ccode,FromDate,ToDate)
      url = main_url+sub_url
                  

      options = Options()
      options.add_argument('--headless')
      options.add_argument('--disable-gpu')  # Last I checked this was necessary.
      driver = webdriver.Chrome(executable_path=PATH)
      driver.get(url)
      time.sleep(3)
      GetDatafromMarket(driver,State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode)
      csv_file.close()
      p = pd.read_csv("price_"+Commodity+".csv")
      print("DATA")
      print(p.head())
      """

      