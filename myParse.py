
""" ****add / remove fields where appropriate, delete this line when done****
--------------------------------------------------------------------------------
Descriptive Name     : myParse.py.
Author               : Sihao Yin 								      
Contact Info         : yin93@purdue.edu
Date Written         : 2018.01.24
Description          : Parse camera and metadata from San Diego Zoo website 
Command to run script: Python myParse.py
Usage                : maybe you want to do chmod u+x before run just in case 
Input file format    : (eg. url#description (on each line))
Output               : (eg. <file name> or <on screen>)
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://animals.sandiegozoo.org/live-cams
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
import urllib
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import time

def Navigate():
	#initialise the file and geocoding classes for use in the GetInfo
	key = None 
	coords = Geocoding('Google',key)
	file = open('list_zoo_cam.txt','w')
	firstLine = "country#state#city#animal#snapshot_url#latitude#longtitude" 
	#use firefox to go to the zoo's website 
	driver = webdriver.Firefox()
	driver.get("http://animals.sandiegozoo.org/live-cams")	
	
	#navigating the webpage and click every cameras  
	cameras = driver.find_elements_by_class_name("live-cams-row")
	for i in range(len(cameras)):
		cameras[i].click()
		GetInfo(driver,coords,file)
		time.sleep(1)
		driver.back()
		cameras = driver.find_elements_by_class_name("live-cams-row")
		time.sleep(1)	
	file.close()
	driver.close()
def GetInfo(driver,coords,file):
	#get the location San Digeo Zoo and city San Diego
	location = giveStr(driver.find_element_by_xpath("//meta[@property='og:site_name']"))
	print(location)
	city = location[:9]
	animal = giveStr(driver.find_element_by_xpath("//meta[@property='og:title']"))
	#get the url 
	url = (driver.find_element_by_xpath("//div[@class='videoWrapper']/iframe")).get_attribute("src")
	latitude = "Not Avaliable"
	longitude = "Not Avaliable"
	try:
		coords.locateCoords(location,city,"CA","USA")
		latitude = coords.latitude
		longitude = coords.longitude
	except:
		print ("UNexpected error:",sys.exc_info()[0])
		raise
	info = "USA"+"#"+"CA"+"#"+city+"#"+animal+"#"+url+"#"+latitude+"#"+longitude+"\n\n"
	file.write(info)
def giveStr(obj):
	return obj.get_attribute("content")
if __name__ == '__main__':
	Navigate()
