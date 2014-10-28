import sys
import json
import argparse
import pocket.pocketparse
import pocket.pocketprint

if __name__ == "__main__":

	endpoint_output = []

	# Define the cmd line args
	parser=argparse.ArgumentParser(description='''Parse a log file to determine metrics.''')
	parser.add_argument('--file', '-f', type=str, help='path to log file, i.e. /var/log/apache2/access.log', required=True)
	parser.add_argument('--url', '-u', type=str, default='api/users', help='base URL endpoint to extract for analysis (pattern match), i.e. /api/users/')
	parser.add_argument('--endpoints', '-e', type=list, default=['count_pending_messages','get_messages', 'get_friends_progress', 'get_friends_score'], help='list of endpoints for metrics calculations (pattern match)')
	parser.add_argument('--output', '-o', type=str, default='text', choices=['text', 'json'], help='output the results in table format or as json')
	args=parser.parse_args()

	# get the endpoint data - returned as dictionary with args.endpoints as indicies containing lists
	endpoint_data = pocket.pocketparse.get_log_endpoint_data(args.file, args.url, args.endpoints)

	for key in endpoint_data:
		# Place final output data into list
		endpoint_output.append([key, 
			len(endpoint_data[key]),
			pocket.pocketparse.mean(endpoint_data[key], 2),
			pocket.pocketparse.median(endpoint_data[key], 2),
			pocket.pocketparse.mode(endpoint_data[key], 2)[0],
			pocket.pocketparse.mode(endpoint_data[key], 3)[0]
		])

	if args.output == 'text':
		# pretty print table header
		endpoint_output.insert(0, ["endpoint", "times called", "mean(resp. time)", "median(resp. time)", "mode(resp. time)", "dyno resp. most"])
		# pretty print table data
		pocket.pocketprint.pprint_table(sys.stdout, endpoint_output)
	else:
		# print json
		print json.dumps(endpoint_output)
