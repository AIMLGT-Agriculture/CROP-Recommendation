import math
class Distribution:
    def __init__(self, mode, maxi, mini, std_dev, unit):
        self.mode = mode
        self.maximum = maxi
        self.minimum = mini
        self.std_dev = std_dev
        self.unit = unit


    def sample(self):
        pass

    def show(self,text=""):
        print(text+" Distribution")
        print("Mean = ",self.mode," ",self.unit)
        print("Maximum = ",self.maximum," ",self.unit)
        print("Minimum = ",self.minimum," ",self.unit)
        print("Standard Deviation=",self.std_dev)

    def short_show(self,text=""):
        print(text, " Distribution : ",self.mode,",",self.maximum,",",self.minimum,",",self.std_dev,self.unit)


class Pert():
    def __init__(self,mode, minimum,maximum,gamma,unit, mean, variance):
        self.mode=mode
        self.maximum=maximum
        self.minimum=minimum
        self.gamma=gamma
        self.unit = unit
        self.mean = mean
        self.variance = variance
        #self.mean = (minimum + gamma*mode + maximum)/(gamma + 2)
        #self.variance = ((self.mean - minimum)*(maximum - self.maximum))/(gamma + 3)
        self.std_dev = math.sqrt(variance)

    def sample(self):
        pass

    def show(self,text=""):
        print(text+" Pert Distribution")
        print("Mode = ",self.mode," ",self.unit)
        print("Maximum = ",self.maximum," ",self.unit)
        print("Minimum = ",self.minimum," ",self.unit)
        print("Gamma=",self.gamma)

    def short_show(self,text=""):
        print(text, " Distribution : ",self.mode,",",self.maximum,",",self.minimum,",",self.gamma,self.unit)

class Pert_arithematic():
    def multiply(p1,p2):
        minimum = p1.minimum*p2.minimum
        maximum = p1.maximum*p2.maximum
        mode = p1.mode*p2.mode
        mean = p1.mean*p2.mean
        variance = (p1.mean**2)*p2.variance + (p2.mean**2)*p1.variance + p1.variance*p2.variance
        #std_dev = math.sqrt(variance)
        return Pert.Pert(mode, minimum, maximum, p1.gamma/2 + p2.gamma/2, p1.unit+p2.unit, mean, variance)
        #return Pert(...)

    def add(p1,p2):
        minimum = 0
        maximum = 0
        mode = 0
        mean = p1.mean+p2.mean
        variance = p1.variance + p2.variance
        #std_dev = math.sqrt(variance)
        return Pert.Pert(mode, minimum, maximum, p1.gamma/2 + p2.gamma/2, p1.unit, mean, variance)
        #return Pert(...)

    def subtract(p1,p2):
        minimum = 0
        maximum = 0
        mode = 0
        mean = p1.mean - p2.mean
        variance = p1.variance + p2.variance
        #std_dev = math.sqrt(variance)
        return Pert.Pert(mode, minimum, maximum, p1.gamma/2 + p2.gamma/2, p1.unit, mean, variance)
        #return Pert(...)

    def divide(p1,p2):
        pass
        #return Pert(...)
