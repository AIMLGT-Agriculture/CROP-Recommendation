import streamlit as st
import pandas as pd
header = st.container()
dataset = st.container()
feature = st.container()
model_training = st.container()

with header:
	st.title('Agriculture Crop Recommendation Engine (ACRE)')
	st.write("A crop recommendation system for farmers based on environmental conditions, soil characteristics, and geographical locations, ranking the portfolio of crops by calculating the farmer utilities such as profit maximization and minimizing risk.")


import Crop
import Utility
import Utility_Calculator
import Model
import Direct_Parameters
import Portfolio



# RABI Crops
onion = Crop.Crop(['Onion'], 23, ['December','January','July','August','October','November'],['March','April','May'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"},{"min":80,"max":150})
potato = Crop.Crop(['Potato'], 24, ['February','March','April'],['September','October'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":100,"max":120})
wheat = Crop.Crop(['Wheat'], 1, ['February','March','April'],['April', 'May'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":100,"max":120})
barley = Crop.Crop(['Barley', 'Jau'], 1, ['October', 'November'],['October', 'November','December'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":130,"max":150})

# KHARIF Crops
maize = Crop.Crop(['Maize','Makka'], 4, ['February','June','July','October','November'],['January','February','December'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":100,"max":120})
rice = Crop.Crop(['Rice','Paddy'], 3,['January','February','June','July'],['November','December'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":105,"max":150})


# green_chilli = Crop.Crop('Green Chilli',['January','February','May','June','September','October'],[],{"Yield":"../data/Uttar Pradesh Yield Data.csv"})
# groundnut = Crop.Crop(['Groundnut'], 10, ['February','March','June','July','November'],[],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":120,"max":130})


print("*******************************************************************")

# crop_list = [groundnut, maize, rice]
# crop_list = [ rice, maize]
# start_time = "January"

cols = st.columns(3)
state = cols[0].text_input("Enter State : ","Uttar Pradesh")
# state = "Uttar Pradesh"
district = cols[1].text_input("Enter District : ","Agra")
# district = "Agra"
# market = "Agra"
market = cols[2].text_input("Enter Market : ","Agra")
#year = 2013
year = cols[0].slider("Choose Year : ", 2010,2015, 2013, 1)
# season = "Kharif"
season = cols[1].radio("Choose Season : ", ["Kharif","Rabi","Whole Year", "Summer"])

crop_list = []
if season == "Kharif":
	st.write("KHARIF CROPS")
	crop_list = [rice, maize]
	check = cols[2].checkbox("Rice")
	check = cols[2].checkbox("Maize")

elif season == "Rabi":
	st.write("RABI CROPS")
	crop_list = [onion, wheat]
	check = cols[2].checkbox("Onion")
	check = cols[2].checkbox("Wheat")

start = st.button("Get Recommendation")
if start:
	direct_parameter = Direct_Parameters.Direct_Parameters(crop_list, state, district, market, year, season)
	utility = Utility.Profit_Maximization(Model.Yield_Ensemble_Model(), Model.Price_Current_year(), Model.Cost_cultivation_last_year(), Model.Cost_production_last_year(), Model.CycleTime_last_year())
	calculator = Utility_Calculator.Utility_Calculator(direct_parameter)
	crop_utility_distribution = []

	profit_data = []

	for crop in crop_list:
		temp = []
		print(crop.names[0])
		try:
			utility_distribution = calculator.get_utility_distribution(crop, utility)
		except:
			st.error("Error in getting utility distribution for ",crop.names[0])
			continue
		temp.append(crop.names[0])
		temp.append(utility_distribution.mean)
		temp.append(utility_distribution.maximum)
		temp.append(utility_distribution.minimum)
		variance = (utility_distribution.maximum-utility_distribution.mean + utility_distribution.mean-utility_distribution.minimum)/2
		temp.append(variance)
		crop_utility_distribution.append(utility_distribution)
		st.success("Profit Distribution Calculated for "+crop.names[0])
		utility_distribution.short_show("Profit utility for "+crop.names[0])
		print("******************")
		print(" ")
		profit_data.append(temp)
	profit_output = pd.DataFrame(profit_data, columns = ["Crop", "Average Profit", "Maximum Profit", "Minimum Profit", "Variance in Profit"])
	st.write("*********************************************************************")
	st.dataframe(profit_output)



	ratios = [(0,1), (0.25, 0.75), (0.5,0.5), (0.75, 0.25), (1,0)]
	pf = Portfolio.Portfolio()
	data = []
	for ratio in ratios:
		try:
			temp = []
			temp.append(ratio[0])
			temp.append(ratio[1])
			temp.append(pf.sharpeRatio(crop_utility_distribution, ratio))
			temp.append(pf.logUtility(crop_utility_distribution, ratio))
			data.append(temp)
		except:
			continue
	output = pd.DataFrame(data, columns = [crop_list[0].names[0], crop_list[1].names[0], "Sharpe Ratio on profit maximization", "Log Utilities"])	
	print("*********************************************************************")
	st.write("*********************************************************************")
	st.write("Portfolios with different utility scores")
	st.dataframe(output)

	st.write("*********************************************************************")
	print("*******************************************************************")
st.write("By : Rohit Patel, MTech CSA, IISc Bangalore")
st.write("Advisor : Prof. Yadati Narahari")
st.write("Mentors : Inavamsi Enaganti, Mayank Ratan Bharadwaj")
