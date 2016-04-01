
from pandas.io.parsers import read_csv
from datetime import datetime
from matplotlib import pyplot
import math

#k = 2
MAX_K = 10

def tryFormat(packed):
	try:
		return datetime.strptime("{0} {1}".format(packed[0], packed[1]), "%d %m")
	except:
		return None

def load_data(filename, linear=True):
  dataframe = read_csv(filename)
  y = dataframe['TMAX']
  
  cols = zip(dataframe['DAY'], dataframe['MONTH'])

  dates = map(tryFormat, cols)
    
  return dates, y


data2015, output2015 = load_data('~/Downloads/78616478.csv')
data2016, output2016 = load_data('~/Downloads/2016_examples.csv')


zipped2015 = zip(data2015, output2015)
sortedZipped2015 = sorted(zipped2015, key=lambda x: x[0])
data2015, output2015 = zip(*sortedZipped2015)

def predictDate(date, k):
	if not date:
		return None
	atIndex = data2015.index(date)
	indices = range(atIndex - k, atIndex)
	predicted = float(sum([output2015[x] for x in indices])) / float(k)
	return predicted

def predict(day, month, k):
	queryDate = datetime.strptime("{0} {1}".format(day, month), "%d %m")
	#queryDate.replace(year=2015)
	atIndex = data2015.index(queryDate)
	indices = range(atIndex - k, atIndex)
	predicted = float(sum([output2015[x] for x in indices])) / float(k)
	return predicted

def actual(day, month):
	queryDate = datetime.strptime("{0} {1}".format(day, month), "%d %m")
	atIndex = data2015.index(queryDate)
	return output2015[atIndex]

def actualDate(date):
	if not date:
		return None
	date.replace(year=2015)
	atIndex = data2015.index(date)
	return output2015[atIndex]

predicted = []
for k in range(1, MAX_K):
	errors = []
	for date in data2016:
		actualVal = actualDate(date)
		prediction = predictDate(date, k)
		if actualVal and prediction:
			errors += [math.fabs(actualVal - prediction)]

	predicted += [sum(errors) / len(errors)]

pyplot.plot(predicted)
pyplot.title("K vs. Error")
pyplot.xlabel("K")
pyplot.ylabel("Error")
pyplot.show()
