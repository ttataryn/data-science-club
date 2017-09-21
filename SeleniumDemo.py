from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from textblob import TextBlob
import urllib
import base64
import pandas as pd
import matplotlib as plt

def collect(webdriver):
	plList = ['Java','C','C++','C#','Python','PHP','Javascript','Visual Basic', 'VB','.NET','Perl','Ruby',
	'R','Delphi','Swift','Assembly','Go','Objective-C','PL','SQL','Scratch','Dart','SAS','D','COBOL',
	'Ada','Erlang','Lisp','Prolog','LabVIEW', 'HTML','CSS','JQuery','ASP','Groovy','Clojure','Script','Node','Mongo']
	driver = webdriver
	linkElements = driver.find_elements_by_class_name("job-title-link")
	links = []

	for a in linkElements:
		linkHref= a.get_attribute("href")
		links.append(linkHref)
		print([i for i in links])
	#a.send_keys(Keys.RETURN)
	#time.sleep(3)
	#driver.back()



	for link in links:
		driver.get(link)
		#jobDesc = driver.find_element_by_class_name("description-section")
		soup = BeautifulSoup(driver.page_source, "html.parser")

		jobDesc = soup.find("div", class_="description-section").text

		blob = TextBlob(jobDesc)
		jobTitle1 = urllib.parse.unquote("jobs-details-top-card__job-title Sans-21px-black-85%-dense")
		jobTitle = driver.find_element_by_class_name(jobTitle1)
		print(jobTitle)

	#results = soup.p.find_all(string=re.compile('.*{0}.*'.format(plList)), recursive=True)
	#print(results)
		for lang in plList:
			if lang not in blob:
				continue
			elif lang in blob:
				print(lang)


#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--incognito")
def main():
	driver = webdriver.Chrome('/Users/Taras/bin/chromedriver')
	driver.get("https://www.linkedin.com/jobs")
	url = driver.current_url
	newURL = urllib.parse.unquote(url)
	print(newURL)
	if newURL != "https://www.linkedin.com/jobs/?trk=jobs-home-jobsfe-redirect":
		print("hello")
		signIn = urllib.parse.unquote("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fjobs%2F%3Ftrk%3Djobs-home-jobsfe-redirect&fromSignIn=true&trk=uno-reg-join-sign-in")
		driver.get(signIn)
		email = driver.find_element_by_name("session_key")
		email.send_keys("tarastataryn_2018@depauw.edu")
		pwd = driver.find_element_by_name("session_password")
		pwd.send_keys("Leroyiheanacho19$")
		signInBtn = driver.find_element_by_name("signin")
		signInBtn.click()
		collect(driver)
		#logIn = driver.find_element_by_class_name("form-toggle")
		#logIn.click()
	assert "in" in driver.title
	elem = driver.find_element_by_name("keywords")
	#elem = driver.find_element_by_xpath("//input[@placeholder='Search jobs by title, keyword or company']")
	elem2 = driver.find_element_by_class_name("location-clear-icon")
	#elem3 = driver.find_element_by_xpath("//input[@placeholder='City, state, postal code or country']")
	elem3 = driver.find_element_by_name("location")
	jobSearch = input("What keyword would you like to search for? ")
	locSearch = input("Where would you like to run this search on? ")
	print("Running a search on the position of " + jobSearch + " in " + locSearch + ".")



	#elem.clear()
	elem2.click()

	elem.send_keys(jobSearch)
	elem3.send_keys(locSearch)
	elem.send_keys(Keys.RETURN)
	#button = driver.find_element_by_xpath("//button[text()='Search']")
	#button.click()
	assert "No results found." not in driver.page_source
	plList = ['Java','C','C++','C#','Python','PHP','Javascript','Visual Basic', 'VB','.NET','Perl','Ruby',
	'R','Delphi','Swift','Assembly','Go','Objective-C','PL','SQL','Scratch','Dart','SAS','D','COBOL',
	'Ada','Erlang','Lisp','Prolog','LabVIEW', 'HTML','CSS','JQuery','ASP','Groovy','Clojure','Script','Node','Mongo']
	
	linkElements = driver.find_elements_by_class_name("job-title-link")
	links = []

	for a in linkElements:
		linkHref= a.get_attribute("href")
		links.append(linkHref)
		#print([i for i in links])
	#a.send_keys(Keys.RETURN)
	#time.sleep(3)
	#driver.back()

	i=1
	frame = pd.DataFrame( columns=[i], index=['Job Title', 'Company', 'Languages', 'Total Langs'])

	for link in links:
		driver.get(link)
		#jobDesc = driver.find_element_by_class_name("description-section")
		soup = BeautifulSoup(driver.page_source, "html.parser")

		jobDesc = soup.find("div", class_="description-section").text

		blob = TextBlob(jobDesc)
		#jobTitle1 = urllib.parse.unquote("h1.jobs-details-top-card__job-title.Sans-21px-black-85%-dense")
		jobTitle = driver.find_element_by_tag_name("h1").text

		companyName = driver.find_element_by_class_name("company").text
		companies = []
		companies.append(companyName)
		print(companies)
		#print(jobTitle.text) #works -- prints job title
		jobs = []
		jobs.append(jobTitle)
		print(jobs)
		
		languages = []



	#results = soup.p.find_all(string=re.compile('.*{0}.*'.format(plList)), recursive=True)
	#print(results)
		count = 0
		for lang in plList:
			if lang not in blob:
				continue
			elif lang in blob:
				languages.append(lang)
				count = count + 1
		jobs = ''.join(jobs)
		companies = ''.join(companies)
		languages = ', '.join(languages)
		finalArr = []
		finalArr.append(jobs)
		finalArr.append(companies)
		finalArr.append(languages)
		finalArr.append(count)


		
		frame[i] = finalArr
		print(frame)
		i = i + 1
		
		colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]

# Create a pie chart
	plt.pie(
    # using data total)arrests
    	df['Total Langs'],
    # with the labels being officer names
    	labels=df['Languages'],
    # with no shadows
    	shadow=False,
    # with colors
    	colors=colors,
    # with one slide exploded out
    	explode=(0, 0, 0, 0, 0.15),
    # with the start angle at 90%
    	startangle=90,
    # with the percent listed as a fraction
    	autopct='%1.1f%%',
    	)

# View the plot drop above
	plt.axis('equal')

# View the plot
	plt.tight_layout()
	plt.show()


				
if __name__ == "__main__":
	main()
