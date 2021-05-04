from selenium import webdriver
from app.main.service import time
from config.config import configs
import time
config = configs()
'''
Đầu vào: Dữ liệu các mã cổ phiếu.
Đầu ra: Các file excell được download trực tiếp từ website ứng với từng mã"
'''

def fill_form_stock(symbol1, volume1, trading1):
    driver = webdriver.Chrome()
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


