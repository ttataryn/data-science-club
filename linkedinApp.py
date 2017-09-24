from flask import Flask
from flask import render_template
from flask import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob
TEMPLATES_AUTO_RELOAD = True

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def main():
    return render_template('/home.html')

@app.route('/results', methods=['POST'])
def results():
	print("hello")
	driver = webdriver.Chrome('/Users/Taras/bin/chromedriver')
	driver.get("https://www.linkedin.com/jobs")
	url = driver.current_url
	newURL = urllib.parse.unquote(url)
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

		input1 = driver.findElement(By.xpath("//input[@placeholder='Search jobs by title, keyword or company']"))
		input2 = driver.findElement(By.xpath("//input[@placeholder='City, state, postal code or country']"))

		jobSearch = request.form['job']
		locSearch = request.form['loc']
		input1.send_keys(jobSearch)
		input2.send_keys(locSearch)

	assert "in" in driver.title
	elem = driver.find_element_by_name("keywords")
	#elem = driver.find_element_by_xpath("//input[@placeholder='Search jobs by title, keyword or company']")
	elem2 = driver.find_element_by_class_name("location-clear-icon")
	#elem3 = driver.find_element_by_xpath("//input[@placeholder='City, state, postal code or country']")
	elem3 = driver.find_element_by_name("location")
	jobSearch = request.form['job']
	locSearch = request.form['loc']
	print("Running a search on the position of " + jobSearch + " in " + locSearch + ".")
	elem2.click()

	elem.send_keys(jobSearch)
	elem3.send_keys(locSearch)
	elem.send_keys(Keys.RETURN)

	#list of Languages that are relatively popular
	plList = ['Java','C','C++','C#','Python','PHP','Javascript','Visual Basic', 'VB','.NET','Perl','Ruby',
	'R','Delphi','Swift','Assembly','Go','Objective-C','PL','SQL','Scratch','Dart','SAS','D','COBOL',
	'Ada','Erlang','Lisp','Prolog','LabVIEW', 'HTML','CSS','JQuery','ASP','Groovy','Clojure','Script','Node','Mongo']
	
	linkElements = driver.find_elements_by_class_name("job-title-link")
	links = []

	for a in linkElements:
		linkHref= a.get_attribute("href")
		links.append(linkHref)
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
		#print(jobs)
		
		languages = []

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

		#print(frame)
		i = i + 1

	if request.method == 'POST':
		frame = frame.to_html()
		return render_template("/results.html", tables=frame)


def before_request():
    app.jinja_env.cache = {}



if __name__ == '__main__':
	app.before_request(before_request)
	app.debug = True
	app.TEMPLATES_AUTO_RELOAD = True
	app.run(TEMPLATES_AUTO_RELOAD = True)