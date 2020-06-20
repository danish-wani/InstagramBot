__author__ = 'danish_wani'


#https://selenium-python.readthedocs.io/from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class InstagramBot():
	"""
		Searches for a hashtag and likes the posts found
	"""
	def __init__(self,username,password):
		self.username = username
		self.password = password

	def login(self):
		self.bot = webdriver.Firefox()
		self.bot.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
		sleep(3)
		username_field = self.bot.find_element_by_name("username")
		password_field = self.bot.find_element_by_name("password")
		username_field.clear()
		password_field.clear()
		username_field.send_keys(self.username)
		password_field.send_keys(self.password)
		password_field.send_keys(Keys.RETURN)
		sleep(3)
		self.bot.find_element_by_class_name("aOOlW").click()	#closes Allow notications pop up of instagram

	def search(self,hashtag):
		sleep(2)
		search_field = self.bot.find_element_by_class_name("XTCLo")		#selects the search field
		search_field.send_keys(hashtag)
		sleep(2)
		self.bot.find_element_by_class_name("yCE8d").click()	#selects the first search result
		sleep(2)
		thumbnails = self.bot.find_elements_by_class_name("Nnq7C")	#gets all the posts
		for thumbnail in thumbnails:
			thumbnail.click()	#opens a post
			sleep(3)
			like_button = self.bot.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]")
			like_button.click()	#likes the post
			sleep(2)
			self.bot.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()	#closes the modal showing preview of Post
		self.bot.close()

if __name__ == '__main__':
	username, password, hashtag = [value.strip() for value in str(input('Enter username, password and hashtag separted by comma(,): \n')).split(',')]
	insta_bot = InstagramBot(username, password)	# provide credentials of the instagram account
	try:
		insta_bot.login()
	except Exception as ex:
		print('Invalid Credentials  ',ex)
	try:
		insta_bot.search(hashtag)	#provide the hashtag
	except Exception as e:
		print(e)
