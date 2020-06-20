__author__ = 'danish_wani'

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
except Exception as e:
	print(e)

from github import Github
from time import sleep
import sys
import random
import os

REPOSITORY_NAME = 'automation_repo'

class Repository:
	"""
		Creates a Repository on Github, Clones that to local machine and creates a virtual environment for the same
	"""
	def __init__(self, repo_name, ssh, private):
		self.repo_name = repo_name
		self.ssh = ssh
		self.private = private
		self.clone_url = str()

	def login(self, username, password):
		pass

	def clone_repo_locally(self):
		os.system("git clone {0}".format(self.clone_url))
		print('**Git Repo cloned successfully**')

	def create_virtualenv(self):
		os.system("sudo virtualenv -p python3 env_{0}".format(self.repo_name))
		print('**Virtualenv by the name env_{0} created successfully**'.format(self.repo_name))


class Foreground(Repository):
	"""
		Creates github repository in Foreground
	"""
	def __init__(self, repo_name=REPOSITORY_NAME, ssh=False, private=True):
		super().__init__(repo_name=repo_name, ssh=ssh, private=private)
		self.bot = object()

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

	def create(self):
		options_dropdown = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH, "/html/body/div[1]/header/div[6]/details")))
		options_dropdown.click()	#navigates to new repo page
		new_repo = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH, "/html/body/div[1]/header/div[6]/details/details-menu/a[1]")))
		new_repo.click()
		repo_name_field = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.ID, "repository_name")))
		repo_name_field.clear()
		repo_name_field.send_keys(self.repo_name)

		# if provided repo name already exists
		sleep(2)
		new_name = str()
		while 'is-autocheck-successful' not in repo_name_field.get_attribute('class'):
			sleep(2)
			repo_name_field.clear()
			new_name = self.repo_name+str(random.randint(0,9))
			repo_name_field.send_keys(new_name)
			sleep(2)

		if self.private:
			WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_private"]'))).click()
		else:
			WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_public"]'))).click()
		
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_visibility_public"]'))).click()	#make the repo public
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="repository_auto_init"]'))).click()	#initialize th readme
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="new_repository"]/div[3]/button'))).click()	#submit and create the repo
		print('**Repository on Github successfully created by the name {0}**'.format(new_name if new_name else self.repo_name))
		self.get_github_repo_click()

	def get_github_repo_click(self):
		WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH,'/html/body/div[4]/div/main/div[2]/div/div[3]/span/get-repo-controller/details/summary'))).click()
		link_field = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable
			((By.XPATH,'/html/body/div[4]/div/main/div[2]/div/div[3]/span/get-repo-controller/details/div/div/div[1]/div[1]/div/input')))
		self.repo_link = link_field.get_attribute("value")
		self.bot.quit()


class Background(Repository):
	"""
		Creates github repository in Background
	"""
	def __init__(self, repo_name=REPOSITORY_NAME, ssh=True, private=True):
		super().__init__(repo_name=repo_name, ssh=ssh, private=private)
		self.github = object()
		self.user = object()
	
	def login(self, username, password):
		try:
			self.github = Github(username, password)
			self.user = self.github.get_user()
			self.user.login
			print('Login successfull')
		except Exception as e:
			print(e)
			return e

	def create(self):
		try:
			repo = self.user.create_repo(self.repo_name, private=self.private)
			if self.ssh:
				self.clone_url = repo.ssh_url
			else:
				self.clone_url = repo.clone_url
			print('Successfully created the repo', self.clone_url)
		except Exception as e:
			print(e)
			return e


class Main:
	def __init__(self):
		self.main()

	def main(self):
		username, password, repo_name = self.fetch_credentials()
		ssh, private, background = self.fetch_extra_params()

		if background:
			project_task = Background(repo_name=repo_name, ssh=ssh, private=private)
		else:
			project_task = Foreground(repo_name=repo_name,  ssh=ssh, private=private)
		credentials_error = project_task.login(username, password)
		if credentials_error:
			print('Invalid credentials')
			return
		repository_error = project_task.create()
		if repository_error:
			print('Repository with the provided name already exists')
			return
		sleep(3)
		project_task.clone_repo_locally()
		project_task.create_virtualenv()

	@staticmethod
	def fetch_credentials():
		username, password, repo_name = [value.strip() for value in str(input('Enter username, password and repository name, separted by comma(,): \n')).split(',')]
		if not repo_name:
			repo_name = REPOSITORY_NAME
		return username, password, repo_name

	def fetch_extra_params(self):
		ssh = str(input('Do you want to clone over ssh? (Y/N) N -> https (Default is ssh): \n'))
		ssh = self.get_boolean(ssh)
		
		private = str(input('Do you want to keep the repository private? (Y/N): \n'))
		private = self.get_boolean(private)

		background = str(input('Do you want to run the process in background(recommended)? (Y/N): \n'))
		background = self.get_boolean(background)
		return ssh, private, background

	@staticmethod
	def get_boolean(input_value):
		if input_value.lower() == 'y' or not input_value:
			return True
		else:
			return False

if __name__ == '__main__':
	Main()

	
