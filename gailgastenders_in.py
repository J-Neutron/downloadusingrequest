import datetime
import os
import shutil
import zipfile

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import time
import sqlite3
import logging
import requests
from os.path import basename
import pyodbc as pyodbc
import json
import netrc
import scrapy
from scrapy.utils.response import open_in_browser
from requests_html import HTMLSession
from fake_useragent import UserAgent




search_url = 'https://www.tenderwizard.com/ROOTAPP/Mobility/index.html?dc=encygBmHTtkq4tornNA2KAOLw==#/home'
name = search_url.split('//')[1]
d_name = name.split('/')[0]
app_name = d_name.replace('.','_')
server_name = d_name.replace('.','_') + 'py_TenderListing'
d_name = d_name + 'py'

all_file_path = os.getcwd()
sqlite_path = f'{all_file_path}\\{app_name}.db'
csv_path = f'{all_file_path}\\{app_name}.csv'
temp_down_path = all_file_path + '\\temp_files\\'
download_path = os.path.expanduser('~') + '\\Documents\\PythonDocuments\\' + d_name + '\\files\\'
log_path = os.path.expanduser('~') + '\\Documents\\PythonLogs\\'
chrome_driver_path = os.path.join(os.environ['USERPROFILE'],"Desktop") + f'\\Python\\available Tender\\chromedriver\\'


single_page_list, single_row_list = [], []
page_nos, skip_tenders_counts, pos, scraping_compleated, flags, pg, data_string, questionmark_string, q_string, Documents_2 = '', 0, 0, False, 1, 5, '', '', '', ''
page_index,next_page,tender_index = 1, 1, 1
scraping_completed_flag = True
sqlite_connection = sqlite3.connect(sqlite_path)
sqlite_cursor = sqlite_connection.cursor()
if os.path.exists(log_path):
    logging.basicConfig(filename=log_path + '\\' + app_name + '.log', format='%(asctime)s %(message)s', filemode='a', level=logging.INFO)
else:
    os.makedirs(log_path)
    logging.basicConfig(filename=log_path + '\\' + app_name + '.log', format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
if os.path.exists(all_file_path):
    pass
else:
    os.makedirs(all_file_path)
if os.path.exists(download_path):
    pass
else:
    os.makedirs(download_path)
if os.path.exists(temp_down_path):
    if len(os.listdir(temp_down_path)) != 0:
        for i in os.listdir(temp_down_path):
            if os.path.isdir(temp_down_path + i):
                shutil.rmtree(temp_down_path + i)
            elif os.path.isfile(temp_down_path + i):
                os.remove(temp_down_path + i)
    else:
        pass
else:
    os.makedirs(temp_down_path)
if os.path.exists(chrome_driver_path):
    pass
else:
    os.makedirs(chrome_driver_path)


try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": temp_down_path,  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": False  # It will not show PDF directly in chrome
    })
    driver = webdriver.Chrome(options=options, service=Service(executable_path=os.path.join(os.environ['USERPROFILE'],
                                                                                          "Desktop") + f'\\Python\\available Tender\\chromedriver\\chromedriver.exe'))
    driver.get(search_url)
    logging.info(f'Connection to {search_url}')
    # driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    action = ActionChains(driver)
except Exception as e:
    logging.error(str(e))
    logging.error(f'Driver Error')
time.sleep(1)


data_string = '''Tender_Notice_No, Tender_Summery, Documents_2, Purchaser_Name, actualvalue, DocFees, EMD,
     Pur_Add, Pur_Country, Pur_Email, Pur_URL, currency, TenderType, createdOn,
     remove_extra_space(Content), OpeningDate, Bid_deadline_2, DupFlag'''
for i in data_string.split(','):
    q_string += '?'
questionmark_string = ','.join(q_string)



def download(len_of_data_list):
    files = []
    try:
        global scraping_completed_flag
        scraping_completed_flag = True
        global Documents_2
        driver.find_element(By.XPATH,f'/html/body/form/contenttemplate/table/tbody/tr[2]/td/table/tbody/tr/td[2]')
        if len(os.listdir(temp_down_path)) == len_of_data_list:
            for i in os.listdir(temp_down_path):
                if i.endswith('.crdownload') or i.endswith('.tmp'):
                    time.sleep(1)
                    download(len_of_data_list)
                    files.append(False)
                else:
                    files.append(True)
                if all(files):
                    if len(os.listdir(temp_down_path)) == 1:
                        extention = '.' + str(i)[::-1].split('.')[0][::-1]
                        # print(f'""""""""""{extention}""""""""""')
                        name1 = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime('%d%m%Y_%H%M%S%f')
                        os.rename(temp_down_path + i, temp_down_path + 'wcci_' + name1 + extention)
                        time.sleep(1)
                        shutil.move(temp_down_path + 'wcci_' + name1 + extention, download_path)
                        Documents_2 = download_path + 'wcci_' + name1 + extention

                        print(f'.......... {Documents_2} ..........')
                        logging.info(f"File download completed = {Documents_2}")
                        scraping_completed_flag = True
                    else:
                        extention = '.' + str(i)[::-1].split('.')[0][::-1]
                        # print(f'""""""""""{extention}""""""""""')
                        name1 = datetime.datetime.strptime(str(datetime.datetime.now()),
                                                           '%Y-%m-%d %H:%M:%S.%f').strftime('%d%m%Y_%H%M%S%f')
                        os.rename(temp_down_path + i, temp_down_path + 'wcci_' + name1 + extention)
                        time.sleep(1)
                        # shutil.move(temp_down_path + 'wcci_' + name1 + extention, download_path)
                        # Documents_2 = 'multiple files'
                        # logging.info(f"File download completed = {Documents_2}")
                        scraping_completed_flag = True
        else:
            time.sleep(1)
            download(len_of_data_list)
    except Exception as e:
        print(f'download code = {str(e)}')
        scraping_completed_flag = False
        Documents_2 = ''

def remove_extra_space(string):
    new = ' '.join(string.split())
    return new

def zipdir(path, ziph):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    elif os.path.isfile(path):
        ziph.write(path, basename(path))

def create_zip_code(unique_name):
    global Documents_2
    zip_name = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime('%d%m%Y_%H%M%S%f')
    Documents_2 = download_path + unique_name + zip_name + '.zip'
    print(f'----- {Documents_2} -----')
    with zipfile.ZipFile(Documents_2, mode='w') as zipf:
        for j in os.listdir(temp_down_path):
            # zipf.write(temp_down_path + j, basename(temp_down_path + j))
            zipdir(temp_down_path + j, zipf)

    for k in os.listdir(temp_down_path):
        if os.path.isdir(temp_down_path + k):
            shutil.rmtree(temp_down_path + k)
        elif os.path.isfile(temp_down_path + k):
            os.remove(temp_down_path + k)

def text_to_number(data):
    v = ''
    try:
        if 'lac' in data or 'lakh' in data:
            v = float(data.split(' ')[0]) * 100000
        elif 'cr' in data:
            v = float(data.split(' ')[0]) * 10000000
        elif 'each' in data:
            v = float(data.split(' ')[0])
        elif '/' in data:
            v = float(data.split('/')[0])
        else:
            v = float(data)
    except Exception as e:
        print(e)
    return v

def sqlite_code(main_li):
    try:
        sqlite_cursor.executemany(f'''INSERT INTO {app_name}(
                            {data_string})
                            VALUES({questionmark_string});''',
                                  main_li)

        sqlite_cursor.execute(f'''SELECT 
                            {data_string}
                            FROM {app_name} WHERE flag = ?''', (1,))
        data2 = sqlite_cursor.fetchall()

        if data2 != []:
            server_connection = pyodbc.connect('DRIVER={SQL Server};'
                                               'SERVER=153TESERVER;'
                                               'DATABASE=CrawlingDB;'
                                               'UID=hrithik;'
                                               'PWD=hrithik@123')
            logging.info('The connection to the server has been established successfully')
            server_cursor = server_connection.cursor()

            ID_val = server_name + ' ID'
            server_cursor.execute(f'''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[{server_name}]') AND type in (N'U'))
                                                    CREATE TABLE {server_name} (
                                                    "{ID_val}" UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
                                                    Tender_Notice_No nvarchar(4000),
                                                    Tender_Summery nvarchar(4000),
                                                    Tender_Details nvarchar(max), 
                                                    Bid_deadline_2 nvarchar(4000),
                                                    Documents_2 nvarchar(4000), 
                                                    TenderListing_key nvarchar(4000), 
                                                    Notice_Type nvarchar(4000), 
                                                    Competition nvarchar(4000), 
                                                    Purchaser_Name nvarchar(4000), 
                                                    Pur_Add nvarchar(4000), 
                                                    Pur_State nvarchar(4000), 
                                                    Pur_City nvarchar(4000), 
                                                    Pur_Country nvarchar(4000), 
                                                    Pur_Email nvarchar(4000), 
                                                    Pur_URL nvarchar(4000),
                                                    Bid_Deadline_1 nvarchar(4000),
                                                    Financier_Name nvarchar(4000),
                                                    CPV nvarchar(4000),
                                                    scannedImage nvarchar(4000),
                                                    Documents_1 nvarchar(4000),
                                                    Documents_3 nvarchar(4000),
                                                    Documents_4 nvarchar(4000),
                                                    Documents_5 nvarchar(4000),
                                                    currency nvarchar(4000),
                                                    actualvalue nvarchar(4000),
                                                    TenderFor nvarchar(4000),
                                                    TenderType nvarchar(4000),
                                                    SiteName nvarchar(4000),
                                                    createdOn nvarchar(4000),
                                                    updateOn nvarchar(4000),
                                                    Content varchar(max),
                                                    Content1 nvarchar(4000),
                                                    Content2 nvarchar(4000),
                                                    Content3 nvarchar(4000),
                                                    DocFees nvarchar(4000),
                                                    EMD nvarchar(4000),
                                                    OpeningDate nvarchar(4000),
                                                    Tender_No nvarchar(4000))''')

            server_connection.commit()
            q = f'''INSERT INTO {server_name} ({data_string}) 
            VALUES({questionmark_string})'''
            server_cursor.executemany(q, data2)
            server_connection.commit()
            sqlite_connection.commit()
            print('Data inserted into sqlite successfully')
            logging.info(f'Data inserted in sqlite successfully')
            logging.info(f'Data inserted on server')
            print('Data inserted on server')
            server_cursor.close()
            server_connection.close()

            sql1 = f'UPDATE {app_name} SET flag ={0} WHERE flag = {1};'
            sqlite_cursor.execute(sql1)
            sqlite_connection.commit()
            logging.info(f'Flag updated')
        else:
            print(f'Data already available in sqlite database')
            logging.info(f'Data already available in sqlite database')
    except Exception as e:
        print(f'sqlite code = {e}')
        logging.error(str(e))
        logging.error(f'Sqlite Error')
        driver.quit()
    print('\n\n\n')

def get_year(data):
    return int(((data[::-1])[0:4])[::-1])

def GetImageCookies():
    print('Extracting Browser Cookies')
    image_cookies = ''
    for cookie in driver.get_cookies():
        if cookie['name'] == 'ssc':
            image_cookies += 'ssc={};'.format(cookie['value'])
        elif cookie['name'] == 'ghsdfkjlksssalk35bbr':
            image_cookies += 'ghsdfkjlksssalk35bbr={};'.format(cookie['value'])
    # print(image_cookies)
    return image_cookies

def SaveImage(captcha_file, img_link):
    print('Saving the captcha image')
    header = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,en-US;q=0.9,ar;q=0.8',
    'Cookie': GetImageCookies(),
    'Host': 'masked',
    'Referer': 'masked',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}


    pic = requests.get(img_link,verify=False,headers = header)
    if pic.status_code == 200:
        with open(captcha_file + 'master.jpg', 'wb') as f:
            f.write(pic.content)

def scraping():
    try:
        Tender_Summery = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//td[contains(.,"Description Of Work:")]//following::td'))).text
    except Exception as e:
        logging.error(str(e))
        logging.error(f'Tender_Summery Element not available')
        Tender_Summery = ''

    try:
        Tender_Notice_No = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//span[text() = 'Tender:']//..//..//td[2]"))).text.strip()
    except Exception as e:
        logging.error(str(e))
        logging.error(f'Tender_Notice_No Element not available')
        Tender_Notice_No = ''
    print(Tender_Notice_No)

    try:
        Content = driver.find_element(By.XPATH, '/html/body/div[3]')
        Content = Content.get_attribute('innerHTML')
    except Exception as e:
        logging.error(str(e))
        logging.error(f'Content Element not available')
        Content = ''

    try:
        Pur_Add = 'State bank of india'
    except:
        logging.error(str(e))
        logging.error(f'Pur_Add Element not available')
        Pur_Add = ''

    try:
        Pur_Email = driver.find_element(By.XPATH, "//span[text() = 'Email:']//..//..//td[2]").text.strip()
    except:
        logging.error(str(e))
        logging.error(f'Pur_Email Element not available')
        Pur_Email = ''

    try:
        TenderType = driver.find_element(By.XPATH,"//span[text() = 'Type of Tender:']//..//..//td[2]").text.strip()
    except:
        logging.error(str(e))
        logging.error(f'TenderType Element not available')
        TenderType = ''


    try:
        actualvalue = driver.find_element(By.XPATH,"//span[text() = 'Estimated Cost:']//..//..//td[2]").text.split()[0].strip().replace(',', '')
    except:
        logging.error(str(e))
        logging.error(f'actualvalue Element not available')
        actualvalue = ''

    try:
        DocFees = driver.find_element(By.XPATH,"//span[text() = 'Form Fee:']//..//..//td[4]").text.split()[0].strip().replace(',', '')
    except:
        logging.error(str(e))
        logging.error(f'DocFees Element not available')
        DocFees = ''

    try:
        EMD = driver.find_element(By.XPATH,"//td[contains(.,'EMD')]//..//td[2]").text.split()[0].strip().replace(',', '')
    except:
        logging.error(str(e))
        logging.error(f'EMD Element not available')
        EMD = ''

    try:
        OpeningDate = driver.find_element(By.XPATH,"//span[text() = 'Issue of Tender Document From:']//..//..//td[4]").text.split()[0].strip().replace('-', '/')
    except:
        logging.error(str(e))
        logging.error(f'OpeningDate Element not available')
        OpeningDate = ''

    try:
        Bid_deadline_2 = driver.find_element(By.XPATH,"//span[text() = 'Tender Closing Date and Time:']//..//..//td[4]").text.split()[0].strip().replace('-', '/')
    except:
        logging.error(str(e))
        logging.error(f'Bid_deadline_2 Element not available')
        Bid_deadline_2 = ''

    Pur_Country = 'India'
    Purchaser_Name = 'State bank of india'
    createdOn = datetime.datetime.now().strftime('%d-%b-%Y')
    DupFlag = '1'
    currency = 'INR'
    Pur_URL = driver.current_url

    single_page_list.append([Tender_Notice_No, Tender_Summery, Documents_2, Purchaser_Name, actualvalue, DocFees, EMD,
     Pur_Add, Pur_Country, Pur_Email, Pur_URL, currency, TenderType, createdOn,
     remove_extra_space(Content), OpeningDate, Bid_deadline_2, DupFlag])




try:
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/ux-dialog-container/div/div/div/div[1]/div[2]')))
    button.click()
    time.sleep(0.5)
except Exception as e:
    print(f'Button error {str(e)}')
    logging.error(e)

windows_before  = driver.current_window_handle

e1 = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'au-target sha-pg001-02-menu-item']")))
e2 = e1.find_element(By.XPATH, "//div[@class = 'au-target sha-pg001-02-menu-item']")
action.move_to_element(e1).move_to_element(e2).perform()
e2.click()


WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
windows_after = driver.window_handles
new_window = [x for x in windows_after if x != windows_before][0]
driver.close()
driver.switch_to.window(new_window)


# name_img = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/form/div[2]/img[1]').get_attribute('src')
#
# link_of_img = name_img
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
# SaveImage(temp_down_path, link_of_img)
# det_text_from_img(temp_down_path)
#
# if os.path.exists(temp_down_path):
#     if len(os.listdir(temp_down_path)) != 0:
#         for i in os.listdir(temp_down_path):
#             if os.path.isdir(temp_down_path + i):
#                 shutil.rmtree(temp_down_path + i)
#             elif os.path.isfile(temp_down_path + i):
#                 os.remove(temp_down_path + i)
#     else:
#         pass
# else:
#     os.makedirs(temp_down_path)

captcha = input('Enter captcha >>>>> ')

try:
    driver.find_element(By.XPATH,'//*[@id="UserEnteredCaptcha"]').send_keys(captcha)
    driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
except Exception as e:
    print(e)


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True, stream = True)
    header = h.headers
    print(header)
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def url_response(url):
    r = requests.get(url, stream = True)
    print(r.text)
    print(r.headers)


def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d


try:
    length_of_tr = WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div[1]/div[2]/form/div[2]/table/tbody/tr")))[1:]
    for p, i in enumerate(length_of_tr):
        print(f'{page_index}.{tender_index}')
        if 'corrigendum' in str(i.text).lower() or 'corrigemdum' in str(i.text).lower():
            logging.info(f'Skip tender because of "corrigendum"')
            print('skip tender because of "corrigendum"', '\n')
            continue

        # Bid_deadline_2 = i.find_element(By.XPATH, './td[6]').text.strip().split(' ')[0]
        # print(datetime.datetime.today().year, get_year(Bid_deadline_2))
        # if datetime.datetime.today().year > get_year(Bid_deadline_2):
        #     print(f'Old tenders = {Bid_deadline_2}')
        #     logging.info(f'Skip tender because of old date = {Bid_deadline_2}')
        #     continue

        Tender_Notice_No = i.find_element(By.XPATH, './td[4]').text.strip()

        Tender_Summery = i.find_element(By.XPATH,f'./td[6]').text.strip()
        logging.info(f'Tender_Summery = {Tender_Summery}')
        print(Tender_Summery)
        Tender_Details = Tender_Summery
        # OpeningDate = i.find_element(By.XPATH,f'./td[7]').text.strip().split(' ')[0]
        sql = f"""  CREATE TABLE IF NOT EXISTS {app_name}(Id INTEGER PRIMARY KEY AUTOINCREMENT
                                                                                 ,Tender_Summery TEXT
                                                                                 ,Pur_City TEXT
                                                                                 ,Tender_Notice_No TEXT
                                                                                 ,Tender_Details TEXT
                                                                                 ,Bid_deadline_2 TEXT
                                                                                 ,Documents_2 TEXT
                                                                                 ,OpeningDate TEXT
                                                                                 ,TenderListing_key TEXT
                                                                                 ,Notice_Type TEXT
                                                                                 ,Competition TEXT
                                                                                 ,Purchaser_Name TEXT
                                                                                 ,Pur_Add TEXT
                                                                                 ,Pur_State TEXT
                                                                                 ,Pur_Country TEXT
                                                                                 ,Pur_Email TEXT
                                                                                 ,Pur_URL TEXT
                                                                                 ,Bid_Deadline_1 TEXT
                                                                                 ,Financier_Name TEXT
                                                                                 ,CPV TEXT
                                                                                 ,scannedImage TEXT
                                                                                 ,Documents_1 TEXT
                                                                                 ,Documents_3 TEXT
                                                                                 ,Documents_4 TEXT
                                                                                 ,Documents_5 TEXT
                                                                                 ,currency TEXT
                                                                                 ,actualvalue TEXT
                                                                                 ,TenderFor TEXT
                                                                                 ,TenderType TEXT
                                                                                 ,SiteName TEXT
                                                                                 ,createdOn TEXT
                                                                                 ,updateOn TEXT
                                                                                 ,Content TEXT
                                                                                 ,Content1 TEXT
                                                                                 ,Content2 TEXT
                                                                                 ,Content3 TEXT
                                                                                 ,DocFees TEXT
                                                                                 ,EMD TEXT
                                                                                 ,Tender_No TEXT
                                                                                 ,flag INT DEFAULT 1);  """
        sqlite_cursor.execute(sql)
        sqlite_connection.commit()
        sqlite_cursor.execute(f'''SELECT Tender_Summery FROM {app_name} WHERE 
        Tender_Summery = ? and Tender_Notice_No = ?''',(Tender_Summery, Tender_Notice_No))
        a = sqlite_cursor.fetchone()
        if a is None:
            try:
                driver.maximize_window()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[text() = 'Action']"))).click()
                # driver.find_element(By.XPATH, "//a[text() = 'Action']").click()
                time.sleep(1)
                # ele = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
                #     (By.XPATH, f"//a[text() = 'Show Form']")))
                # time.sleep(1)
                # ele.click()
                driver.find_element(By.XPATH, "//a[text() = 'Show Form']").click()
                first_dindow = driver.current_window_handle



                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                second_window_after = driver.window_handles[1]
                driver.switch_to.window(window_name=second_window_after)

                # second_dindow = driver.current_window_handle


                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                #     (By.XPATH, f"//table//a"))).click()
                #
                # third_window_after = driver.window_handles[2]
                # driver.switch_to.window(window_name=third_window_after)
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # scraping()
                # driver.close()
                # second_window = driver.window_handles[1]
                # driver.switch_to.window(second_window)

                try:

                    # ul = '/ROOTAPP/servlet/asl.tw.DownloadController?enc%3DQF4%2BcgQaAiwmoDLcWeACXo1NB%2BIZLc85oUraHZ4fy9aaNZ0bGFM0MHhoKAFftDm23kwH6nPGhFMQ%0D%0AWTq%2FuSxLfTIYLnVOgY5%2FOViSxz0SBP74fg8D4KMfA3SsZSzMiEOmi8zA90ZRDoPGQa%2BlkDAvJThX%0D%0A6qb2m1Pk1HLc5hnm9kM8CO6W2dJrC6JdYHO%2BySas6E1HWCX8FiF63WvT9x372brYoty4jbfKcDYh%0D%0A6Mn0NrnBwERhHvILiERGR0Hgqa4nR85DNBtwAT0Ka2VnEYr6m4TEUSlWbtTEnHTWH9ETQMxWjGr9%0D%0Alb50Qyy55j4FpRPaS%2BqPPpH1%2FpqBIU%2BlsM5GKC8tpqwGuaSunrvTq%2FBnSxX7KL81TmndXoazAwhj%0D%0A31xHvsdmLhVK%2F%2Fo4XkJgFkv6I7hc1Ueg8RZMDezrHA0WQgA%3D%26chkSum%3D0fbd7b7d2b1498241a94b8fa95a54bac7179dbf9'

                    session = requests.Session()
                    response = session.post(search_url)
                    print(session.cookies.get_dict())


                    ele = driver.find_element(By.XPATH, "//a[@class = 'download']").find_element(By.XPATH,'..').get_attribute('innerHTML')
                    ul = ele.split("adDownload('")[1].split("');return false")[0]
                    a1, a2 = ul.split('?')
                    print(a1, a2)

                    d1, d2 = driver.get_cookies()
                    co1 = d1['name'] + '=' + d1['value']
                    print(co1)
                    co2 = d2['name'] + '=' + d2['value']
                    print(co2)

                    cook = f'{co1}; {co2}'
                    print(cook)
                    print(driver.get_cookies())

                    d = session.cookies.get_dict()
                    ewq = f"JSESSIONID={d['JSESSIONID']}"
                    print(ewq)
                    h1 = f"""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: JSESSIONID=1229FE671AE5A85869AB804EE4FF6BA5.worker2; viewingTabID=1
Host: www.tenderwizard.com
Referer: https://www.tenderwizard.com/ROOTAPP/servlet/asl.tw.aac.VendorDocumentsController?enc%3DlcyEhmaDoQDnJztYoZrBaMp0mT9AEztjs%2Bc3RRZwxMvK%2FhNxEuuzvkUj%2BQLlvrj5NXivUKIGj1ta%0D%0A7Cx9XNYg8BYq%2Fq1UNxMbE4acp8TFoi3fl85T1XeWo5zZfa8v5dK1XBjMxIVs1Iz6ILiR5PMt0hPC%0D%0AyrxIGHl1Xsu02x%2FjsSFaPBoy8ppVBAlHgVmtreYyfsBniRWEn2EB5WEDo6Y29xbkjMMzt3FdxCBt%0D%0As0iFhIqag0yRrzHpEiFEo3Xlb3C8A0wcL7X9uZu8608p5SOu3dbCqTvMlB5YgcYIk3YUc%2FI%3D%26chkSum%3Deff2b4ea49b260627a43428d38c01e36a6e09892
sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: iframe
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"""

                    header = get_headers(h1)
                    header['Referer'] = 'https://www.tenderwizard.com' + ul
                    if header['Referer'] == 'https://www.tenderwizard.com' + ul:
                        print(header['Referer'])
                    print(header)

                    header['Cookie'] = cook

                    print(header)

                    r = requests.get('https://www.tenderwizard.com' + ul, headers= header, verify=True, stream=True)
                    r.raw.decode_content = True
                    with open("file_name.pdf", 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                except Exception as e:
                    print(e)
                    print('hrithik')

                logging.info(f'Documents_2 = {Documents_2}')
                single_page_list.append(single_row_list)
                print('---------- Data Scraped ----------', '\n')
                tender_index += 1
            except Exception as e:
                print(f'response ex : {e}')
                logging.error(str(e))
                logging.error(f'Tab switch Error')
        else:
            print('Data already available on sqlite')
            logging.info('Data already available on sqlite')
    tender_index = 1
    page_index += 1
    # sqlite_code(single_page_list)
    single_page_list = []

    scraping_compleated = True

except WebDriverException as wd:
    if scraping_completed_flag:
        logging.info(f'Scrap data flag = {scraping_completed_flag} so last data not removed')
    else:
        if single_page_list != []:
            del single_page_list[-1]
            print('last data deleted')
        logging.info(f'Scrap data flag = {scraping_completed_flag} so last data removed')
    print(f'webdriverexception = {str(wd)}')
    logging.error(f'{str(wd)}')
    # sqlite_code(single_page_list)
    single_page_list = []
    logging.info(f'Driver quit')
    driver.quit()

except Exception as e:
    if scraping_completed_flag:
        logging.info(f'Scrap data flag = {scraping_completed_flag} so last data not removed')
    else:
        if single_page_list != []:
            del single_page_list[-1]
            print('last data deleted')
        logging.info(f'Scrap data flag = {scraping_completed_flag} so last data removed')
    print(f'main exception = {str(e)}')
    logging.error(f'{str(e)}')
    # sqlite_code(single_page_list)
    single_page_list = []
    logging.info(f'Driver quit')
    driver.quit()

if scraping_compleated:
    logging.info(f'Scraping completed')
    logging.info(f'Driver quit')
    driver.quit()

sqlite_cursor.close()
sqlite_connection.close()

