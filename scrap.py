from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json 

#----------Output Scapped Result-------------------#
def OutPut_Result(jsonObject,index) :
    # output 
    with open("result_"+str(index)+".json", 'w') as f:
        json.dump(jsonObject, f)
    # Closing file
    f.close()
    
#----------Move Cursor to Right-------------------#
def RightArrow(element):
    element.send_keys(Keys.ARROW_RIGHT)

#----------Move Cursor to Left-------------------#
def LeftArrow(element):
    element.send_keys(Keys.ARROW_LEFT)
    
#----------Move Content's Focus-------------------#
def MoveFocus(ele):
     RightArrow(ele)
     return   ele.get_attribute('title')
 
#--------- Restore Content's Focus----------------#    
def RestoreFocus(ele):
     LeftArrow(ele)
     return   ele.get_attribute('title')


#---------Download giving Row Element--------------#
def Download_Row_Data(row_div):
        
    left_child = row_div.find_elements(by = By.TAG_NAME, value = "div")
    fileURL = left_child[1].get_attribute('title')
    contractNumber =  left_child[3].get_attribute('title')
    documentType = left_child[4].get_attribute('title')
    contractVendor = left_child[6].get_attribute('title')
    contractDescription = left_child[7].get_attribute('title')

    #-------------------Move Cursor to Right----------------- 
    
    MoveFocus(left_child[len(left_child)-1])
    right_child = row_div.find_elements(by = By.TAG_NAME, value = "div")
    
    #------------------Get Rest Part Data-----------------------
    beginDate = right_child[5].get_attribute('title')
    expireDate = right_child[7].get_attribute('title')
    
    #------------------Move Cursor to Left-----------------------
    RestoreFocus(right_child[1])
    left_child = row_div.find_elements(by = By.TAG_NAME, value = "div")
    RestoreFocus(left_child[1])
    left_child = row_div.find_elements(by = By.TAG_NAME, value = "div")
    RestoreFocus(left_child[1])
    
    return {
             'Contract Number'      : contractNumber,
             'Contract Vendor'      : contractVendor,
             'Contract Description' : contractDescription,
             'Begin Date'           : beginDate,
             'Expire Date'          : expireDate,
             'Document Pdf'         : fileURL,
             'document Type'        : documentType   
            } 

def Start_Download(firstElement):
    current_element = firstElement
    result = []  
    next_index = 0  # the next element's index
    count = 0       # current row index
    zip_number = 1  # current package number
    try :
         while 0 < 1:
                
            current_row_index = current_element.get_attribute('aria-rowindex')
            print("downloading.. -> " + current_row_index)
            next_index = int(current_row_index)+1
            result_temp = Download_Row_Data(current_element)
            result.append(result_temp)
            if len(result) == 1000:
                OutPut_Result(result,zip_number)
                zip_number = zip_number + 1
                result = []
                
            #---------------move cusor to next row-----------------------------------------
            current_element.find_elements(by = By.TAG_NAME, value="div")[1].send_keys(Keys.ARROW_DOWN)
            next_element = current_element.find_element(by = By.XPATH, value = ("//div[@aria-rowindex='"+str(next_index)+"']"))
            current_element = next_element
            count = count + 1
    except:
            OutPut_Result(result,zip_number)
            print("Total Records: " + str(count))
    # OutPut_Result(result)
    

def Chrome_Init(page_url):
    
    #-----------------Start Page URL and Wait for loading page-------------
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(page_url)
    wait = WebDriverWait(driver, 60) 
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='row']")))
    
    #-----------------------Start Process-------------------------- 
    rowContent = driver.find_elements(by=By.XPATH, value = "//div[@role='row']")
 
    if len(rowContent) == 0 :
        print("No Content")
    else :
        Start_Download(rowContent[1])
        
def get_Iframe_URL():
    chrome_options = Options()
    start_url = "https://data.tempe.gov/documents/tempegov::procurement-contracts/explore"
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(start_url)
    wait = WebDriverWait(driver, 60) 
    iframeElement = wait.until(EC.presence_of_element_located((By.TAG_NAME,"iframe")))
    result = iframeElement.get_attribute('src')
    driver.quit()
    return result 
if __name__ == '__main__':
    iframe_url =  get_Iframe_URL()
    Chrome_Init(iframe_url)