'''
Calcula CDD das temperaturas definidas pelo intervalo definido.
'''

import glob
import pandas

MIN_THRESHOLD = 15
MAX_THRESHOLD = 22

FILES = glob.glob('*.epw')
print(FILES)

THRESHOLDS = list(range(MIN_THRESHOLD, MAX_THRESHOLD+1))

def cdd_add(threshold, t):
	if t > threshold:
		cdd = t - threshold
	else:
		cdd = 0
	return(cdd)

DATA = {'Climate': []} #, 'CDD_DRY': [],'CDD_WET': []}

for threshold in THRESHOLDS:
	DATA['CDD'+str(threshold)+'_DRY'] = []
	DATA['CDD'+str(threshold)+'_WET'] = []

for file in FILES:

	cdd_dry = [0] * (MAX_THRESHOLD+1 - MIN_THRESHOLD)
	cdd_wet = [0] * (MAX_THRESHOLD+1 - MIN_THRESHOLD)

	with open(file, encoding = 'latin-1') as file_reader:
		start_sum = False
		for line in file_reader:
			if start_sum:
				line = line.split(',')
				for i in range(len(THRESHOLDS)):
					cdd_dry[i] += cdd_add(THRESHOLDS[i], float(line[6]))
					cdd_wet[i] += cdd_add(THRESHOLDS[i], float(line[7]))

			if 'DATA PERIODS' in line:
				start_sum = True

	DATA['Climate'].append(file)
	for i in range(len(THRESHOLDS)):			
		DATA['CDD'+str(THRESHOLDS[i])+'_DRY'].append(cdd_dry[i])
		DATA['CDD'+str(THRESHOLDS[i])+'_WET'].append(cdd_wet[i])


output = pandas.DataFrame(DATA)

output.to_csv("CDD.csv", index=False)