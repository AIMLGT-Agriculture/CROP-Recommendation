import math

class Portfolio():
	def __init__(self):
		pass

	def sharpeRatio(self, crop_utilities, ratio):
		# crop1 = crop_utilities[0]
		# crop2 = crop_utilities[1]
		# a = ratio[0]
		# b = ratio[1]
		# expected_value = a * crop1.mode + b * crop2.mode
		# std_dev = math.sqrt((a**2)*(crop1.std_dev**2) + (b**2)*(crop2.std_dev**2))

		expected_value = 0.0
		std_dev = 0.0

		for i in range(len(ratio)):
			expected_value += (ratio[i] * crop_utilities[i].mode)
			std_dev += (ratio[i]**2)*(crop_utilities[i].std_dev**2)

		std_dev = math.sqrt(std_dev)

		return 0.8 * expected_value/std_dev

	def sortinoRatio(self, crop_utilities, ratio):

		crop1 = crop_utilities[0]
		crop2 = crop_utilities[1]
		a = ratio[0]
		b = ratio[1]
		
		average_realized_return = a * crop1.mode + b * crop2.mode
		minimum_acceptable_return = 0
		target_semi_deviation = 0

	# def riskFactor(self, risks, ratio):
	# 	# a = ratio[0]
	# 	# b = ratio[1]

	# 	risk = 0.0

	# 	for i in range(len(ratio)):
	# 		risk += (ratio[i]*risks[i])
	# 	return risk

	def riskFactor(self, crop_utilities, ratio):
		# crop1 = crop_utilities[0]
		# crop2 = crop_utilities[1]
		# a = ratio[0]
		# b = ratio[1]
		# expected_value = a * crop1.mode + b * crop2.mode
		# std_dev = math.sqrt((a**2)*(crop1.std_dev**2) + (b**2)*(crop2.std_dev**2))

		expected_value = 0.0
		std_dev = 0.0

		for i in range(len(ratio)):
			expected_value += (ratio[i] * crop_utilities[i].mode)
			std_dev += (ratio[i]**2)*(crop_utilities[i].std_dev**2)

		std_dev = math.sqrt(std_dev)

		return std_dev/expected_value

	def logUtility(self, crop_utilities, ratio):
		crop1 = crop_utilities[0]
		crop2 = crop_utilities[1]
		a = ratio[0]
		b = ratio[1]
		val1 = a*crop1.maximum + b*crop2.maximum
		val2 = a*crop1.minimum + b*crop2.minimum
		sign1 = 1
		sign2 = 1
		if val1 < 0:
			sign1 = -1
		if val2 < 0:
			sign2 = -1
		return sign1*math.log(abs(val1)) + sign2*math.log(abs(val2))

	


