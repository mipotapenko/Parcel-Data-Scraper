# Scrape the Steuben County Parel Data Sit.

from bs4 import BeautifulSoup
import requests
import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def request_page_and_pickle(url, filename):
    page = requests.get(url)

    with open(filename, 'wb') as file:
        pickle.dump(page, file)

    return page


def extract_tax_info_string(driver, link):
    driver.get(link)
    info_table = driver.find_element(By.ID, "Table1")
    top_label = info_table.find_element(By.ID, "pnlLabel")
    bulk_data = info_table.find_element(By.ID, "pnlRTaxID")

    return top_label.text + "\n" + bulk_data.text


# def collect_links_from_index_page()
def extract_inventory_string(driver, link):
    driver.get(link)
    try:
        inventory_button = driver.find_element(By.ID, "btnInventory")
    except:
        inventory_button = driver.find_element(By.ID, "btnCInventory")

    inventory_button.click()
    info_table = driver.find_element(By.ID, "Table1")
    top_label = info_table.find_element(By.ID, "pnlLabel")

    try:
        bulk_data = info_table.find_element(By.ID, "pnlRInventory")
    except:
        bulk_data = driver.find_element(By.ID, "pnlCInventory")

    return top_label.text + "\n" + bulk_data.text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.perf_counter()

    url = "https://cityofcorning.sdgnys.com/index.aspx"

    new_request_Q = False

    options = Options()
    # options.add_argument('--headless=new')
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    public_button = driver.find_element(By.ID, "btnPublicAccess")
    public_button.click()

    if "disclaimer" in driver.current_url:
        check_box = driver.find_element(By.ID, "chkAgree")
        check_box.click()
        submit = driver.find_element(By.ID, "btnSubmit")
        submit.click()

    search_button = driver.find_element(By.ID, "btnSearch")
    search_button.click()

    index_page_url = driver.current_url
    parcel_data_text = []
    total_page_count = driver.find_element(By.ID, "lblPageCount").text
    next_page_exists_Q = True

    while next_page_exists_Q:
        table = driver.find_element(By.ID, "tblList")
        entries = table.find_elements(By.TAG_NAME, "tr")
        entry_links = [entry.find_element(By.TAG_NAME, "a").get_attribute("href") for entry in entries]

        for link in entry_links[1:]:
            try:
                full_table_text = extract_tax_info_string(driver, link)
                parcel_data_text.append(full_table_text)
                inventory = extract_inventory_string(driver, link)
                parcel_data_text.append(inventory)
            except Exception as error:
                print("error at " + link)
                print(error)

        driver.get(index_page_url)
        current_page = driver.find_element(By.ID, "lblCurrentPage").text
        next_page_exists_Q = int(current_page) < int(total_page_count)

        if next_page_exists_Q:
            index_page_url = driver.find_element(By.ID, "lnkNextPage").get_attribute("href")
            driver.get(index_page_url)

        print("Finished processing page " + current_page + " of " + total_page_count)

    driver.close()

    dumpfile_name = os.path.join(os.path.realpath(os.path.dirname(__file__)), "IndexPageCorningEstimatesWithInventory.pickle")
    with open(dumpfile_name, 'wb') as file:
        pickle.dump(parcel_data_text, file)

    stop = time.perf_counter()
    print("It took " + str(stop - start) + "ms to scrape the parcel data")



