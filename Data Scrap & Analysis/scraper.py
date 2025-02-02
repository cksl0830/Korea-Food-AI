"""
pip install selenium
pip install webdriver_manager
"""

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from webdriver_manager.utils import ChromeType

class getRecipeCrawler:
    def __init__(self):
        self.url = 'https://www.10000recipe.com/'   
        self.nextPage = [
            '//*[@id="content"]/section/div[2]/div/div[2]/a[2]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[5]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[6]',
            '//*[@id="content"]/section/div[2]/div/div[2]/a[7]'
            ]
        self.location = 'a.call_recipe > strong'

    def launch_crawler(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)

    def find_click(self, xpath, sleep_interval=0.1):
        btn = self.driver.find_element_by_xpath(xpath)
        btn.click()
        time.sleep(sleep_interval)
    
    def find_recipe(self, ingredient):
        search_box = self.driver.find_element_by_name('name')
        search_box.send_keys(ingredient)
        search_box.submit()

    def get_recipe(self, element):
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')
        recipeName = self.soup.select(element)
        for recipe in recipeName:
            return recipe.text

    def run(self):
        result = []
        self.launch_crawler()
        
        key = input("재료를 입력하세요: ")
        self.find_recipe(key)

        for i in range(len(self.nextPage)):
            recipe = self.get_recipe(self.location)

            recipe_obj = {
                'recipe_ID': i,
                'recipe_Name': recipe,
                'ingredient_Key': key
            }
            print(recipe)
            result.append(recipe_obj)

            self.find_click(self.nextPage[i])

        return print(result)
        
        

        time.sleep(2)
        self.driver.quit()

if __name__ == "__main__":
    crawler = getRecipeCrawler()
    crawler.run()
