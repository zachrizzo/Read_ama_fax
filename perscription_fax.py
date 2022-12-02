

import concurrent.futures
import concurrent.futures
from dataclasses import replace
from hashlib import new
from platform import mac_ver
from posixpath import split
from telnetlib import DO
from tkinter.messagebox import NO
from paddle import assign
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from pynput.mouse import Button, Controller
from PyPDF2 import PdfReader
import urllib.request
import os

from paddleocr import PaddleOCR, draw_ocr  # main OCR dependencies
from matplotlib import pyplot as plt  # plot images
import cv2  # opencv
from pdf2image import convert_from_path
from datetime import date ,timedelta

from sklearn.tree import export_text
today = date.today()

Images_folder_path = r'C:\Users\zachc\OneDrive - RAHEEL KHAWAJA\Desktop\AMA Automation\Perscripton\Images'
path = r"C:\Users\zachc\OneDrive - RAHEEL KHAWAJA\Desktop\AMA Automation\Perscripton\pdfs"
poppler_path = r"C:\Program Files\poppler-22.04.0\Library\bin"
os.chdir(path)
mouse = Controller()
sleep1 = time.sleep(3)
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": path,
    "downloaded.extensions_to_open": "applications/pdf",
    # savefile
    "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],

    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.open_pdf_in_system_reader": False,
    "profile.default_content_settings.popups": 0,
    # "safebrowsing.enabled": False,
    # "profile.content_settings.exceptions.automatic_downloads.*.setting": True,


})
options.add_argument("--disable-extensions")

options.add_argument('disable-component-cloud-policy')
print(options)
options.add_argument("plugins.always_open_pdf_externally")


class textfile:
    def create_text_file(new_file_name, Body_of_file):
        # "x" - Create - will create a file, returns an error if the file exist
        # "a" - Append - will create a file if the specified file does not exist
        # "w" - Write - will create a file if the specified file does not exist
        file = open(f"{new_file_name}.txt", "w")
        file.write(Body_of_file)
        file.close()
    
    def read_text_file(file_name):
        file = open(f"{file_name}.txt", "w")
        file.read()
    
    def add_to_file(file_name, stuff_to_add):
        file = open(file_name, "a")
        file.write(stuff_to_add)
        file.close()



class CheckPatient:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        
        self.action = ActionChains(self.driver)
        self.driver.get('https://azamasapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp')
        self.driver.maximize_window()
    def login(self):
        Eclinical_loging = self.driver.find_element(By.XPATH, '//*[@id="doctorID"]')
        Eclinical_loging.send_keys('zachrizzo')
        time.sleep(2)
        loging_buttom_1 = self.driver.find_element(By.XPATH, '//*[@id="nextStep"]')
        loging_buttom_1.click()
        password_2 = self.driver.find_element(By.XPATH, '//*[@id="passwordField"]')
    
        time.sleep(2)
        login_2 = self.driver.find_element(By.XPATH, '//*[@id="Login"]')
        login_2.click()
        time.sleep(8)
        # input("Press Enter to continue...")
    
    def searchPatient(self ,last_Name,first_Name,DOB):
        time.sleep(2)
        searchButton = self.driver.find_element(By.XPATH,'//*[@id="JellyBeanCountCntrl"]/div[8]/div[1]') 
        searchButton.click()
        time.sleep(4) 
        primary_name_search_box = self.driver.find_element(By.XPATH, '//*[@id="searchText"]')
        secondary_DOB_search_box = self.driver.find_element(By.XPATH ,'//*[@id="patientSearchIpt3"]')
        time.sleep(3)
        DOB_bare = DOB.replace('/','')
        primary_name_search_box.send_keys(f'{last_Name},{first_Name}')
        secondary_DOB_search_box.send_keys(DOB_bare)
        time.sleep(4)
    
        
        try:
            self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
            time.sleep(2)
            for person in range(1,10):

                try:
                    persons = self.driver.find_element(By.XPATH ,f'//*[@id="rule-table2"]/tbody/tr[{person}]')
                    time.sleep(2)
                    if persons.is_displayed():
                        try:
                            lastName = self.driver.find_element(By.XPATH, f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[4]/span')
                            firstName = self.driver.find_element(By.XPATH, f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[5]/span')
                            date_of_birth = self.driver.find_element(By.XPATH , f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[7]/span')
                            print(lastName.text.lower(), firstName.text.lower(), date_of_birth.text)
                            
                            if lastName.text.lower() == last_Name.lower() and firstName.text.lower() == first_Name.lower() and date_of_birth.text == DOB:
                                lastName.click()

                                time.sleep(4)
                            break
                        except:
                            pass
                except:
                    break
        except:
            pass
            print("couldnt find perosn")

 
    def check_encounters(self, name_of_medicine_from_fax, pharmacy_from_fax ):
        #check to see if encounter is already made
        try:
            current_provider = []
            encounters_button = self.driver.find_element(By.XPATH , '//*[@id="patient-hubUl2"]/li[7]')
            encounters_button.click()
            time.sleep(5)
            try:
                for encounters in range(1,10):
                    try:
                        encounter = self.driver.find_element(By.XPATH , f'//*[@id="Encounter-lookupTbl2"]/tbody/tr[{encounters}]')
                        encounter_date = self.driver.find_element(By.XPATH ,f'//*[@id="Encounter-lookupTbl2"]/tbody/tr[{encounters}]/td[4]')
                        provider_resources = self.driver.find_element(By.XPATH , f'//*[@id="Encounter-lookupTbl2"]/tbody/tr[{encounters}]/td[11]')
                        if not current_provider and len(provider_resources.text) >3:
                            print('empty')
                            current_provider.append(provider_resources.text)
                        print(current_provider)
                        encounter_reason = self.driver.find_element(By.XPATH , f'//*[@id="Encounter-lookupTbl2"]/tbody/tr[{encounters}]/td[13]')
                        encounter_reason_text =encounter_reason.text.lower()
                        encounter_type = self.driver.find_element(By.XPATH ,f'//*[@id="Encounter-lookupTbl2"]/tbody/tr[{encounters}]/td[7]')
                        
                        print(encounter_date.text, provider_resources.text, encounter_reason.text)
                        refill_possibilitys = ['refill', 'new refill request','med refill','refill request','refill request','refil']
                        for refill in refill_possibilitys:
                            if encounter_reason_text == refill:
                                try:
                                    encounter_date_split = encounter_date.text.split('/')
                                    new_month = int(encounter_date_split[0])
                                    print(new_month,1)
                                    if(new_month < 10):
                                        new_month_str = encounter_date_split[0].replace('0','')
                                        new_month = int(new_month_str)
                                        print(new_month,2)
                                    new_encounter_date = date(int(encounter_date_split[2]),int(new_month),int(encounter_date_split[1]))
                                    print(new_encounter_date)
                                    delta = today-new_encounter_date
                                    print(delta.days, "days")
                                    time_diff = delta.days
                                    if time_diff < 21:
                                        encounter_type.click()
                                        time.sleep(5)
                                        message_box = self.driver.find_element(By.XPATH ,'//*[@id="savePrompt-tplBtn1"]')
                                        action_taken_box = self.driver.find_element(By.XPATH ,'//*[@id="actionTextArea"]')
                                        close_button = self.driver.find_element(By.XPATH ,'//*[@id="savePrompt-tplBtn1"]')
                                        time.sleep(1)
                                        if message_box.text.lower() == name_of_medicine_from_fax.lower():
                                            print('its a duplicate')
                                            close_button.click()
                                            time.sleep(2)
                                    else:
                                        encounter_close_button = self.driver.find_element(By.XPATH ,'//*[@id="Encounter-lookupBtn1"]')
                                        encounter_close_button.click()
                                        time.sleep(2)
                                        self.new_encounter(last_provider=current_provider[0] ,meds=name_of_medicine_from_fax,pharmacy_from_fax=pharmacy_from_fax )
                                        break
                                except Exception as e:
                                    print(e)
                        else:
                            continue
                        break
                                        





                        # if encounter_reason_text == 'refill' or encounter_reason_text == 'new refill request' or encounter_reason_text == 'med refill' or encounter_reason_text == 'medrefill' or encounter_reason_text == 'refill request' or encounter_reason_text == 'refil':
                        
                    except:
                        break
               
                  
               
            except:
                print('no encounters found')
        except Exception as e:
            print(e)

            
    def check_refill(self, name_of_medicine_from_fax, pharmacy_from_fax):
        time.sleep(2)
        RX = self.driver.find_element(By.XPATH ,'//*[@id="patient-hubUl2"]/li[9]')
        RX.click()
        time.sleep(3)
        try:
            for prescription in range(10):
                try:
                    time.sleep(2)
                    name_of_medicine = self.driver.find_element(By.XPATH, f'//*[@id="RxSummary_HubTbl2ngR{prescription}"]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div[1]').text
                    print(name_of_medicine)
                    date_last_processed  = self.driver.find_element(By.XPATH, f'//*[@id="RxSummary_HubTbl2ngR{prescription}"]/tbody/tr/td/table/tbody/tr/td[3]/div/div/div/span').text                           
                    print(date_last_processed)
                    date_last_processed_simplified_to_days = date_last_processed.split('-')
                    print('3')
                    date_last_processed_number_string = date_last_processed_simplified_to_days[2].split('d')
                    print(date_last_processed_number_string)
                    date_last_processed_number_number = int(date_last_processed_number_string[0])

                    print(date_last_processed_number_number)
                    if name_of_medicine == name_of_medicine_from_fax:
                        if date_last_processed_number_number > 22 and date_last_processed_number_number <= 35 and date_last_processed_number_number<36  or date_last_processed_number_number >= 51 and date_last_processed_number_number <= 65 and date_last_processed_number_number <66 or date_last_processed_number_number >= 81 and date_last_processed_number_number <=95 and date_last_processed_number_number<96:
                            close_button = self.driver.find_element(By.XPATH, '//*[@id="rxSummaryXBtn"]')
                            close_button.click()
                            time.sleep(3)
                            self.check_encounters(name_of_medicine_from_fax =name_of_medicine_from_fax)                             
                            break

                        else:
                            print('this is a duplicate')
                            break
                    else:
                        close_button = self.driver.find_element(By.XPATH, '//*[@id="rxSummaryXBtn"]')
                        close_button.click()
                        self.check_encounters(name_of_medicine_from_fax=name_of_medicine_from_fax, pharmacy_from_fax=pharmacy_from_fax)
                        break
                except Exception as  e:
                    print(e)
                    print('prescription dosent exsist')
                    
                    self.check_encounters(name_of_medicine_from_fax=name_of_medicine_from_fax, pharmacy_from_fax=pharmacy_from_fax)
                    break
        except Exception as e:
            print(e)
            print('there was a problem')



    def new_encounter(self, last_provider:str,meds:str ,pharmacy_from_fax:str):
        provider_list = ["BALLARD,DANIEL R","DAUSCHA,ASHLEE", "KEESEE,RANDI N",'KHAN,HASSAN M', "LEIFSON,BRETT LEE","NADIR,Ehreema", "Omole,Oluwaseun"]
        new_tel_encounter = self.driver.find_element(By.XPATH ,'//*[@id="patient-hubBtn13"]')
        new_tel_encounter.click()
        time.sleep(1)
        cancel_pop_ip_button = self.driver.find_element(By.XPATH , '//*[@id="billingAlertBtn6"]')
        cancel_pop_ip_button.click()
        time.sleep(3)
        try:
            caller_input = self.driver.find_element(By.XPATH ,'//*[@id="JellyBeanT-Telephone-Encounter-DetailViewIpt2"]')
            reason_input = self.driver.find_element(By.XPATH ,'//*[@id="dv"]')
            assign_to = self.driver.find_element(By.XPATH ,'//*[@id="staff-lookup_telenc_assignedTolookup_Ipt1"]')
            assign_button = self.driver.find_element(By.XPATH , '//*[@id="staff-lookup_telenc_assignedTolookup_Btn2"]')
            
            pharmacy =self.driver.find_element(By.XPATH ,'//*[@id="JellyBeanT-Telephone-Encounter-DetailViewBtn2"]')
            pharmacy_button = self.driver.find_element(By.XPATH, '//*[@id="JellyBeanT-Telephone-Encounter-DetailViewBtn2"]')
            message_input_box = self.driver.find_element(By.XPATH ,'//*[@id="messageTextArea"]')
            caller_input.send_keys('fax')
            reason_input.send_keys('refill')
            assign_to.clear()
            time.sleep(2)
            
            pharmacy_button.click()
            time.sleep(2)
            address_dropdown= self.driver.find_element(By.XPATH, '//*[@id="docPharmaDetailsDropDwn"]')
            address_dropdown.click()
            time.sleep(.5)
            address_option = self.driver.find_element(By.XPATH , '//*[@id="docPharmaDetailsDropDwn"]/option[10]')
            address_option.click()
            address_search = self.driver.find_element(By.XPATH , '//*[@id="docPharmaDetailsText"]')
            address_search.send_keys(pharmacy_from_fax)
            option_address = self.driver.find_element(By.XPATH , '//*[@id="1128"]/td[9]')
            item_check = self.driver.find_element(By.XPATH , '//*[@id="docId"]')
            if option_address.text == pharmacy_from_fax:
                item_check.click()
            select = self.driver.find_element(By.XPATH , '//*[@id="linkingPharmacyBtn7"]')
            time.sleep(.5)
            select.click()

            

            assign_button.click()
            time.sleep(3)
            try:
                staff_search = self.driver.find_element(By.XPATH ,'//*[@id="staffName"]')
                for found_providers in provider_list:
                    print(last_provider,'last')
                    print('list', found_providers)
                    if last_provider.lower().find(found_providers.lower()) != -1:
                        time.sleep(2)
                        staff_search.send_keys(found_providers)
                        provider_select = self.driver.find_element(By.XPATH , '//*[@id="StaffLookupModalBtn6"]')
                        provider_select.click()
                        break
            except Exception as e:
                print(e)
                print('error with assigning providers')
            time.sleep(2)
            message_input_box.send_keys(meds)
            time.sleep(5)
            submit_encounter = self.driver.find_element(By.XPATH , '//*[@id="JellyBeanT-Telephone-Encounter-DetailViewBtn28"]')
            #submit_encounter.click()
            print('done DONE')
        except Exception as e:
            print(e)
            print('error with encounter')
                                                                                        
        

            
            
            

            


        except Exception as e:
            print(e)



       







class DownloadAndReadFax:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        
        self.action = ActionChains(self.driver)
        self.driver.get('https://azamasapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp')
        self.driver.maximize_window()
        
        self.pdf_count = 0
        self.Sender_fax_number = []
        self.CVS_fax_numbers = ['8007467287']
        self.frys_farmacy_fax_numbers = ['4807828695','4807529700','480566881']
        self.walgreens_fax_numbers =['4809884326']




    def extract_pdf():
        reader = PdfReader(
            '/Users/zachrizzo/Desktop/Automation for AMA/Z. Rizzo MAAD Paystubs.pdf')
        page = reader.pages[0]
        print('ji')
        print(page.extract_text())


    def expand_root_element(element, self):
        shadow = self.driver.execute_script("return arguments[0].shadowRoot", element)
        return shadow


    def download_file(download_url, filename):
        response = urllib.request.urlopen(download_url)
        file = open(filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()


    def login(self):
        Eclinical_loging = self.driver.find_element(By.XPATH, '//*[@id="doctorID"]')
        Eclinical_loging.send_keys('zachrizzo')
        time.sleep(2)
        loging_buttom_1 = self.driver.find_element(By.XPATH, '//*[@id="nextStep"]')
        loging_buttom_1.click()
        password_2 = self.driver.find_element(By.XPATH, '//*[@id="passwordField"]')
        password_2.send_keys('Karen013074!')
        time.sleep(2)
        login_2 = self.driver.find_element(By.XPATH, '//*[@id="Login"]')
        login_2.click()
        time.sleep(8)
        # input("Press Enter to continue...")


    def navigate_To_Documents(self):
        menu_item = self.driver.find_element(
            By.XPATH, '//*[@id="jellybean-panelLink4"]')
        menu_item.click()
        time.sleep(1)
        Doc_tab = self.driver.find_element(By.XPATH, '//*[@id="jcarousel2"]/ul/li[8]')
        Doc_tab.click()
        time.sleep(1)
        fax_inbox = self.driver.find_element(
            By.XPATH, '//*[@id="jcarousel2"]/ul/li[8]/div/div[1]/ul/li[3]/a/span[2]')
        fax_inbox.click()
        time.sleep(1)
        inbox_folder = self.driver.find_element(By.XPATH, '//*[@id="faxInboxBtn1"]')
        inbox_folder.click()
        time.sleep(1.5)
        chandler_inbox = self.driver.find_element(
            By.XPATH, '//*[@id="rule-table1"]/tbody/tr[2]/td')
        chandler_inbox.click()
        time.sleep(.5)
        ok_button = self.driver.find_element(By.XPATH, '//*[@id="faxInboxMapBtn2"]')
        ok_button.click()


    def Download_one_doc(self, starting_page:int, starting_doc_number):
        max_page_number = self.driver.find_element(By.XPATH , '//*[@id="faxInBoxApp"]/div[2]/div/div[1]/div[3]/div[3]/div[3]/div/div[1]/i/strong/span[4]').text
        next_page_button = self.driver.find_element(By.XPATH , '//*[@id="faxInboxBtn5"]')
        if starting_doc_number == None:
            starting_doc_number:1
        file_count = -1
        if starting_page != 1:
            max_page_number_int = int(max_page_number)-starting_page   
            for page in range(1,abs(starting_page)):
                time.sleep(2)
                next_page_button.click()
        else:

            max_page_number_int = int(max_page_number)+1

        for page in range(1, abs(max_page_number_int)+1 ):
            docs_list = []
            url_list = []
            number_of_docs = self.driver.find_element(By.XPATH ,'//*[@id="faxInBoxApp"]/div[2]/div/div[1]/div[3]/div[3]/div[3]/div/div[1]/i/strong/span[1]').text
            for i in range(starting_doc_number, int(number_of_docs)+1):
                try:
                    doc = self.driver.find_element(
                        By.XPATH, f'//*[@id="demotable"]/tbody/tr[{i}]')
                    sender_Fax_number= self.driver.find_element(By.XPATH,f'//*[@id="demotable"]/tbody/tr[{i}]/td[3]/span')
                                                                            
                    if doc.is_displayed():
                        docs_list.append(doc)
                        self.Sender_fax_number.append(sender_Fax_number.text)
                    else:
                        pass
                except Exception as e:
                    print(e)
                    input('hit Enter')

            for i in docs_list:
                self.action\
                    .scroll_to_element(i)\
                    .perform()
                time.sleep(.1)
                try:
                    i.click()
                except:
                    time.sleep(10)
                    i.click()
                
                iframe = self.driver.find_element(By.CSS_SELECTOR, '#iframeDocView')
                pdfUrl = iframe.get_attribute("src")
                #url_list.append(pdfUrl)

                time.sleep(1)
                self.driver.switch_to.new_window('tab')
                self.driver.switch_to.window(self.driver.window_handles[1])
                
               
                self.driver.get(pdfUrl)
                    
                time.sleep(3)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(2)
                self.pdf_count += 1
                self.ReadAndOrganizeOneDoc(pdf_count=self.pdf_count, file_count=file_count, fax_number=i)
            next_page_button = self.driver.find_element(By.XPATH , '//*[@id="faxInboxBtn5"]')
            try:
                next_page_button.click()
            except:
                pass
            time.sleep(2)
            
    def ReadAndOrganizeOneDoc(self, pdf_count, file_count,fax_number):
        
        
        #rename as pdf
        for file in os.listdir():
            
            if  ".pdf" not in file:
                if f"pdf{pdf_count}.pdf" not in os.listdir():
                    os.rename(file, f'pdf{pdf_count}.pdf')
                    # time.sleep(.5)
                else:
                    pdf_count += 1
                    os.rename(file, f'pdf{pdf_count}.pdf')
                    # time.sleep(.5)
        #read each pdf and change to jpg, then put in separate folders
        
        for file in os.listdir():
            
            cvs_possibilities = ['cvs', 'cvs pharmacy','cvs/pharmacy']
            pages_array = []
            pages = 0
            file_count += 1
            # print(file)
            #create folder name
            file_name = file.split('.')
            new_directory = f"{file_name[0]}"
            single_pdf_folder = os.path.join(Images_folder_path , new_directory)
            os.chdir(Images_folder_path)
            if new_directory in os.listdir():
                # print('it exists')
                pass
            else:
                os.chdir(path)
                #makes new folder
                os.mkdir(single_pdf_folder)
                #converts Image 
                images = convert_from_path(pdf_path=file,dpi=300,  poppler_path=poppler_path)
                os.chdir(single_pdf_folder)
                
                for i in range(len(images)):

                    # Save pages as images in the pdf
                    images[i].save('page' + str(i+1) + '.jpg', 'JPEG')

                #read Image and extract Text 
                set_simon_med = None
                set_exam = None
                set_Lastname = None
                set_Firstname = None
                set_dob = None
                set_order_type =None
                set_found_patient = False
                set_diagnostic_report =None
                set_see_tomorrow_today = None
                set_from_simon_med = None
                set_provider = None

                for file in os.listdir():
                    pages += 1
                    pages_array.append(pages)
                    ocr_model = PaddleOCR(lang='en' )
                    # ocr_model = PaddleOCR(lang='en' )
                    # for file in os.listdir():
                    result = ocr_model.ocr(file)

                    all_text = []
                    
                    
                    number_box= 0
                    text = [res[1][0] for res in result]
                    
                    score = [res[1][1] for res in result]
                        
                    box = [res[0] for res in result]
                    
                    
                    # textfile.create_text_file(new_file_name=f'{file_name[0]}' , Body_of_file= f'  page {pages}: \n {text} '   )
                    for boxs,texts in result:
                            
                            # print(f'{number_box}.{texts} at {box[number_box]}')
                            # print ('found request')
                            
                            scores = int(texts[1])
                            simple_text= texts[0].lower().replace(' ','')
                            
                            textfile.add_to_file(file_name=f'{file_name[0]}.text', stuff_to_add=f'\n {number_box}.{texts[0]} ===== {scores}      ----------------------{boxs} ')
                            # for p in cvs_possibilities:
                            #     # print(texts.lower().replace(' ',''))
                            #     # print(p.lower().replace(' ',''))
                            #     is_text_found =simple_text.find(p.lower().replace(' ',''))

                            #     if is_text_found != -1 and scores > 70:
                            #         print(texts[0].lower().replace(' ',''))
                            #         print(p.lower().replace(' ',''))
                            #         print('------------------Found====================================== ')
                            is_simon_med_found = simple_text.find('simonmed')
                            is_exam = simple_text.find('exam')
                            if set_found_patient ==False:
                                is_patient =simple_text.find("patient")
                            is_diagnostic_report = simple_text.find('iagnosticimagingreport')
                            is_see_tomorrow_today = simple_text.find('seetomorrowtoday')
                            is_from_simnon_med = simple_text.find('fromsimonmed')

                            if is_exam != -1:
                                set_exam = 'exam'
                            if is_simon_med_found != -1:
                                # find patient name
                                print('simon Med')
                                set_simon_med='simonmed'
                            if is_diagnostic_report != -1:
                                set_diagnostic_report='diagnostic_report'

                            if is_see_tomorrow_today != -1:
                                set_see_tomorrow_today = 'see_tomorrow_today'
                            if is_from_simnon_med != -1:
                                set_from_simon_med = 'fromsimonMed'
                            
                            
                            # if set_found_patient == True:

                            #     self.is_simon_med(set_from_simon_med=set_from_simon_med, is_patient=is_patient,fax_number=fax_number,texts=texts[0],simple_text=simple_text,set_see_tomorrow_today=set_see_tomorrow_today,set_diagnostic_report=set_diagnostic_report,set_found_patient=set_found_patient,set_order_type=set_order_type,set_dob=set_dob,set_Firstname=set_Firstname,set_Lastname=set_Lastname,set_exam=set_exam,set_simon_med=set_simon_med)
                            # if is_patient != -1 and set_simon_med != None  and set_from_simon_med != None:
                            #     set_found_patient = True          
                            
                            if set_simon_med != None and  set_found_patient==True and set_Lastname == None and set_from_simon_med != None:

                                try:
                                    
                                    [lastname, firstname, sex, sex_type, dob, date_of_birth_full, age, age_number ] =texts[0].split(' ')
                                except:
                                    try:
                                        [lastname, firstname, sex, sex_type, dob, date_of_birth_full,  age_number ] =texts[0].split(' ')
                                    except:
                                        try:
                                            [rest_of_sting,  age_number ] =texts[0].split('Age')
                                            
                                            [name_and_sex,date_of_birth_full] = rest_of_sting.split('DOB')
                                            
                                            [fullName, sex] = name_and_sex.split('Sex')
                                            fullName = fullName.strip()
                                            try:
                                                [lastname, firstname] = fullName.split(' ')
                                            except:
                                                 [lastname, firstname, middle_name] = fullName.split(' ')
                                        except Exception as e:
                                            
                                            print(e)
                                            continue
                                #fix DOB
                                # if str(date_of_birth_full).index('1',1,3) == 2 and str(date_of_birth_full).index('1',4,6) == 5 and len(str(date_of_birth_full)) == 10: 
                                #     date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
                                # elif str(date_of_birth_full).index('1',1,3) == 2  and len(str(date_of_birth_full)) == 9:
                                #     date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
                                # elif str(date_of_birth_full).index('1',4,6) == 5  and len(str(date_of_birth_full)) == 9:
                                #     date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/'+date_of_birth_full[2] + date_of_birth_full[3]  + '/'+ date_of_birth_full[4] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] 
                              
                                date_of_birth_full = self.fix_DOB(date_of_birth_full=date_of_birth_full)
                                print(date_of_birth_full)
                                set_Lastname =lastname
                        
                            if is_patient != -1 and set_found_patient == False:
                                set_found_patient = True  
                        
                        
                            if set_simon_med != None and  set_exam != None and set_found_patient==True and set_order_type == None:
                                try:
                                    text_lower =texts[0].lower()
                                    if text_lower.find('/') != -1:
                                        text_lower = text_lower.replace('/','')
                                    [exam,exam_number_line] = texts[0].lower().split('h',1)
                                    #correcting for extra spaces
                                    # scount = 0
                                    # for i in exam_number_line:
                                    #     if(i.isspace()):
                                    #         scount=scount+1
                                    
                                    # if scount > 4:
                                        
                                        
                                    #     [exam_number, date,time,order_type] = exam_number_line.split(' ',5)
                                    #     try:
                                    #         order_type =order_type.replace(' ','')
                                    #     except:
                                    #         pass
                                    
                                    #     try:
                                    #         order_type =order_type.replace(' ','')
                                    #     except:
                                    #         pass
                                    #     try:
                                    #         order_type =order_type.replace(' ','')
                                    #     except:
                                    #         pass
                                    # else:
                                    #     [exam_number, date,time,order_type] = exam_number_line.split(' ')
                                    try:
                                        try:
                                            for i in range(9):
                                                [orderNumber_and_date_time,orderType] = exam_number_line.split(f'{i}pm',1)
                                            
                                        except:
                                            for i in range(9):
                                            
                                                [orderNumber_and_date_time,orderType] = exam_number_line.split(f'{i}am', 1)

                                    except:
                                        try:
                                            [orderNumber_and_date_time,orderType] = exam_number_line.split(' am', 1)
                                        except:
                                            try:
                                                [orderNumber_and_date_time,orderType] = exam_number_line.split(' pm', 1)
                                            except:
                                                try:
                                                    [orderNumber_and_date_time,orderType] = exam_number_line.split('pm', 1)
                                                except:
                                                    try:
                                                        [orderNumber_and_date_time,orderType] = exam_number_line.split('am', 1)
                                                    
                                                    except:
                                                        pass

                                        order_type=orderType.replace(' ','')
                                        [exam_number, date, time] = orderNumber_and_date_time.split(' ')
                                    
                                    new_exam_number = self.replace_letters_in_a_number_string(exam_number)
                                    set_exam = exam_number
                                    set_order_type =order_type
                                    print(exam_number,date,time,order_type)
                                    if self.searchPatient(last_Name=lastname,first_Name=firstname,DOB=date_of_birth_full):
                                    
                                        self.check_for_duplicate(first_name=firstname,last_name=lastname ,dob=date_of_birth_full ,fax_number=fax_number, Exam_number=new_exam_number, order_type_from_fax=order_type)
                                    else:
                                        print('couldnt find patient continuing ')
                                except:
                                    continue
                            number_box +=1



            #go back to original directory
            os.chdir(path)
    
    def fix_DOB(self,date_of_birth_full):
    
        # try:
            date_of_birth_full = str(date_of_birth_full).strip()
            print(str(date_of_birth_full).find('1',1,3))
            print(str(date_of_birth_full).find('1',4,6))
            print(len(str(date_of_birth_full)))
            #add an algorthom for dates with a like 057241956 it comes out to 5/72/4956 so fix this zach
            #KEEP TRYING
            if str(date_of_birth_full).find('7',1,3) != -1  and str(date_of_birth_full).find('4',4,6) != -1 and len(str(date_of_birth_full)) == 10: 
                date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
            elif str(date_of_birth_full).find('4',1,3) != -1  and str(date_of_birth_full).find('7',4,6) != -1 and len(str(date_of_birth_full)) == 10: 
                date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
            elif str(date_of_birth_full).find('7',1,3) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
            elif str(date_of_birth_full).find('4',1,3) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
            


            elif str(date_of_birth_full).find('1',1,3) != -1  and str(date_of_birth_full).find('1',4,6) != -1 and len(str(date_of_birth_full)) == 10: 
                date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
            elif str(date_of_birth_full).find('1',1,3) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
            elif str(date_of_birth_full).find('1',4,6) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/'+date_of_birth_full[2] + date_of_birth_full[3]  + '/'+ date_of_birth_full[4] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] 
       
            elif str(date_of_birth_full).find('7',1,3) != -1 and str(date_of_birth_full).find('7',4,6) != -1 and len(str(date_of_birth_full)) == 10: 
                date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
            elif str(date_of_birth_full).find('7',1,3) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
            elif str(date_of_birth_full).find('7',4,6) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/'+date_of_birth_full[2] + date_of_birth_full[3]  + '/'+ date_of_birth_full[4] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] 
       
            elif str(date_of_birth_full).find('4',1,3) != -1 and str(date_of_birth_full).find('4',4,6) != -1 and len(str(date_of_birth_full)) == 10: 
                date_of_birth_full=date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] + date_of_birth_full[9]
            elif str(date_of_birth_full).find('4',1,3) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/' + date_of_birth_full[3] + date_of_birth_full[4] + '/' +date_of_birth_full[5] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8]  
            elif str(date_of_birth_full).find('4',4,6) != -1  and len(str(date_of_birth_full)) == 9:
                date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/'+date_of_birth_full[2] + date_of_birth_full[3]  + '/'+ date_of_birth_full[4] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] 
        # except:
        #     pass
            return date_of_birth_full
        

    def replace_letters_in_a_number_string(self,string:str):
        new_string = string

        try:
                                    
            if string.isdigit():
                pass
            else:
                try:
                   new_string= string.replace('z','2')
                except:
                    pass
                try:
                    new_string = string.replace('l','1')
                except:
                    pass
                try:
                    new_string = string.replace('s','5')
                except:
                    pass

        except:
            pass

        return new_string

            
    # def is_simon_med(self,is_patient, simple_text, texts,set_from_simon_med, fax_number, set_see_tomorrow_today,set_diagnostic_report,set_found_patient,set_order_type,set_dob,set_Firstname,set_Lastname,set_exam,set_simon_med):
        
        
        
        
        
       


    
    def searchPatient(self ,last_Name,first_Name,DOB):
        time.sleep(2)
        searchButton = self.driver.find_element(By.XPATH,'//*[@id="JellyBeanCountCntrl"]/div[8]/div[1]') 
        searchButton.click()
        time.sleep(4) 
        primary_name_search_box = self.driver.find_element(By.XPATH, '//*[@id="searchText"]')
        secondary_DOB_search_box = self.driver.find_element(By.XPATH ,'//*[@id="patientSearchIpt3"]')
        time.sleep(3)
        DOB_bare = DOB.replace('/','')
        primary_name_search_box.send_keys(f'{last_Name},{first_Name}')
        secondary_DOB_search_box.send_keys(DOB_bare)
        time.sleep(4)
    
        
        try:
            self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
            time.sleep(2)
            self.check_if_patient_is_found()
            
        except:
            
            print("couldn't find person searching for variation")
            primary_name_search_box.clear()
            primary_name_search_box.send_keys(last_Name)
            try: 
                #try to remove first name
                print(' removing first name')
                time.sleep(2)
                self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
                time.sleep(.5)
                self.check_if_patient_is_found(last_Name=last_Name,first_Name=first_Name,DOB=DOB)
                return True
            except:
                print("searching by date only")
                #try only birthdate
                primary_name_search_box.clear()
                try:
                    self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
                    time.sleep(.5)
                    self.check_if_patient_is_found(last_Name=last_Name,first_Name=first_Name,DOB=DOB)
                    return True
                except:
                    print('trying by full name only')
                    #try only name
                    primary_name_search_box.clear()
                    secondary_DOB_search_box.clear()
                    primary_name_search_box.send_keys(f'{last_Name},{first_Name}')
                    
                    try:
                        self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
                        time.sleep(.5)
                        self.check_if_patient_is_found(last_Name=last_Name,first_Name=first_Name,DOB=DOB)
                        return True
                    except:
                            print('trying to search with last name only')
                            primary_name_search_box.clear()
                            primary_name_search_box.send_keys(f'{last_Name}')
                            try:
                                self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
                                time.sleep(.5)
                                self.check_if_patient_is_found(last_Name=last_Name,first_Name=first_Name,DOB=DOB)
                                return True
                            except:
                                print('tring search with first name only')
                                primary_name_search_box.clear()
                                primary_name_search_box.send_keys(f',{first_Name}')
                                try:
                                  
                                    self.driver.find_element(By.XPATH ,'//*[@id="rule-table2"]/tbody/tr[1]')
                                    time.sleep(.5)
                                    self.check_if_patient_is_found(last_Name=last_Name,first_Name=first_Name,DOB=DOB)
                                    return True
                                except:
                                    print('cant find patient, continuing doc reading')
                                    close_patient_search = self.driver.find_element(By.XPATH ,'//*[@id="patientSearchBtn1"]')
                                    close_patient_search.click()
                                    return False

                                
                    
    def check_if_patient_is_found(self, last_Name:str,DOB:str, first_Name:str):
        for person in range(1,10):

                try:
                    persons = self.driver.find_element(By.XPATH ,f'//*[@id="rule-table2"]/tbody/tr[{person}]')
                    time.sleep(2)
                    if persons.is_displayed():
                        try:
                            lastName = self.driver.find_element(By.XPATH, f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[4]/span')
                            firstName = self.driver.find_element(By.XPATH, f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[5]/span')
                            date_of_birth = self.driver.find_element(By.XPATH , f'//*[@id="rule-table2"]/tbody/tr[{person}]/td[7]/span')
                            print(lastName.text.lower(), firstName.text.lower(), date_of_birth.text)
                            is_last_name = last_Name.lower().find(lastName.text.lower())
                            is_first_name = first_Name.lower().find(firstName.text.lower())

                            if is_first_name != -1 and is_last_name != -1 and  date_of_birth.text == DOB:
                                lastName.click()
                                
                                time.sleep(4)
                            break
                        except:
                            print('person did not match, trying different match equation')
                            # try:
                            #     if 
                except:
                    break

    def check_for_duplicate(self, dob, first_name, last_name, order_type_from_fax:str,Exam_number, fax_number ):
       
        time.sleep(3)
        DI_tab = self.driver.find_element(By.XPATH, '//*[@id="patient-hubUl2"]/li[2]')
        DI_tab.click()
        time.sleep(2)
        for orders in range(2,100):
            try:

                order = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[{orders}]')
                
                if order.is_displayed():
                    name_of_imaging_order = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[{orders}]/tr[1]/td[12]').text

                    order_type_from_fax_simple = order_type_from_fax.lower().replace(' ','')

                    name_of_imaging_order_simple = name_of_imaging_order.lower().replace(' ','')
                    print(name_of_imaging_order_simple)
                    if name_of_imaging_order_simple.find('-') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace('-','')
                
                    if name_of_imaging_order_simple.find('/') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace('/','')
                    if name_of_imaging_order_simple.find(':') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace(':','')
                    if name_of_imaging_order_simple.find(',') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace(',','')
                    
                    is_order_found = order_type_from_fax_simple.find(name_of_imaging_order_simple)
                    is_reverse_order_found = name_of_imaging_order_simple.find(order_type_from_fax_simple)
                    #the order should alwase be found
                    if is_order_found != -1 or is_reverse_order_found != -1:
                        try:
                            try:
                                #try gray paper-clip
                                paper_clip = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[{orders}]/tr[1]/td[7]/div')
                                paper_clip.click()
                                time.sleep(2)
                                #download uploaded Image order
                                
                                if self.read_imaging(fax_exam_number=Exam_number):
                                    #if found close and delete fax
                                    print('deleting')
                                    close1 = self.driver.find_element(By.XPATH, f'//*[@id="savePrompt-tplBtn1"]')
                                    close1.click()
                                    time.sleep(1)
                                    close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                                    close2.click()
                                    time.sleep(1)
                                    close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                                    close3.click()
                                    time.sleep(1)   
                                    delete_fax = self.driver.find_element(By.XPATH, f'//*[@id="demotable"]/tbody/tr[3]/td[5]/div/i')
                                    break
                                else:
                                    print('not in gray, trying red')
                            except:
                                pass

                            #if not found in gray try red paperclip
                            try:
                                red_paper_clip = self.driver.find_element(By.XPATH ,'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[3]/tr[1]/td[6]/div/i')
                                red_paper_clip.click()    
                                exam_number_red_paper_clip = self.driver.find_element(By.XPATH ,'//*[@id="pinkPaperClipTbl12ngR0"]/tbody/tr[2]/td/pre')

                                if exam_number_red_paper_clip.is_displayed():
                                    exam_simple =  exam_number_red_paper_clip.text.lower().replace(' ','')
                                    [exam, exam_number] =exam_simple.split('#')
                                    only_exam_number=exam_number.split('-')
                                   
                                    

                                    
                                
                                    
                                    if only_exam_number[0] == Exam_number:
                                        #if found close and delete fax
                                        red_paperclipClose = self.driver.find_element(By.XPATH, '//*[@id="pinkPaperClipModalBtn1"]')
                                        red_paperclipClose.click()
                                        close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                                        close2.click()
                                        time.sleep(1)
                                        close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                                        close3.click()
                                        time.sleep(1)   
                                        delete_fax = self.driver.find_element(By.XPATH, f'//*[@id="demotable"]/tbody/tr[3]/td[5]/div/i')
                                        break
                                    else:
                                        time.sleep(1)
                                        close1 = self.driver.find_element(By.XPATH, f'//*[@id="pinkPaperClipModalBtn1"]')
                                        close1.click()
                                        close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                                        close2.click()
                                        close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                                        close3.click()
                                        print('the exam numbers dont match, trying the next order')
                                        continue

                                   



                                else:
                                    print('no red paper clip')

                                    # else:
                                    #     close1 = self.driver.find_element(By.XPATH, f'//*[@id="savePrompt-tplBtn1"]')
                                    #     close1.click()
                                    #     time.sleep(1)
                                    #     close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                                    #     close2.click()
                                    #     time.sleep(1)
                                    #     close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                                    #     close3.click()
                                    #     time.sleep(1)
                                    #     self.add_to_patient()
                                    #     break

                            except:

                                time.sleep(1)
                                close2 = self.driver.find_element(By.XPATH, f'//*[@id="pinkPaperClipModalBtn1"]')
                                close2.click()
                                time.sleep(1)
                                close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                                close3.click()
                                time.sleep(1)
                                self.add_to_patient(firstname=first_name, lastname=last_name ,dob=dob)
                                print("no red paper_clip")
                                break  

                    


                           

                            

                        except:
                            time.sleep(2)
                            close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                            close2.click()
                            time.sleep(1)
                            close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                            close3.click()
                            time.sleep(1)
                            self.add_to_patient()
                            break

                


            except:
                
                print('no orders found')
                
                close2 = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProHistoryBtn1"]')
                close2.click()
                close3 = self.driver.find_element(By.XPATH, f'//*[@id="patient-hubBtn1"]')
                close3.click()
                time.sleep(1)
                break
               
    
    def download_Imaging(self):
        os.chdir(r'C:\Users\zachc\OneDrive - RAHEEL KHAWAJA\Desktop\AMA Automation\Perscripton\Imaging_orders_pdfs')
        #download uploaded Image order
        iframe = self.driver.find_element(By.XPATH, f'//*[@id="viewframedoc"]')
        pdfUrl = iframe.get_attribute("src")
        time.sleep(1)
        self.driver.switch_to.new_window('tab')
        self.driver.switch_to.window(self.driver.window_handles[1])
        
    
        self.driver.get(pdfUrl)
            
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(2)

    def read_imaging(self, fax_exam_number):
        for file in os.listdir():
            
            cvs_possibilities = ['cvs', 'cvs pharmacy','cvs/pharmacy']
            pages_array = []
            pages = 0
            
            print(file)
            #create folder name
            file_name = file.split('.')
            new_directory = f"{file_name[0]}"
            single_pdf_folder = os.path.join(Images_folder_path , new_directory)
            os.chdir(r'C:\Users\zachc\OneDrive - RAHEEL KHAWAJA\Desktop\AMA Automation\Perscripton\Imaging_orders_pdfs\Imagin_order_image')
            
            #converts Image 
            images = convert_from_path(pdf_path=file,dpi=300,  poppler_path=poppler_path)
            
            
            for i in range(len(images)):

                # Save pages as images in the pdf
                images[i].save('page' + str(i+1) + '.jpg', 'JPEG')

            #read Image and extract Text 
            for file in os.listdir():
                pages += 1
                pages_array.append(pages)
                ocr_model = PaddleOCR(lang='en' )
                # ocr_model = PaddleOCR(lang='en' )
                # for file in os.listdir():
                result = ocr_model.ocr(file)

                all_text = []
                
                
                number_box= 0
                text = [res[1][0] for res in result]
                
                score = [res[1][1] for res in result]
                    
                box = [res[0] for res in result]
                
                
                # textfile.create_text_file(new_file_name=f'{file_name[0]}' , Body_of_file= f'  page {pages}: \n {text} '   )
                for boxs,texts in result:
                        
                        # print(f'{number_box}.{texts} at {box[number_box]}')
                        # print ('found request')
                        
                        scores = texts[1]
                        simple_text= texts[0].lower().replace(' ','')
                        
                        
                        if simple_text.find(fax_exam_number) != -1:
                            print('its a dubble')
                            return True 
                        else:
                            
                            return False

                        

                                
                       
                            
                #go back to original directory
                os.chdir(path)
                time.sleep(.5)




    def add_to_patient(self,dob, lastname, firstname,order_type_from_fax,provider ):
        print('adding to patient')
        add_to_patient_button =self.driver.find_element(By.XPATH ,'//*[@id="faxInboxBtn3"]')
        add_to_patient_button.click()
        time.sleep(1)
        search_type = self.driver.find_element(By.XPATH ,'//*[@id="searchPtBtn"]')
        search_type.click()
        time.sleep(.5)
        DOB_type = self.driver.find_element(By.XPATH ,'//*[@id="patient-lookupUl2"]/li[3]')
        DOB_type.click()
        time.sleep(2)
        search_box = self.driver.find_element(By.XPATH ,'//*[@id="ptLookup"]')  
        DOB_bare = dob.replace('/','')
        search_box.send_keys(DOB_bare)
        time.sleep(2)
        for patients in range(1,20):
            try:
                name = self.driver.find_element(By.XPATH ,f'//*[@id="patient-lookupUl1"]/li[{patients}]/div[1]/div/h4/span[1]')
                DOB = self.driver.find_element(By.XPATH ,f'//*[@id="patient-lookupUl1"]/li[{patients}]/div[1]/div/p/span[5]')
                [fullname,age] = name.split('(')
                if fullname.lower().replace(' ','').find(firstname) != -1 and fullname.lower().replace(' ','').find(lastname) != -1:
                    name.click()
                    break
            except: 
                pass


        x_ray_docs = self.driver.find_element(By.XPATH ,'//*[@id="ptt_3"]/span')
        x_ray_docs.click()
        time.sleep(.5)
        ok_button = self.driver.find_element(By.XPATH ,'//*[@id="ptDocsTreeBtn3"]')
        ok_button.click()
        time.sleep(3)
        attatched_docs = self.driver.find_element(By.XPATH ,'//*[@id="divDocDetail"]/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/form/div[1]/div[8]/div/div/span')
        attatched_docs.click()
        time.sleep(2)
        for orders in range(2,100):
            try:

                order = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[{orders}]')
                
                if order.is_displayed():
                    name_of_imaging_order = self.driver.find_element(By.XPATH, f'//*[@id="LabDIProcHistoryDetailTbl40"]/tbody[{orders}]/tr[1]/td[13]').text

                    order_type_from_fax_simple = order_type_from_fax.lower().replace(' ','')

                    name_of_imaging_order_simple = name_of_imaging_order.lower().replace(' ','')
                    print(name_of_imaging_order_simple)
                    if name_of_imaging_order_simple.find('-') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace('-','')
                    if name_of_imaging_order_simple.find('/') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace('/','')
                    if name_of_imaging_order_simple.find(':') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace(':','')
                    if name_of_imaging_order_simple.find(',') != -1:
                        name_of_imaging_order_simple = name_of_imaging_order_simple.replace(',','')
                    
                    
                    is_order_found = order_type_from_fax_simple.find(name_of_imaging_order_simple)
                    #the order should alwase be found
                    if is_order_found != -1:
                        # 
                        check_box = self.driver.find_element(By.XPATH ,'//*[@id="ptReport-chkbox-330145"]') 
                        check_box.click()
                        time.sleep(.5)
                        ok_button2 =self.driver.find_element(By.XPATH , '//*[@id="LabDIProcHistoryDetailBtn6"]')
                        ok_button2.click()
                        break
            except:
                
                print('no orders found')
                
                break
            #check if for provider
           #if 
            name_of_doc =self.driver.find_element(By.XPATH , '//*[@id="LabDIProcHistoryDetailBtn6"]')
            assigned   =self.driver.find_element(By.XPATH , '//*[@id="LabDIProcHistoryDetailBtn6"]')
            



def process1 ():
        d = DownloadAndReadFax()
        #l = LookUpPatient()
        d.login()
        #l.login()
        #l.searchPatient(last_Name='rizzo' ,first_Name='zach', DOB='05221999')
        d.navigate_To_Documents()
        # d.Download_docs() 
        d.Download_one_doc(starting_page=1, starting_doc_number=7)
       
        time.sleep(5)

    
         
        
def process2():
            l = CheckPatient()
            l.login()
            l.searchPatient(last_Name='brown' ,first_Name='ronald', DOB='12/12/1956')
            l.check_refill(name_of_medicine_from_fax='aaaa', pharmacy_from_fax='3302 garfield avenue')#Metoprolol Tartrate 100 MG 

    # login()
    # try:
    #     navigate_To_Documents()
    # except:
    #     input('hit enter')
    # Download_docs()
    # time.sleep(1)

if __name__ =='__main__':
    
    
    
        # threading_one = threading.Thread(target=thread_one)
    #p1 = mp.Process(target=process1)
        
        #p3 = mp.Process(target= process3)
    #p1.start()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        #results = [executor.submit(process1) for _ in range(3)]
        p1 = executor.submit(process1)
        # p2 = executor.submit(process2)
        
    # process2()
        #p3.start()
        #p1.join()
        # threading_two = threading.Thread(target=thread_two)
        # threading_one.start()
        # threading_two.start()
        # threading_one.join()
        # threading_two.join()

    print('done')
