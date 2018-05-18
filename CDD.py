'''
Calculates CDD for different temperature thresholds defined
'''

import glob
import pandas

# Creates a list with the degrees chosen to be the threshold.
# If it's not needed to pick one by one, you can create a list called "THRESHOLDS"
# with whatever values you want.
MIN_THRESHOLD = 15
MAX_THRESHOLD = 22
THRESHOLDS = list(range(MIN_THRESHOLD, MAX_THRESHOLD+1))

# Lists weather files in folder
FILES = glob.glob('*.epw')
#print(FILES)

def cdd_add(threshold, t):
	# Calculates how much temperature is above threshold

	if t > threshold:
		cdd = t - threshold
	else:
		cdd = 0
	return(cdd)

# Creates a dictionary to organize the values
DATA = {'FILE_NAME': []}

# Creates a CDD for each threshold defined by the THRESHOLD list
for threshold in THRESHOLDS:
	DATA['CDD'+str(threshold)+'_DRY'] = []
	DATA['CDD'+str(threshold)+'_WET'] = []

# Reads each .epw file listed in the folder
for file in FILES:

	# Creates a list where each value on the list will be the CDD for each threshold
	cdd_dry = [0] * (len(THRESHOLDS))
	cdd_wet = [0] * (len(THRESHOLDS))

	# Opens each file
	with open(file, encoding = 'latin-1') as file_reader:
		
		# Condition created so it doesn't take values from the header
		start_sum = False
		
		# Reads each line of the .epw file
		for line in file_reader:
			
			# Checks if it's over reading the header
			if start_sum:

				# Splits lines by comma
				line = line.split(',')

				# adds how much line's temperature is above threshold and adds it to the sum
				for i in range(len(THRESHOLDS)):
					cdd_dry[i] += cdd_add(THRESHOLDS[i], float(line[6]))
					cdd_wet[i] += cdd_add(THRESHOLDS[i], float(line[7]))

			# Checks if it's the last line of the header
			if 'DATA PERIODS' in line:
				start_sum = True

	# Adds the filename and the CDDs to the dictionary
	DATA['FILE_NAME'].append(file)
	for i in range(len(THRESHOLDS)):			
		DATA['CDD'+str(THRESHOLDS[i])+'_DRY'].append(cdd_dry[i]/24)
		DATA['CDD'+str(THRESHOLDS[i])+'_WET'].append(cdd_wet[i]/24)

# Turns de DATA as a pandas' Data Frame
output = pandas.DataFrame(DATA)

# Save pandas' Data Frame to a .csv file
output.to_csv("CDD.csv", index=False)
