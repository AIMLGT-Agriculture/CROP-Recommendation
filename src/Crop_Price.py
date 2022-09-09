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



            
 
def CreateSubUrl(State,Scode,District,Dcode,Market,Mcode,Commodity,Ccode,FromDate,ToDate):
      import urllib
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
      
      
