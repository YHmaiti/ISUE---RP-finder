import re
import requests
import pandas as pd
import Libraries.xploreapi as xplore
from bs4 import BeautifulSoup
#from selenium import webdriver 
#from selenium.webdriver.common.by import By 
#from selenium.webdriver.support.ui import WebDriverWait 
#from selenium.webdriver.support import expected_conditions as EC 
#from selenium.common.exceptions import TimeoutException


class ACM:
  def __init__(self):
    self.site = 'acm'
    self.url = 'https://dl.acm.org'
    self.query = '/action/doSearch?AllField={request}&startPage={page_num}&pageSize=50'
    
  def _get_page(self, request, page_num):
    formatted_query = self.query.format(request=request, page_num=page_num)
    page = requests.get(self.url + formatted_query)
    return BeautifulSoup(page.content, 'html.parser')

  def get_all_papers(self, request):
    page_num = 0
    papers = pd.DataFrame(columns=['site', 'title', 'year_published', 'link'])
    while True:
      page_result = self._parse_page(self._get_page(request, page_num))
      print(f'Page {page_num} completed.')
      
      if len(page_result['title']) == 0:
        return papers
      
      papers = papers.append(pd.DataFrame(page_result), ignore_index=True)
      page_num += 1

  def _parse_page(self, page):
    site = []
    titles = []
    years = []
    links = []

    for paper in page.find_all('div', class_='issue-item'):
      result = self._parse_paper(paper)

      site.append(self.site)
      titles.append(result['title'])
      years.append(result['year'])
      links.append(self.url + result['link'])
    return { 'site': site, 'title': titles, 'year_published': years, 'link': links }
    
  def _parse_paper(self, paper):
    title = paper.find('h5', class_='issue-item__title')
    year = paper.find('div', class_='bookPubDate')
    link = title.find('a')
    
    return {'title': title.get_text().strip(), 'year': int(year.get('data-title').split()[-1]), 'link': link.get('href')}

class IEEE:
  # TODO: Get selenium to work, or scrap it and go with the api
  def __init__(self):
    self.site = 'ieee'
    self.url = 'https://ieeexplore.ieee.org'
    self.api_key = 'pn8zjc3jb7faeezapws5xxss' # figure out how to get around this limitation / uniqueness
    self.request_type = 'article_title'
    self.query = xplore.XPLORE(self.api_key)
    #self.driver = webdriver.Edge(executable_path='Drivers/msedgedriver', service_log_path='Logs/msedgedriver.log')
    #self.driver.get(self.url)

  def _request(self, request):
    if self.request_type == 'article_title':
      self.query.articleTitle(request)
    return self.query.CALLAPI()

  def _parse_result(self, result):
    title = result.find('a')
    year = result.find('div', class_='publisher-info-container')
    link = result.find('a')

    return {'title': title.get_text().strip(), 'year': int(re.findall(r'\d{4}', year.get_text())[0]), 'link': link.get('href')}

class SPRINGER:
  # Think about using the download for search results rather than webscrape
  def __init__(self):
    self.site = 'springer'
    self.url = 'https://link.springer.com'
    self.query = '/search/page/{page_num}?query={request}'
    
  def _get_page(self, request, page_num):
    formatted_query = self.query.format(request=request, page_num=page_num)
    page = requests.get(self.url + formatted_query)
    return BeautifulSoup(page.content, 'html.parser')

  def get_all_papers(self, request):
    page_num = 1
    papers = pd.DataFrame(columns=['site', 'title', 'year_published', 'link'])
    while True:
      page_result = self._parse_page(self._get_page(request, page_num))
      print(f'Page {page_num} completed.')
      
      if len(page_result['title']) == 0:
        return papers
      
      papers = papers.append(pd.DataFrame(page_result), ignore_index=True)
      page_num += 1

  def _parse_page(self, page):
    site = []
    titles = []
    years = []
    links = []

    results_list = page.find('ol', class_='content-item-list')
    for paper in results_list.find_all('li'):
      result = self._parse_paper(paper)

      if result == None:
        continue

      site.append(self.site)
      titles.append(result['title'])
      years.append(result['year'])
      links.append(self.url + result['link'])
    return { 'site': site, 'title': titles, 'year_published': years, 'link': links }
    
  def _parse_paper(self, paper):
    title = paper.find('a', class_='title')
    year = paper.find('span', class_='year')
    link = title
    
    if title == None:
      return None

    if year == None:
      year = 0
    else:
      year = int(year.get_text().strip('()'))
    title.get_text().strip()
    link.get('href')
    return {'title': title.get_text().strip(), 'year': year, 'link': link.get('href')}



class ResearchPaperScraper:
  
  def __init__(self):
    select_database = int(input('Select a database to search from this list:\n\t1. acm\n\t2. ieee (not implemented)\n\t3. springer\n: '))
    self.ieee = IEEE()
    self.acm = ACM()
    self.springer = SPRINGER()
    if select_database == 1:
      self.database = self.acm
    elif select_database == 2:
      #self.database = self.ieee
      pass
    elif select_database == 3:
      self.database = self.springer
    
    search_request = input('Enter search query: ')
    search_request = search_request.replace(' ', '+')
    self.request = search_request


# CSV Format: site, title, year_published, link
scraper = ResearchPaperScraper()
papers = scraper.database.get_all_papers(scraper.request)
papers.to_csv('./papers.csv')
