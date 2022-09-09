import Crop
import Utility
import Utility_Calculator
import Model
import Direct_Parameters
import Portfolio
import Weather_Parameters
import pandas as pd
import numpy as np


# Mentioning folder path in google drive

folder_path = '/content/drive/MyDrive/1Crop-Recommendation-System-ACRE--main/src/'

# Whole Year Crop
# potato = Crop.Crop(['Potato'], 24, ['February','March','April'],['January','September','October', 'December'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":75,"max":120}, [],0.0)

# RABI Crops
#onion = Crop.Crop(['Onion'], 23, ['December','January','July','August','October','November'],['March','April','May'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"},{"min":80,"max":150})

wheat = Crop.Crop(['Wheat'], 1, ['February','March','April'],['April', 'May', 'June'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":100,"max":120}, [3.323586062, 3.218444909, 3.692355925], 3.891433566)
barley = Crop.Crop(['Barley', 'Jau'], 29, ['October', 'November'],['October','November','December'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":130,"max":150}, [3.052224371, 2.997775306, 3.299376299], 3.231009365)
masur = Crop.Crop(['Masur Dal'], 259, ['February','March','April'],['May', 'June', 'July'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":100,"max":120}, [0.88101983, 0.803455724, 0.880866426], 1.9283)
gram = Crop.Crop(['Gram Raw'], 359, ['October', 'November'],['January', 'February', 'March'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":130,"max":150}, [1.006393862, 0.82685069, 1.944634313], 1.561)

# KHARIF Crops
maize = Crop.Crop(['Maize','Makka'], 4, ['February','June','July','October','November'],['January','February'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":100,"max":120}, [2.634375, 2.412969283, 2.384879725], 2.735483871)
rice = Crop.Crop(['Rice','Paddy'], 3,['January','February','June','July'],['November','December'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":105,"max":150}, [2.672574627, 2.402309059, 2.454864154], 2.696326531)
jowar = Crop.Crop(['Jowar'], 5, ['February','June','July','October','November'],['January','February'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":100,"max":120}, [0.989010989, 0.954166667, 0.989583333], 0.7709)
bajra = Crop.Crop(['Bajra'], 28,['January','February','June','July'],['January', 'February', 'March'],{"Yield":"../data/Crop_Yield_Data_Final.csv"}, {"min":105,"max":150}, [1.57119939, 1.572847996, 1.771776702], 2.1107)


# green_chilli = Crop.Crop('Green Chilli',['January','February','May','June','September','October'],[],{"Yield":"../data/Uttar Pradesh Yield Data.csv"})
groundnut = Crop.Crop(['Groundnut'], 10, ['February','March','June','July','November'],['January','February','March'],{"Yield":"../data/Uttar_Pradesh_Yield_Data.csv"}, {"min":120,"max":130}, [0.333333333, 1, 1], 1)


print("*******************************************************************")
print("KHARIF CROPS")
# crop_list = [groundnut, maize, rice]
# crop_list = [barley]
crop_list = [ rice, maize, groundnut]
# start_time = "January"
state = "Uttar Pradesh"
district = "Agra"
latitude = 27.1752554
longitude = 78.0098161
year = 2010        # We need to set the year for recommendation 
AESR = [0,0,1,0]
# aesr = 4.1
market = "Agra"   
season = "Kharif"

# latitude = -0.04
# longitude = -1.31
# year = [1.76, 2014]         # We need to set the year for recommendation 
# AESR = [-0.3, -0.83, 0.89, -1.11]


#Creating Direct_Parameter Object
direct_parameter = Direct_Parameters.Direct_Parameters(crop_list, state, district, latitude, longitude, AESR, market, year, season)


# Kharif Season Weather Parameters

#For year 2011
# rain = [0.027457949, 0.002977096, 0.010711648, 0.009454854, 0.004308686, 5.67E-06]
# humidity = [350.261673, 59.916996, 80.3916, 82.906075, 75.55818, 51.48882]
# sunlight = [67350938, 15655537, 11419001, 11184673, 13548952, 15542775]
# temperature = [1517.921173, 306.49545, 303.28308, 302.6915, 302.66214, 302.789]

# # For year 2010
rain = [0.025110954, 0.00014846, 0.008011071, 0.0086559, 0.008169727, 0.000125796]
humidity = [344.8503723, 39.707195, 76.06058, 83.302055, 82.333145, 63.4474]
sunlight = [67565964, 18662864, 12475511, 11251721, 10277158, 14898710]
temperature = [1520.983521, 309.74747, 304.4506, 302.89493, 301.5351, 302.35544]

# # For year 2009
# rain = [0.019815195, 0.000776291, 0.004593134, 0.006355368, 0.004735928, 0.003354475]
# humidity = [308.5959854, 36.309196, 70.54657, 69.42545, 73.3605, 58.95427]
# sunlight = [75960815, 19382104, 14088720, 13654603, 14795430, 14039958]
# temperature = [1525.505035, 310.01453, 304.9616, 304.49646, 303.93826, 302.09418]

weather_parameter = Weather_Parameters.Weather_Parameters(rain, humidity, sunlight, temperature)

utility = Utility.Profit_Maximization(Model.Yield_Ensemble_Model(), Model.Price_Current_year(), Model.Cost_cultivation_last_year(), Model.Cost_production_last_year(), Model.CycleTime_last_year())
#utility_list=[utility1]

calculator = Utility_Calculator.Utility_Calculator(direct_parameter, weather_parameter)

kharif_crops = dict()
crop_utility_distribution = []
risk_factor = []

crop_names = []
profit = []
max_profit = []
min_profit = []
actual = []

for crop in crop_list:
	print(crop.names[0])
	utility_distribution, actual_profit = calculator.get_utility_distribution(crop, utility)
	crop_utility_distribution.append(utility_distribution)
	utility_distribution.short_show("Profit utility for "+crop.names[0])
	# variance = (utility_distribution.maximum-utility_distribution.mode + utility_distribution.mode-utility_distribution.minimum)/2
	risk_factor.append((utility_distribution.std_dev)/utility_distribution.mode)
	kharif_crops[crop.names[0]] = {"Maximum Profit":utility_distribution.maximum, "Minimum Profit":utility_distribution.minimum, "Average Profit":utility_distribution.mode, "Variance":(utility_distribution.std_dev)**2, "Risk Factor":risk_factor}
	
	crop_names.append(crop.names[0])
	profit.append(utility_distribution.mode)
	max_profit.append(utility_distribution.maximum)
	min_profit.append(utility_distribution.minimum)
	actual.append(actual_profit)

	print("******************")
	print(" ")

results = pd.DataFrame(list(zip(crop_names, profit, max_profit, min_profit, actual)), columns =['Crops', 'Profit', 'Maximum Profit', 'Minimum Profit', 'Actual Profit'])
results.to_csv(folder_path + season + "_Results_"+str(year)+".csv", index = False)

# ratios = [(0,1), (0.25, 0.75), (0.5,0.5), (0.75, 0.25), (1,0)]

# ratios = [(0.3, 0.3, 0.4), (0.3, 0.4, 0.3), (0.4, 0.3, 0.3)]

# ratios = [(0.2, 0.3, 0.2, 0.3), (0.4, 0.2, 0.2, 0.2), (0.1, 0.4, 0.3, 0.2), (0.3, 0.1, 0.4, 0.2)]

ratios = [(x/10.0, y/10.0, (10-x-y)/10.0) for x in range(0,11,2) for y in range(0,11-x,2)]
ratios.extend([(0.33, 0.33, 0.33), (0, 0.5, 0.5), (0.5, 0, 0.5), (0.5, 0.5 , 0)])

pf = Portfolio.Portfolio()

print("Sharpe Ratios")


crops = []
sharpe_ratios = []

for ratio in ratios:
	sr = pf.sharpeRatio(crop_utility_distribution, ratio)
	print(ratio, " ", crop_names," ","sharpe ratio on profit maximization = ", sr)
	crops.append(crop_names)
	sharpe_ratios.append(sr)

results = pd.DataFrame(list(zip(ratios, crops, sharpe_ratios)), columns =['Ratios', 'Crops', 'Sharpe Ratio'])
results.to_csv(folder_path + season + "_Sharpe_Ratio_"+str(year)+".csv", index = False)

print("********************")

print("Risk Ratios")

risk_ratios = []

for ratio in ratios:
	rf = pf.riskFactor(crop_utility_distribution, ratio)
	print(ratio, " ", crop_names, " ","Risk Factor = ", rf)
	risk_ratios.append(rf)

results = pd.DataFrame(list(zip(ratios, crops, risk_ratios)), columns =['Ratios', 'Crops', 'Risk Ratio'])
results.to_csv(folder_path + season + "_Risk_Ratio_"+str(year)+".csv", index = False)

print("*********************************************************************")


print("*******************************************************************")



print("RABI CROPS")

season = 'Rabi'
# crop_list = [groundnut, maize, rice]
crop_list = [barley, wheat, masur]
# start_time = "January"

direct_parameter = Direct_Parameters.Direct_Parameters(crop_list, state, district, latitude, longitude, AESR, market, year, season)


#Weather Parameters for Rabi Season

# For year 2011
# rain = [0.003508609, 0.000293519, 1.47E-05, 0.000532638, 0.000504307, 0]
# humidity = [321.3465118, 68.01477, 67.256226, 65.12289,	52.215195, 62.412903]
# sunlight = [68463660, 11644526, 12810072, 14847578,	18032684, 12960760]
# temperature = [1472.657013, 292.2687, 289.35544, 293.74738,	299.9843, 298.55063]

# # For year 2010
rain = [0.001937892, 0.000400044, 0.000278786, 0.000533771, 0, 0.00216341]
humidity = [310.8444023, 64.358154, 76.77458, 62.894264, 44.977432, 68.737434]
sunlight = [67736971, 11444737, 12043426, 14316953, 18183372, 11128800]
temperature = [1480.935272, 293.67038, 291.02106, 295.74106, 303.49493, 297.30118]

# # For year 2009
# rain = [0.000277657, 0, 0, 3.40E-05, 0.000198323, 0.000725292]
# humidity = [302.88274, 68.90697, 68.40209, 59.294563, 45.242245, 61.83997]
# sunlight = [70134435, 11450832, 12155849, 15293547, 18109552, 11748483]
# temperature = [1480.182587, 294.14398, 292.02435, 295.3658, 300.6035, 297.00784]

#Creting Weather Parameter Object
weather_parameter = Weather_Parameters.Weather_Parameters(rain, humidity, sunlight, temperature)

utility = Utility.Profit_Maximization(Model.Yield_Ensemble_Model(), Model.Price_Current_year(), Model.Cost_cultivation_last_year(), Model.Cost_production_last_year(), Model.CycleTime_last_year())
#utility_list=[utility1]

calculator = Utility_Calculator.Utility_Calculator(direct_parameter, weather_parameter)

rabi_crops = dict()
crop_utility_distribution = []
risk_factor = []

crop_names = []
profit = []
max_profit = []
min_profit = []
actual = []

for crop in crop_list:
	print(crop.names[0])
	utility_distribution, actual_profit = calculator.get_utility_distribution(crop, utility)
	crop_utility_distribution.append(utility_distribution)
	utility_distribution.short_show("Profit utility for "+crop.names[0])
	# variance = (utility_distribution.maximum-utility_distribution.mode + utility_distribution.mode-utility_distribution.minimum)/2
	risk_factor.append((utility_distribution.std_dev)/utility_distribution.mode)
	rabi_crops[crop.names[0]] = {"Maximum Profit":utility_distribution.maximum, "Minimum Profit":utility_distribution.minimum, "Average Profit":utility_distribution.mode, "Variance":(utility_distribution.std_dev)**2, "Risk Factor":risk_factor}
	
	crop_names.append(crop.names[0])
	profit.append(utility_distribution.mode)
	max_profit.append(utility_distribution.maximum)
	min_profit.append(utility_distribution.minimum)
	actual.append(actual_profit)

	print("******************")
	print(" ")

results = pd.DataFrame(list(zip(crop_names, profit, max_profit, min_profit, actual)), columns =['Crops', 'Profit', 'Maximum Profit', 'Minimum Profit', 'Actual Profit'])
results.to_csv(folder_path + season + "_Results_"+str(year)+".csv", index = False)


# ratios = [(0,1), (0.25, 0.75), (0.5,0.5), (0.75, 0.25), (1,0)]
# ratios = [(0.3, 0.3, 0.4), (0.3, 0.4, 0.3), (0.4, 0.3, 0.3)]

ratios = [(x/10.0, y/10.0, (10-x-y)/10.0) for x in range(0,11,2) for y in range(0,11-x,2)]
ratios.extend([(0.33, 0.33, 0.33), (0, 0.5, 0.5), (0.5, 0, 0.5), (0.5, 0.5 , 0)])

pf = Portfolio.Portfolio()

crops = []
sharpe_ratios = []

print("Sharpe Ratios")
for ratio in ratios:
	sr = pf.sharpeRatio(crop_utility_distribution, ratio)
	print(ratio, " ",crop_names," sharpe ratio on profit maximization = ", sr)
	crops.append(crop_names)
	sharpe_ratios.append(sr)

results = pd.DataFrame(list(zip(ratios, crops, sharpe_ratios)), columns =['Ratios', 'Crops', 'Sharpe Ratio'])
results.to_csv(folder_path + season + "_Sharpe_Ratio_"+str(year)+".csv", index = False)

print("Risk Ratios")

risk_ratios = []
for ratio in ratios:
	rf = pf.riskFactor(crop_utility_distribution, ratio)
	print(ratio, " ",crop_names," Risk Factor = ",rf)
	risk_ratios.append(rf)

results = pd.DataFrame(list(zip(ratios, crops, risk_ratios)), columns =['Ratios', 'Crops', 'Risk Ratio'])
results.to_csv(folder_path + season + "_Risk_Ratio_"+str(year)+".csv", index = False)

print("*********************************************************************")
