__author__ = 'danish_wani'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
import random
import os

PROJECT_NAME = 'task_demo'

class Project:
        """
            Creates a Repository on Github, Clones that to local machine and creates a virtual environment for the same
        """
	def __init__(self, project_name):
		self.project_name = project_name

	def login(self, username, password):
		self.username = username
		self.password = password
		self.bot = webdriver.Firefox()
		self.bot.get('https://github.com/login')
		username_field = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.ID, "login_field")))
		password_field = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.ID, "password")))
		username_field.clear()
		password_field.clear()
		username_field.send_keys(self.username)
		password_field.send_keys(self.password)
		password_field.send_keys(Keys.RETURN)
		print('**Login Successful**')

	def create_github_repo(self):
		options_dropdown = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH, "/html/body/div[1]/header/div[7]/details")))
		options_dropdown.click()	#navigates to new repo page
		new_repo = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH, "/html/body/div[1]/header/div[7]/details/details-menu/a[1]")))
		new_repo.click()
		repo_name_field = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.ID, "repository_name")))
		repo_name_field.clear()
		repo_name_field.send_keys(self.project_name)

		# if provided repo name already exists
		while 'is-autocheck-successful' not in repo_name_field.get_attribute('class'):
			sleep(2)
			repo_name_field.clear()
			new_name = self.project_name+str(random.randint(0,9))
			repo_name_field.send_keys(new_name)
			sleep(2)

		# uncomment below code if you want to take input from the user for the visibility of Repo
		# self.visibility = str(input('Do you want to make this Repostory Private? Y/N          '))
		# if self.visibility.lower() == 'y':
			# WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_private"]'))).click()
		# else:
			# WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_public"]'))).click()
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_public"]'))).click()	#make the repo public
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_auto_init"]'))).click()	#initialize th readme
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="new_repository"]/div[3]/button'))).click()	#submit and create the repo
		print('**Repository on Github successfully created by the name {0}**'.format(new_name))

	def get_github_repo_click(self):
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH,'/html/body/div[4]/div/main/div[2]/div[1]/div[3]/details[2]/summary'))).click()
		link_field = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH,'/html/body/div[4]/div/main/div[2]/div[1]/div[3]/details[2]/div/div/div[1]/div[1]/div/input')))
		self.repo_link = link_field.get_attribute("value")

	def clone_repo_locally(self):
		os.chdir("/home/danish/Workspace/projects/")
		os.system("git clone {0}".format(self.repo_link))
		print('**Git Repo cloned successfully**')

	def create_virtualenv(self):
		os.chdir("/home/danish/Workspace/envs/")
		os.system("sudo virtualenv -p python3 env_{0}".format(self.project_name))
		print('**Virtualenv by the name env_{0} created successfully**'.format(self.project_name))


if __name__ == '__main__':
	if len(sys.argv) > 1:
		project_name = str(sys.argv[1])
	else:
		project_name = PROJECT_NAME
	project_task = Project(project_name)
	project_task.login('danish-wani','danish@17')
	project_task.create_github_repo()
	project_task.get_github_repo_click()
	sleep(3)
	project_task.bot.quit()
	project_task.clone_repo_locally()
	project_task.create_virtualenv()
	