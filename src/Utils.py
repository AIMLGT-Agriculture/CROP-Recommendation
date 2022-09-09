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
