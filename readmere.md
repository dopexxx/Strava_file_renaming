

Download and install Selenium
Made for FIERFOX brrowser. Download geckodriver for your OS and specify path to download folder to program (not sure that it runs for linux). Give password and username into progrram


--commuting 	 Rename all rides that have commuting tag
--private 		 Rename all private rides
--string 		 Rename all rides that contain a certain string (>1 word possible)

Ask for geckodriver path string

If string mode: Collect name of string

WHILE 
	Password and Username wrong
	Repeat




Project goal:
- Collecting first experience in using Python to navigate on websites and analyze the HTML Code to do some simple things
- Renaming a bunch of rides in Strava

Project problem definition:
- Having a bunch of rides on Strava that have the same name ("Irchel Day", "Kombi Day"), I would like to rename all those rides according to the following regular expression: "Zürich Commuting [DATE]".


Project pipeline:
1. Make yourself familiar with the python libraries that can be used to navigate on websites (JANNIK fragen?)
2. Navigate to Strava, to the Activities page
3. For all activities do:
	1. Check the title of the ride: If one of the above DO:
	2. Click on Edit the Ride
	3. Select the title section, delete current title
	4. Fill in replacing title according to the provided regExp
	5. Save the changed ride

GET STARTED:
pip install selenium
Intro: http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python

Navigate on pages? (i.e. if all rides on one side checked, do I need to click on the next page?)