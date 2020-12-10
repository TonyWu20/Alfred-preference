import os
from sys import argv, stdout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import re
# import multiprocessing as mp
# from functools import wraps
path = os.path.abspath('.')
driver_path = f'{path}/chromedriver'


class pandas_search(object):
    def search(self, keyword):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        with webdriver.Chrome(driver_path, options=option) as self.driver:
            query = keyword
            self.driver.get(f'https://pandas.pydata.org/pandas-docs/stable/search.html?q={query}&check_keywords=yes&area=default')
            wait = WebDriverWait(self.driver, 25)
            res = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="search-results"]/ul/li[10]/a')))

            def get_results(i):
                i = i + 1
                result = res.find_element_by_xpath(
                    f'//*[@id="search-results"]/ul/li[{i}]/a')
                link = result.get_attribute('href')
                title = result.text
                try:
                    context = res.find_element_by_xpath(f'//*[@id="search-results"]/ul/li[{i}]/div').text
                    result = {"Title": title,
                              "Subtitle": context, "Link": link}
                except:
                    result = {"Title": title,
                              "Subtitle": link, "Link": link}
                return result
            result_list = [get_results(i) for i in range(10)]
            self.driver.quit()
        return result_list


class matplotlib_search(object):
    def search(self, keyword):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        with webdriver.Chrome(driver_path, options=option) as self.driver:
            query = keyword
            self.driver.get(f'https://matplotlib.org/search.html?q={query}&check_keywords=yes&area=default')
            wait = WebDriverWait(self.driver, 10)
            time.sleep(2)
            self.res = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="search-results"]/h2')))
            search_page = self.res.find_element_by_xpath(
                '//*[@id="search-results"]/h2')
            condition = search_page.text
            if condition == 'Search Results':
                report = self.res.find_element_by_xpath(
                    '//*[@id="search-results"]/p')
                number = re.findall(r"\d+", report.text)[0]
                num = int(number)
                result = [self.get_results(i) for i in range(num)]
                return result
            else:
                result = [self.get_results(i) for i in range(10)]
                return result

    def get_results(self, i):
        i = i + 1
        element = self.res
        try:
            result = element.find_element_by_xpath(
                f'//*[@id="search-results"]/ul/li[{i}]/a')
        except:
            return {"Title": 'Not found', "Subtitle": 'Result not generated', "Link": ''}
        context_xpath = f'//*[@id="search-results"]/ul/li[{i}]/div'
        link = result.get_attribute('href')
        title = result.text
        try:
            context = self.res.find_element_by_xpath(context_xpath).text
            result = {"Title": title, "Subtitle": context, "Link": link}
        except:
            result = {"Title": title, "Subtitle": link, "Link": link}
        return result


class numpy_search(object):
    def search(self, keyword):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        with webdriver.Chrome(driver_path, options=option) as self.driver:
            query = keyword
            self.driver.get(f'https://docs.scipy.org/doc/numpy/search.html?q={query}&check_keywords=yes&area=default')
            wait = WebDriverWait(self.driver, 25)
            res = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="search-results"]/ul/li[10]/a')))

            def get_results(i):
                i = i + 1
                result = res.find_element_by_xpath(f'//*[@id="search-results"]/ul/li[{i}]/a')
                link = result.get_attribute('href')
                title = result.text
                result = {"Title": title, "Subtitle": link, "Link": link}
                return result
            result_list = [get_results(i) for i in range(10)]
        return result_list


def makeItem(query, url, title, subtitle, search):
    icon = {
        'pandas': 'pandas.png',
        'matplotlib': 'matplotlib_med.png',
        'numpy': 'numpy-logo-300.png'
    }
    item = {
        'uid': url,
        'title': title,
        'subtitle': subtitle,
        'arg': url,
        'autocomplete': query,
        'icon': {
            'path': icon[search]
        }
    }
    return item


def makeReturn(items):
    out = {
        'items': items
    }
    return out


def main():
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    search_type = argv[2]
    search = {
        'pandas': pandas_search(),
        'matplotlib': matplotlib_search(),
        'numpy': numpy_search()
    }
    engine = search[search_type]
    results = engine.search(query)
    results_num = len(results)
    items = [makeItem(query, results[i]['Link'], results[i]['Title'], results[i]['Subtitle'], search_type)
             for i in range(results_num)]
    out = makeReturn(items)
    return json.dumps(out, indent=4) + '\n'


if __name__ == '__main__':
    data = main()
    stdout.write(data)
    # print(data)
