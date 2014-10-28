
from collections import Counter

""" Parses a log file and returns List of records that match pattern

	Args:
		file_name 	(str): The location of the log file to parse
		url 	 	(str): Base URL of log entries to return
		endpoints 	(list): List of endpoints to search for and process
	
	Returns:
		dictonary with lists of data for each endpoint
"""
def get_log_endpoint_data(file_name, url, endpoints):
	# the list of data to return
	endpoint_data = {}
	# read log contents
	log_data = open(file_name,'r')
	
	# for each log entry
	for log_entry in log_data:
		# if matches base URL
		if log_entry.find(url) != -1:
			# Create list from log entry
			log = log_entry.split(' ')
			# Create list from log URLs
			log_url = log[4].split('/')

			# if URL length is 5 then test endpoint against list of required endpoints
			if len(log_url) > 4:
				# endpoint from url
				endpoint = log_url[4]
				# is this endpoint in the list of required endpoints
				add_endpoint = False

				# cycle list of required endpoints
				for target_endpoint in endpoints:
					if endpoint == target_endpoint:
						# endpoint is required in metrics
						add_endpoint = True

				if add_endpoint:
					# add to endpoint_data 
					if endpoint not in endpoint_data:
						endpoint_data[endpoint] = []

					# add to endpoint_data
					endpoint_data[endpoint].append(get_log_endpoint_list(endpoint, False, log));

			# else base endpoint
			else:
				# get endpoint log list
				endpoint_list = get_log_endpoint_list(url.replace('/', '_'), True, log)

				# add to endpoint_data 
				if endpoint_list[0] not in endpoint_data:
					endpoint_data[endpoint_list[0]] = []

				# add to endpoint_data		
				endpoint_data[endpoint_list[0]].append(endpoint_list);

	return endpoint_data

""" Parses a log file and returns List of records that match pattern

	Args:
		endpoint 	(str): The current endpoint
		base_url 	(boolean): If the URL requst method type should be appended to the endpoint
		log 		(list): List from log entry

	Returns:
		list of processed values from log file for endpoint
"""
def get_log_endpoint_list(endpoint, base_url, log):
	# parse the request method type
	method = log[3].replace('method=', '').lower()
	# update endpoint if base_url
	if base_url:
		endpoint = method + '_' + endpoint		
	# parse the dyno
	dyno = log[7].replace('dyno=', '')
	# calculate response time
	response = int(log[8].split('=')[1].replace('ms', '')) + int(log[9].split('=')[1].replace('ms', ''))
	
	# return list
	return [endpoint, method, response, dyno]

""" Parses as list and calculates mean

	Args:
		endpoint 	(list): The list of data for current endpoint
		index		(int): The index of the array from which to calculate stats

	Returns:
		mean of list provided
"""
def mean(endpoint, index):
	# temp list
	endpoint_list = []

	# create list of response times
	for response in endpoint:
		endpoint_list.append(response[index])

	# return mean
	return sum(endpoint_list) / len(endpoint_list)

""" Parses as list and calculates median

	Args:
		endpoint 	(list): The list of data for current endpoint
		index		(int): The index of the array from which to calculate stats

	Returns:
		median of list provided
"""
def median(endpoint, index):
	# temp list
	endpoint_list = []

	# create list of response times
	for response in endpoint:
		endpoint_list.append(response[index])
		
	endpoint_list = sorted(endpoint_list)
	n = len(endpoint_list)
	if not n % 2:
		# return median
		return (endpoint_list[n / 2] + endpoint_list[n / 2 - 1]) / 2.0
	# return median
	return endpoint_list[n / 2]

""" Parses as list and calculates mode

	Args:
		endpoint 	(list): The list of data for current endpoint
		index		(int): The index of the array from which to calculate stats

	Returns:
		mode of list provided
"""
def mode(endpoint, index):
	# temp list
	endpoint_list = []

	# create list of response times
	for response in endpoint:
		endpoint_list.append(response[index])

	# return mode
	return Counter(endpoint_list).most_common(1)[0]
	