
import locale
locale.setlocale(locale.LC_NUMERIC, "")

############
# The code for this module is referenced from
# 	http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
############

""" Format a number according to given places. Adds commas, etc. Will truncate floats into ints!

	Args:
		num 	(num): The number to format
	
	Returns:
		formatted string of num
"""
def format_num(num):
	try:
		inum = int(num)
		return locale.format("%.*f", (0, inum), True)

	except (ValueError, TypeError):
		return str(num)

"""Get the maximum width of the given column index

	Args:
		table 	(list): The list of data
		index	(num): Column index 

	Returns:
		max width of list
"""

def get_max_width(table, index):
	return max([len(format_num(row[index])) for row in table])

"""Prints out a table of data, padded for alignment

	Args: 
		out: 	(stream) Output stream (file-like object)
		table: 	(list) The table to print. A list of lists

	Returns:
		null: prints table to cmd line	
"""
def pprint_table(out, table):
	col_paddings = []

	print ""

	for i in range(len(table[0])):
		col_paddings.append(get_max_width(table, i))

	for row in table:
		# left col
		print >> out, row[0].ljust(col_paddings[0] + 1),
		# rest of the cols
		for i in range(1, len(row)):
			col = format_num(row[i]).rjust(col_paddings[i] + 2)
			print >> out, col,
		print >> out