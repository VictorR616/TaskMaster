from selenium import webdriver
from todo_task.models import Task
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestTaskListPage(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.quit()

