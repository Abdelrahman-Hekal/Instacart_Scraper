from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
import time
import csv
import os
from datetime import datetime
import pandas as pd
import numpy as np
import warnings
import unidecode
warnings.filterwarnings('ignore')



def initialize_bot():

    # Setting up chrome driver for the bot
    #chrome_options = uc.ChromeOptions()
    #chrome_options.add_argument('--headless')
    #############################################################################
    # Create empty profile for Mac OS
    #if os.path.isdir('./chrome_profile'):
    #    shutil.rmtree('./chrome_profile')
    #os.mkdir('./chrome_profile')
    #Path('./chrome_profile/First Run').touch()
    #chrome_options.add_argument('--user-data-dir=./chrome_profile/')
    ##############################################################################
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    #chrome_options.add_argument('--log-level=3')
    #chrome_options.add_argument("--enable-javascript")
    #chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument("user-data-dir=C:\\Users\\hekal\\AppData\\Local\\Google\\Chrome\\User Data")
    #chrome_options.add_argument("--disable-blink-features")
    #chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-impl-side-painting")
    #chrome_options.add_argument("--disable-setuid-sandbox")
    #chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    #chrome_options.add_argument("--disable-breakpad")
    #chrome_options.add_argument("--disable-client-side-phishing-detection")
    #chrome_options.add_argument("--disable-cast")
    #chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    #chrome_options.add_argument("--disable-cloud-import")
    #chrome_options.add_argument("--disable-popup-blocking")
    #chrome_options.add_argument("--ignore-certificate-errors")
    #chrome_options.add_argument("--disable-session-crashed-bubble")
    #chrome_options.add_argument("--disable-ipv6")
    #chrome_options.add_argument("--allow-http-screen-capture")
    #chrome_options.add_argument("--disable-extensions") 
    #chrome_options.add_argument("--disable-notifications") 
    #chrome_options.add_argument("--disable-infobars") 
    #chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument('--disable-dev-shm-usaging')
############################################
    #chrome_options.page_load_strategy = 'eager'
    #driver = uc.Chrome(options=chrome_options)


    ## Setting up chrome driver for the bot
    chrome_options  = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("user-data-dir=C:\\Users\\abdel\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver_path = ChromeDriverManager().install()
    chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    return driver


def scrape_data(driver, output, path, scraped):

    store = 'Kroger'
    URL = "https://www.instacart.com/store/foodhall/storefront"
    driver.get(URL)
    time.sleep(3)
    wait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @class='css-s3ybpu']"))).click()
    address = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='streetAddress' and @id='streetAddress']")))
    address.send_keys('1745 Morse Rd, Columbus, OH 43229')
    time.sleep(3)
    try:
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='css-46w1lj-AddressSuggestionList' and @role='button']"))).click()
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-qaboj3' and @type='submit']"))).click()
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-13suvkx-Confirmation']"))).click()
    except:
        skip = True
    time.sleep(3)
    # getting departments list
    URL = "https://www.instacart.com/store/kroger/storefront"
    driver.get(URL)
    time.sleep(3)
    ul = wait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-1eag065-StoreMenu")))
    lis = wait(ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
    exclude = ['kitchen supplies', 'party & gift supplies', 'miscellaneous', 'floral', 'office & craft', 'shop', 'recipes']
    ndept = len(lis)
    for i in range(ndept):
    #for i in range(1):
        URL = "https://www.instacart.com/store/kroger/storefront"
        driver.get(URL)
        time.sleep(3)
        ul = wait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-1eag065-StoreMenu")))
        lis = wait(ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
        if lis[i].text.lower() in exclude:
            continue
        print('Scraping Department {}'.format(lis[i].text))
        department = lis[i].text
        a = wait(lis[i], 60).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        link = a.get_attribute('href')
        driver.get(link)
        time.sleep(3)
        # getting categories list under each department
        ul = wait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-1eag065-StoreMenu")))
        lis = wait(ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
        sub_ul = wait(lis[i], 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-bng902-MenuLink")))
        sub_lis = wait(sub_ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
        ncat = len(sub_lis)
        for j in range(ncat):
            time.sleep(3)
            ul = wait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-1eag065-StoreMenu")))
            lis = wait(ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
            sub_ul = wait(lis[i], 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.css-bng902-MenuLink")))
            sub_lis = wait(sub_ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
            category = sub_lis[j].text
            print('Scraping Category {}'.format(sub_lis[j].text))
            if category in scraped[:-1]:
                continue
            a = wait(sub_lis[j], 60).until(EC.presence_of_element_located((By.TAG_NAME, "a"))) 
            link = a.get_attribute('href')
            driver.get(link)
            time.sleep(3)

            # displaying the full product list of the category
            while True:
                try:
                    wait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-1rlooc3-ItemsGrid"))).click() 
                    time.sleep(1)
                except:
                    break

            # scrape products of each category
            list_div = wait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-ufx9ox-ItemsGrid")))
            prod_ul = wait(list_div, 60).until(EC.presence_of_element_located((By.TAG_NAME, "ul")))
            prod_li = wait(prod_ul, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))

            if scraped:
                if category == scraped[-1]:
                    df = pd.read_csv(output)
                    df = df[df['Category'] == category]
                    nscraped = len(df['Product URL'].unique().tolist())
                    prod_li = prod_li[nscraped:]
            for item in prod_li:
                try:
                    # open product page
                    wait(item, 60).until(EC.presence_of_element_located((By.TAG_NAME, "a"))).click()
                    time.sleep(5)
                    # getting product details
                    data = []
                    ingred, prod_name, warning = 'NA', 'NA', 'NA'
                    try:
                        prod_name = wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.css-gx0lhm"))).text 
                        prod_name = unidecode.unidecode(prod_name)
                    except:
                        try:
                            prod_name = wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.css-11h8ccw"))).text 
                            prod_name = unidecode.unidecode(prod_name)
                        except:
                            prod_name = 'NA'

                    link = driver.current_url

                    try:
                        div1 = wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-m7xg5w-DetailSections")))
                        divs = wait(div1, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-8atqhb")))
                        for div in divs:
                           header = div.find_element_by_tag_name('h2').text
                           if header.lower() == 'warnings':
                               warning = div.find_element_by_tag_name('p').text
                               warning = unidecode.unidecode(warning)
                           elif header.lower() == 'ingredients':
                               ingred = div.find_element_by_tag_name('p').text
                               ingred = unidecode.unidecode(ingred)
                    except:
                        skip = True

                    ingred = ingred.replace('.', ',').replace('[', ',').replace(']', ',').replace('(', ',').replace(')', ',').replace(';', ',').replace('/', ',').replace('\\', ',').replace('*', ',').replace('-', ',').replace('&', ',').replace('+', ',').replace('=', ',').replace('^', ',').replace('$', ',').replace('#', ',').replace('{', ',').replace('}', ',').replace('<', ',').replace('>', ',').replace('?', ',').replace(':', ',').strip()
                    ingred_list = ingred.split(',')
                    for ing in ingred_list:
                        ing = ing.strip()
                        if len(ing) > 0 and not ing[:-1].isnumeric():
                            data.append([store, department, category, prod_name, link, warning, ingred, ing])
                except:
                    continue

                with open(output, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data) 

                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            if category not in scraped:
                with open(path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([category])

def initialize_output():

    # removing the previous output file
    path = os.getcwd()
    files = os.listdir(path)
    for file in files:
        if 'Scraped_Data' in file:
            os.remove(file)

    header = ['Store', 'Department', 'Category', 'Product Name', 'Product URL', 'Warnings Text', 'Ingredients Text', 'Single Ingredients']


    filename = 'Scraped_Data_{}.csv'.format(datetime.now().strftime("%d_%m_%Y_%H_%M"))

    if path.find('/') != -1:
        output = path + "/" + filename
    else:
        output = path + "\\" + filename

    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)    
        
    return output
  
def resume_output():

    # removing the previous output file
    found = False
    path = os.getcwd()
    files = os.listdir(path)
    for file in files:
        if 'Scraped_Data' in file:
            found = True
            if path.find('/') != -1:
                output = path + "/" + file
            else:
                output = path + "\\" + file

    if found:
        return output
    else:
        return 'N/A'

def clear_screen():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux
    else:
        _ = os.system('clear')

def get_prod_names(driver):

    urls_data = os.getcwd() + '\\' + 'links.csv'
    df = pd.read_csv(urls_data)
    urls = df.iloc[:, 0].values
    names = []
    for i, url in enumerate(urls):
        if i > 0:
            if url == urls[i-1]:
                names.append(names[-1])
                continue

        driver.get(url)
        time.sleep(3)
        prod_name = wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.css-gx0lhm"))).text 
        prod_name = unidecode.unidecode(prod_name)
        names.append([prod_name, url])

    output = os.getcwd() + '\\' + 'names.csv'
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', 'Product Link'])
        writer.writerows(names)

def match_prod_urls():

    df1 = pd.read_csv(os.getcwd() + '\\' + 'names.csv', keep_default_na=False)
    df2 = pd.read_csv(os.getcwd() + '\\' + 'Scraped_Data_Kroger.csv', keep_default_na=False)
    df2['Product Name'] = df2['Product Name'].fillna('NA')
    inds = df2[df2['Product Name'] == 'NA'].index
    for ind in inds:
        url = df2.loc[ind, 'Product URL']
        name = df1[df1['Product Link'] == url].values[0][0]
        df2.loc[ind, 'Product Name'] = name

    df2.to_csv(os.getcwd() + '\\output.csv', index=False, encoding='UTF-8')
    
def process_ingred():

    df = pd.read_csv(os.getcwd() + '\\' + 'Instacart_Kroger_Data_v2.csv', keep_default_na=False)
    df['Single Ingredients'] = df['Single Ingredients'].apply(lambda x: x.strip().title())
    df2 = df['Single Ingredients'].value_counts()
    df2.to_csv(os.getcwd() + '\\Ingredients.csv', encoding='UTF-8')
    df.to_csv(os.getcwd() + '\\output.csv', index=False, encoding='UTF-8')
    
if __name__ == '__main__':

    start_time = time.time()
    #driver = initialize_bot()
    #clear_screen()
    #output = resume_output()
    #if output == 'N/A':
    #    output = initialize_output()


    #while True:
    #    cwd = os.getcwd()
    #    scraped = []
    #    if cwd.find('/') != -1:
    #        path = cwd + "/" + 'log.csv'
    #    else:
    #        path = cwd + "\\" + 'log.csv'

    #    if os.path.isfile(path):
    #        df = pd.read_csv(path)
    #        scraped = df.iloc[:,0].values.tolist()
    #    else:
    #        with open(path, 'w', newline='') as file:
    #            writer = csv.writer(file)
    #            writer.writerow(['category'])
    #    try:
    #        print('-'*50)
    #        print('Scraping Data....')
    #        print('-'*50)
    #        scrape_data(driver, output, path, scraped)
    #        print('-'*50)
    #        print('Outputting Scraped Data....')
    #        df_out = pd.read_csv(output)
    #        df_out.drop_duplicates(inplace=True)
    #        df_out.to_csv(output, encoding='UTF-8', index=False)
    #        break
    #    except:
    #        print('Error in scraping the data, retrying ...')
    #        print('-'*50)
    #        driver.quit()
    #        time.sleep(3)
    #        driver = initialize_bot()

    #get_prod_names(driver)
    #match_prod_urls()
    #process_ingred()
    print('Data is scraped successfully! Total scraping time is {:.1f} mins'.format((time.time() - start_time)/60))
    print('-'*50)



