#Pass as arguments: Index of required state in state.csv, start year - from which year we want to collect data, end year - till which year we want to collect data,
#Commodity, commodity code taken from website
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from datetime import date
import urllib.parse
import csv
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
      
            
def IsDataPresent(page_soup):
      container = page_soup.find('td',{"colspan":"3"})  #plus button element presence
      if container:
            return False
      return True
def IsDitrictIdPresent(page_source,district_id):
      page_soup = soup(page_source,"html.parser")
      container = page_soup.find('input',{"id":district_id})
      if container:
            return True
      return False
      
def GetArrivalData(page_source,State,Scode,Commodity,Ccode,date,i):
	page_soup = soup(page_source,"html.parser")
	district_id = "cphBody_GridArrivalData_gvOrders_0_Lab2DistrictName_"+str(i)
	try:
		element = WebDriverWait(driver, 10).until(
		  EC.presence_of_element_located((By.ID, district_id))
		)
		district_span = page_soup.find("span", {"id":district_id})
		if(district_span):
			district = district_span.text
			table_id = "cphBody_GridArrivalData_gvOrders_0_gvProducts_"+str(i)
			try:
				element = WebDriverWait(driver, 10).until(
				  EC.presence_of_element_located((By.ID, table_id))
				)
				market_table = page_soup.find("table", {"id":table_id})
				if(market_table):
					rows = market_table.findAll('tr')
					rows.pop(0)
					for row in rows:
						cols = row.findAll('td')
						market = cols[0].text.replace('\n', '').strip()
						vol = cols[1].text.replace('\n', '').strip()
						data = State+","+Scode+","+district.replace(",",":")+","
						data = data + market.replace(",",":")+","+Commodity+","+Ccode+","+vol+","+date
						print(data)
						csv_file.write(data+"\n") #writing the data to csv file
			finally:
				return
	finally:
		return
            
def GetDatafromAgmarknet(driver,State,Scode,Commodity,Ccode,date):
      print(State,Scode,Commodity,Ccode,date)
      page_source = driver.page_source
      page_soup = soup(page_source,"html.parser")
      if(IsDataPresent(page_soup)):
            element = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.ID, "cphBody_GridArrivalData_imgOrdersShow_0"))
            )
            state_plus = driver.find_element_by_id('cphBody_GridArrivalData_imgOrdersShow_0')
            actions = ActionChains(driver)
            actions.click(state_plus)
            actions.perform()
            time.sleep(2)
            i = 0
            while True:
                  district_id =  "cphBody_GridArrivalData_gvOrders_0_imgProductsShow_"+str(i)
                  if(IsDitrictIdPresent(driver.page_source,district_id)):
                        district_plus = driver.find_element_by_id(district_id)
                        actions = ActionChains(driver)
                        actions.click(district_plus)
                        actions.perform()
                        time.sleep(2)
                        GetArrivalData(driver.page_source,State,Scode,Commodity,Ccode,date,i)
                        i += 1  
                  else:
                        break 
            
            driver.quit()    
      else:
            print("No data available")
            driver.quit()
      
def CreateSubUrl(State,Scode,Commodity,Ccode,FromDate,ToDate):
      url = "SearchCmmMkt.aspx?"
      url = url+"Tx_Commodity="+str(Ccode)
      url = url+"&Tx_State="+str(Scode)
      url = url+"&Tx_District=0"
      url = url+"&Tx_Market=0"
      url = url+"&DateFrom="+FromDate
      url = url+"&DateTo="+ToDate 
      url = url+"&Fr_Date="+FromDate
      url = url+"&To_Date="+ToDate
      url = url+"&Tx_Trend=1"
      url = url+"&Tx_CommodityHead="+Commodity
      url = url+"&Tx_StateHead="+urllib.parse.quote_plus(State, safe='') #url encoding for state, district, market
      url = url+"&Tx_DistrictHead=--Select--"#+urllib.parse.quote_plus(District, safe='')
      url = url+"&Tx_MarketHead=--Select--"#+urllib.parse.quote_plus(Market, safe='')
      return url
      
              
if __name__=='__main__':
      
      args = sys.argv
      s = int(args[1])  #Index of required state in state.csv
      s_year = int(args[2]) #start year - from which year we want to collect data
      e_year = int(args[3]) #end year - till which year we want to collect data
      Commodity = args[4]#"Tomato" #commodity and it's code taken from website
      Ccode = args[5]#"78"
      main_url = "https://www.agmarknet.gov.in/" #website url
      PATH = "/home/bhardwaj/Softwares/chromedriver" #path for chrome web driver
      s_date = date(s_year, 1, 1)
      e_date = date(e_year, 12, 31)
      
      
      file_name = "quantity_"+Commodity+"_"+str(s_year)+"_"+str(s)+".csv" #file name to save the commodity-price data
      
      csv_file = open(file_name,"w")
      headers = "State,State_Code,District,Market,Commodity,Commodity_Code,Arrivals,Date\n"
      csv_file.write(headers) #writing the headers in csv file
      stateFile = open('state.csv') #opening and reading the market csv file
      stateReader = csv.reader(stateFile)
      stateDataSet = list(stateReader)
      
      #stateDataSet.pop(0) #To remove headers in the csv file
      #print(stateDataSet)
      
      
      stateData = stateDataSet[s]
      Scode = stateData[0]
      State = stateData[1] 
      print(Scode,State)
      
      delta = e_date - s_date
      d_size = delta.days
      date_list = []
      for i in range(d_size + 1):
          day = s_date + timedelta(days=i)
          date_list.append(day.strftime("%d-%b-%Y"))  
      for query_date in date_list:
            sub_url = CreateSubUrl(State,Scode,Commodity,Ccode,query_date,query_date)
            url = main_url+sub_url
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')  # Last I checked this was necessary.
            driver = webdriver.Chrome(executable_path=PATH,options=options)
            #driver = webdriver.Chrome(executable_path=PATH)
            #driver.minimize_window()
            #print(url)
            driver.get(url)
            time.sleep(3)
            GetDatafromAgmarknet(driver,State,Scode,Commodity,Ccode,query_date)
      stateFile.close()
      csv_file.close()
      


