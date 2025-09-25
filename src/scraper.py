# RSS feed stands for "really simple syndication" and refers to simple text files of information used in a format called XML
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree as et
from webdriver_manager.chrome import ChromeDriverManager
from seleniumbase import SB
from seleniumbase import Driver
from csv import writer
import time


def run_scraper():
    driver = Driver(uc=True)
    driver.get("https://www.indeed.com/jobs?q=software+developer&l=&from=searchOnDesktopSerp&vjk=23f82f6df4a5ac48")
    job_search_keyword = ['Software+Engineer', 'Data+Scientist', 'Data+Engineer', 'Web+Developer'] #, 'Full+Stack+Developer', 'Machine+Learning+Engineer']
    location_search_keyword = ['New York', 'California', 'Los+Angeles']
    base_url = 'https://www.indeed.com'
    paginaton_url = "https://www.indeed.com/jobs?q={}&l=New+York%2C+NY&radius=0&vjk=6d93b50af399fccf"
    with open('./data/raw_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        thewriter = writer(f)
        heading = ['job_title','company', 'description', 'link', 'pub_date']
        thewriter.writerow(heading)
        for job_keyword in job_search_keyword:
            url1 = paginaton_url.format(job_keyword)
            driver.get(url1)
            time.sleep(3)    # wait for page to load
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            results = soup.find_all('div', class_='job_seen_beacon')
            start_website(results, thewriter, driver)
        #return results
    driver.quit()



def start_website(results, thewriter,driver):
        #print(page_content[:10000])  # print first 2000 characters -- debug

    
        indeed_link = "https://www.indeed.com"
        for job in results:
            #JOB TITLE
            title_elem = job.find('h2')
            job_title = title_elem.get_text(strip=True) if title_elem else "Not available"

            #job company name
            comp_elem = job.find('span', class_='css-1h7lukg eu4oa1w0' )
            job_company = comp_elem.get_text(strip=True) if comp_elem else "Not available"

            #JOB LINK
            link_elem = job.find('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0' )
            job_link = link_elem.get('href') if link_elem else "Not available"

            job_full_link = indeed_link + job_link

            driver.get(job_full_link)
            time.sleep(3)    # wait for page to load
            job_soup = BeautifulSoup(driver.page_source, 'html.parser')

            
            #JOB DESCRIPTION
            description_elem = job_soup.find('div', id='jobDescriptionText' )
            job_description = description_elem.get_text(" ", strip=True) if description_elem else "Not available"

            #JOB publication date
            pub_elem = job_soup.find('dive', class_='jobsearch-JobMetadataFooter')
            job_pub = pub_elem.get_text(strip=True) if pub_elem else "Not available"

            print("job: ", job_title, "|company: " , job_company)
            thewriter.writerow([job_title, job_company, job_description, job_full_link, job_pub])


#run_scraper()
    
"""if __name__ == "__main__":
    
    

    # define base and pagination URLs
    

    driver = Driver(uc=True)"""



    
    