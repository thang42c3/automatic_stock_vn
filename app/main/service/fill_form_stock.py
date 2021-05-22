from selenium import webdriver
from config.config import configs
import time
import os
config = configs()
'''
Đầu vào: Dữ liệu các mã cổ phiếu.
Đầu ra: Các file excell được download trực tiếp từ website ứng với từng mã"
'''

def fill_form_stock1(symbol1, volume1, trading1):
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)


    driver.get("https://webtrading.ssi.com.vn/")
    user=driver.find_element_by_id("name")
    user.send_keys(config["login_user"]["Username"])
    password = driver.find_element_by_id("txtPassword")
    password.send_keys(config["login_user"]["Password"])
    driver.find_element_by_id("btnLogin").click()
    time.sleep(3)
    if trading1 == "L":
        driver.find_element_by_id("btnOrderBuy").click()
    elif trading1 == "S":
        driver.find_element_by_id("btnOrderSell").click()
    code_stock = driver.find_element_by_id("txtStockSymbol")
    code_stock.send_keys(symbol1)
    volume_stock = driver.find_element_by_id("txtOrderUnits")
    volume_stock.send_keys(volume1)
    price_stock = driver.find_element_by_id("txtOrderPrice")
    price_stock.send_keys("ATO")
    pin_stock = driver.find_element_by_id("txtSecureCode")
    pin_stock.send_keys(config["login_user"]["Pin_code"])
    #driver.find_element_by_id("btnOrder").click()
    driver.close()
    return symbol1


