import sys, os, time, argparse, re, getpass
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from Helper import argParsing 


def replaceName(openEditSec=True):
	'''
	Being core element of the tool, this method deletes the current activity name and fills in the desired one 
	plus appending the date of the trip (in reversed order)
	'''

	if openEditSec:
		openEditSection()

	textBox = act.find_element_by_xpath(pathToEdit + "//td[@style='']//div[@class='form-group']//input[@id='name']")
	textBox.clear()

	datetimeO = datetime.strptime(date, '%d.%m.%Y')
	dateShort = str(datetimeO.date())[2:4] + str(datetimeO.date())[5:7] + str(datetimeO.date())[8:10]

	textBox.send_keys(newStr +' '+ dateShort)
	textBox.send_keys(Keys.RETURN)
	time.sleep(2)

	print('Affected activity repaired, new title: ', newStr+' '+dateShort)


def openEditSection():

	editButton = act.find_elements_by_xpath("//td[@class='view-col col-actions']//ul[@class='list-inline bottomless']"
					"//li//button[@class='btn btn-link btn-xs quick-edit']")
	editButton[ind].click()








# Extract user input
argDict = argParsing(sys.argv)
print('These are your specified parameters: ', argDict)


# Verify dependencies
geckoP = str(input("Please specify the path to your geckodriver: "))
while True:
	try:
		browser = webdriver.Firefox(executable_path=os.getcwd()+geckoP)
	except FileNotFoundError:
		geckoP = str(input("File was not found. Please verify OS-version of your driver, put it in a subdirectory of this file" +
			" and specify path again: "))
		continue
	break


#Login 
browser.get('http://strava.com/dashboard')
while True:

	t = browser.find_element_by_id('email')
	email = str(input("Please enter the emailadress of your account: "))
	t.send_keys(email)
	t = browser.find_element_by_id('password')
	pw = str(getpass.getpass("Please enter the password of your account: "))
	t.send_keys(pw)
	t.send_keys(Keys.RETURN)

	# Check whether login succesful
	time.sleep(1)
	browser.get('http://strava.com/athlete/training')
	try:
		a = browser.find_element_by_id('email') 
	except NoSuchElementException:
		break
	print('Password wrong, try again!')
	continue

if argDict['string']:
	oldStr = str(input("Please enter the substring contained in all activities you want to rename: "))
newStr = str(input("Please enter the new name for all affected activites: "))


pathToEdit = "//td[@class='edit-col']//form//table[@class='table-layout table-activity-edit']//tbody//tr"

# Navigate to activities 
browser.get('http://strava.com/athlete/training')
# How many activities are there in total
txt = re.search(' [0-9]+',browser.find_element_by_class_name('text-center').text)
numberOfAct = int(txt.group())
numberOfPages = 1 + numberOfAct // 20
curAct = 0
argDict['N'] = numberOfAct if argDict['N'] == 0 else argDict['N']

# Iterate over all pages of activities
for page in range(numberOfPages):
	print("Look at page ", page+1)
	table = browser.find_element_by_xpath("//table[@id='search-results']")
	acts = table.find_elements_by_class_name('training-activity-row')

	# Iterate over all activities on that page
	for ind,act in enumerate(acts):
		
		# Check whether already done
		if curAct >= argDict['N']:
			print('Job done')
			sys.exit()
		else:
			curAct += 1

		# Extract meta data
		dtO = re.search('[0-3]?[0-9]\.[0-1]?[0-9]\.20[0-9]{2}',act.text)
		date = dtO.group()
		durO = re.search('([0-9]:)?[0-5]?[0-9]?:[0-5][0-9]',act.text)
		duration = durO.group()
		name = act.text[dtO.span()[1]+1 : durO.span()[0]-1]

		try:
			print('Activity no', curAct, ' title: ', name)
		except UnicodeEncodeError:
			print('Actitivity title cannot be displayed')

		name = name.lower() # To undo case sensitivity for title matching

		# Check whether activity is affected
		if argDict['string'] and name.find(oldStr.lower()) > -1:
		    replaceName()

		if argDict['private']: # If all private rides should be replaced

			privObj = act.find_element_by_xpath(".//td[@class='view-col col-title']//div[@title='Privat']")
			if privObj.get_attribute('style') == 'display: inline-block;':
				replaceName()

		if argDict['commute']: # If all commuting rides should be replaced

			openEditSection()
			time.sleep(2)
			t = act.find_element_by_xpath(pathToEdit + "//td[@style='']//div[@class='ride-only checkbox']")
			
			print(t.find_element_by_xpath(".//label//input[@id='commute']").get_attribute('value'))
			print(t.get_attribute('style') == 'display: block;')

			if t.get_attribute('style') == 'display: block;' and \
				t.find_element_by_xpath(".//label//input[@id='commute']").get_attribute('value'):

					# If commute value is set to true and the ride only box is displayed we found a commuting ride
					replaceName(openEditSec=False)
			else:
				# Close the EditSection
				act.find_element_by_xpath(pathToEdit + "//td[@class='edit-actions']//"
				"button[@class='btn btn-link cancel ml-sm']").click()
			


            
    # Now move to the next page:
	pageSwitchO = browser.find_element_by_class_name('switches')
	buttons = pageSwitchO.find_elements_by_xpath(".//*")
	buttons[3].click()
	time.sleep(2)

print("Job done!")
browser.quit()
