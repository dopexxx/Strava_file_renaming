import sys, os, re

def argParsing(args):

	argDict = {'private':False, 'commute':False, 'string':False, 'N':0}

	# Display help if requested
	if '--help' in args or '-help' in args or '-h' in args:
		showHelp()

	# If no flag, then enter string mode
	if len(args) == 1:
		argDict['string'] = True

	# If one flag and it is -N flag, also enter string mode:
	if len(args) == 2:
		limit = re.search('[0-9]+', args[1])
		if limit != None:
			argDict['N'] = int(limit.group())
			argDict['string'] = True

	# Enter private mode
	if '--private' in args or '-private' in args:
		argDict['private'] = True

	# Enter commute mode and make sure that not a double mode
	if '--commute' in args or '-commute' in args:
		if argDict['private']:
			print('Please choose either -commute or -private flag')
			sys.exit()
		argDict['commute'] = True

	# Enter string mode (if explicitly specified)
	if '--string' in args or '-string' in args:
		if argDict['private'] or argDict['commute']:
			print('Please choose only one of the flags: -private, -commute, -string' )
			sys.exit()
		argDict['string'] = True

	# Extract how many activities should be examined (0 if not specified)
	for arg in args:
		limit = re.search('[0-9]+',arg)
		if limit != None:
			argDict['N'] = int(limit.group())

	if not argDict['private'] and  not argDict['string'] and not argDict['commute']:
		print("Please specify exactly one of the 3 flags (-commute, -private, -string) or do not specify any to"
			" enter string mode.")
		sys.exit()

	if argDict['commute']:
		print("Sorry. This mode does not work yet due to inconsistencies in Stravas HTML source code.")
		sys.exit()

	return argDict


def showHelp():

	print('This is a small tool to rename multiple activities on Strava. \n ')
	print('For further information, please check out the readme. Below I list the flag you can set to use this tool.')
	print('Flags are intended to set the mode of the program. Without any provided flags, program will check ALL your')
	print('activities and replace the title of the activity by a new title if it contains a certain substring. You will')
	print('be asked for both, the old (sub)-title and the new title later. \n')

	print('---------------------------------- Options ------------------------------------\n')
	print('\t -private: \t \t This flag allows to you rename all private activities ')
	print('\t -commute: \t \t This flag allows you to rename all commuting rides ')
	print("Either use the '-private' or the '-commute' flag, but not both at the same time \n")
	print('\t -N: \t \t Instead of renaming all activities, you can specify that only the N ')
	print('\t \t \t latest activites should be verified. Use this flag independently from the others.')

	sys.exit()

