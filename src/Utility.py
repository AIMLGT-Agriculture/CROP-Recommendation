import Distribution
import math

class Utility:
    def __init__(self, name):
        self.name=name

    def calculate_utility(self):
        pass

        #return an object of the distribution class

class Profit_Maximization(Utility):
    def __init__(self, Yield, price, cost_cultivation, cost_production, cycleTime):
        Utility.__init__(self,'Profit Maximization')
        self.Yield = Yield
        self.price = price
        self.cost_production = cost_production
        self.cost_cultivation = cost_cultivation
        self.cycleTime = cycleTime

    def get_product_distribution(self, d1, d2):

        std_dev = math.sqrt(((d1.std_dev**2)*(d2.std_dev**2))/((d1.std_dev**2)+(d2.std_dev**2)))
        mean = ((d1.mean * (d2.std_dev**2)) + (d2.mean * (d1.std_dev**2)))/ ((d1.std_dev**2)+(d2.std_dev**2))
        
        return Distribution.Distribution(mean, d1.maximum * d2.maximum, d1.minimum * d2.minimum, std_dev, "rupees per hectare")


    def get_profit(self, crop_yield, crop_price, cost_cultivation, cost_production, crop_cycle_time):
        profit = (crop_yield*crop_price - (cost_cultivation + cost_production * crop_yield)) / crop_cycle_time
        #print(crop_yield,crop_price,cost_cultivation,cost_production,crop_yield,crop_cycle_time)
        return profit

    def calculate_utility(self,crop,direct_parameters, weather_paramters):

        yield_distribution = self.Yield.get_prediction(crop, direct_parameters, weather_paramters)
        yield_distribution.short_show("yield")

        
        cost_production_distribution = self.cost_production.get_prediction(crop, direct_parameters, weather_paramters)
        cost_cultivation_distribution = self.cost_cultivation.get_prediction(crop, direct_parameters, weather_paramters)
        cycleTime_distribution = self.cycleTime.get_prediction(crop, direct_parameters, weather_paramters)

        
        
        cost_production_distribution.short_show("cost production")
        cost_cultivation_distribution.short_show("cost cultivation")
        cycleTime_distribution.short_show("cycle time")

        price_distribution = self.price.get_prediction(crop, direct_parameters, weather_paramters) # In QUINTALS
        price_distribution = Distribution.Distribution(price_distribution.mode * 10, price_distribution.maximum * 10, price_distribution.minimum * 10, price_distribution.std_dev * 10, "Per Tonne") # In tonne
        price_distribution.short_show("price") 

        # Get the min, max, mean cycle time
        # Price, Yield, prod cost, cultivation cost

        # create a new  direct parameter by changing the cycle time

        # Use product : http://www.lucamartino.altervista.org/2003-003.pdf
        # Use difference : https://math.stackexchange.com/questions/917276/distribution-of-the-difference-of-two-normal-random-variables
        #return combined distribution

        cycle_time = cycleTime_distribution.mode
        cost_production = cost_production_distribution.mode
        cost_cultivation = cost_cultivation_distribution.mode

        

        # d1 = Distribution.Distribution(price_distribution.mean, price_distribution.maximum, price_distribution.minimum, price_distribution.std_dev, price_distribution.unit)
        # d1.short_show("d1 : ")
        # d2 = Distribution.Distribution(yield_distribution.mean, yield_distribution.maximum, yield_distribution.minimum, yield_distribution.std_dev, yield_distribution.unit)
        # d2.short_show("d2 : ")
        # d3 = self.get_product_distribution(d1, d2)
        # d3.short_show("Product Distribution : ")
        """
        d4 = Distribution.Distribution(d3.mean - cost_cultivation, d3.maximum - cost_cultivation, d3.minimum - cost_cultivation, d3.std_dev, d3.unit)
        d4.short_show("d4")
        d5 = Distribution.Distribution(d4.mean/cycle_time, d4.maximum/cycle_time, d4.minimum/cycle_time, d4.std_dev/cycle_time, "rupees/month/hectare")
        d5.short_show("d5")


        """
        try:
            mode = self.get_profit(yield_distribution.mode, price_distribution.mode, cost_cultivation, cost_production, cycle_time)
            maximum = self.get_profit(yield_distribution.maximum, price_distribution.maximum, cost_cultivation, cost_production, cycle_time)
            minimum = self.get_profit(yield_distribution.minimum, price_distribution.minimum, cost_cultivation, cost_production, cycle_time)

            # std_dev = (maximum - minimum)/4

            std_dev = math.sqrt((mode**2 + maximum**2 + minimum**2 - mode * maximum - maximum * minimum - minimum * mode) / 18)
            actual_yield = crop.actual_yield
            actual_profit = self.get_profit(actual_yield, price_distribution.mode, cost_cultivation, cost_production, cycle_time)
            print("Actual Profit = ", actual_profit)
        except:
            print("Error in calculating profit!")
            return Distribution.Distribution(None,None,None,None,None)


        
        # print("Profit Maximization Utility")
        profit_dist = Distribution.Distribution(mode, maximum, minimum, std_dev, "rupees/month/hectare")

        return profit_dist, actual_profit

        

class Yield_Maximization(Utility):
    def __init__(self):
        pass

"""

t = current time
c = mean_crop_cycle_time
Y = yield(t+c)
P = price(t+c)
cp = cp(t+c)
cc = cc(t+c)

DF = (P.mean-cp, P.max - cp, P.min - cp, P.std_dev, P.unit)
DG = (Y.mean, Y.max, Y.min, Y.std_dev, Y.unit)

product = (Mu_FG, F_max * G_max, F_min*G_min, Sigma_FG, Rupees per hectare)

make function to get the product Mu_FG and Sigma_FG

"""
