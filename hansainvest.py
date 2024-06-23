######################################################
# Author: Ivan Arizanovic <ivanarizanovic@yahoo.com> #
######################################################

import os
import time
import requests
import pandas as pd
from pandas import DataFrame
from hashlib import md5
from typing import TextIO
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import create_parents, info_output, warning_output, error_output
from config import execution_time, root_disk_location, max_entries, summary


class HansaInvest:
    """
    Scrap the fund data from HansaInvest WebSite.
    """
    url: str = "https://fondswelt.hansainvest.com/de/downloads-und-formulare/download-center"
    doc_types: str = ["Verkaufsprospekt", "Jahresbericht", "Halbjahresbericht"]
    csv_path: str = f"{root_disk_location}\\FundDatabase\\fundDatabase.csv"
    file_path_prefix: str = f"{root_disk_location}\\FundDatabase\\Hansainvest"
    entry_counter: int = 0
    entry_skipped: int = 0
    start_time: float = None
    csv_file: TextIO = None
    df: DataFrame = None
    driver: WebDriver = None

    def __init__(self):
        # Get start time for Execution time calculation or for Summary output
        if execution_time or summary:
            self.start_time = time.time()

        # Init and open the CSV data file for appending and parsing
        self.csv_file = self.csv_init()
        self.df = pd.read_csv(self.csv_path)

        # Init the web driver
        self.driver = self.web_driver_init()

    def __del__(self):
        # Print summary information
        self.summary_output()

        # Close the window and quit the web driver
        if self.driver:
            self.driver.quit()

        # Close the CSV file
        if self.csv_file:
            self.csv_file.close()

        # Execution time output
        if execution_time:
            print(f"Execution time: {time.time() - self.start_time} seconds")

    def csv_init(self) -> TextIO:
        """
        Init the CSV data file.
        :return: File stream.
        """
        # Create the CSV, if it doesn't exist
        if not os.path.exists(self.csv_path):
            # Create parents directories
            create_parents(self.csv_path)
            # Add the header
            try:
                with open(self.csv_path, mode="a", encoding='utf-8') as csv_file:
                    csv_file.write('"ISIN","DocumentType","EffectiveDate","DownloadDate","DownloadUrl",'
                                   '"FilePath","MD5Hash","FileSize"\n')
            except:
                error_output(f"CSV file cannot be created on path: '{self.csv_path}'")

        # Open the CSV for appending and parsing
        try:
            csv_file = open(self.csv_path, mode="a", encoding='utf-8')
            return csv_file
        except:
            error_output(f"CSV file cannot be opened from path: '{self.csv_path}'")

    def web_driver_init(self) -> WebDriver:
        """
        Init the Web Driver.
        :return: Web Driver object.
        """
        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.maximize_window()
        return driver

    def summary_output(self) -> None:
        """
        Summary information. Can be enabled/disabled in config file.
        """
        if summary:
            print("Summary information on date: %s" % (time.strftime("%d.%m.%Y")))
            print(f" - Number of downloaded data: {self.entry_counter - self.entry_skipped}")
            print(f" - Number of already downloaded data: {self.entry_skipped}")
            print(f" - Number of read data: {self.entry_counter}")
    def accept_disclaimer(self) -> None:
        """
        Accept disclaimer. Used in Process function.
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="disclaimer-modal-start"]/div/div/div[3]/button'))).click()
        except:
            warning_output("Pop-up 'Disclaimer Akzeptieren' is not present")

    def page_waiting(self) -> None:
        """
        Waiting for Webpage response. Used in Process function.
        """
        # Wait 1 second to whole page be loaded
        time.sleep(1)

        # Wait additionally 5 seconds, if it is necessary
        try:
            page_num = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@class="paginate_button page-item active"]'))).text
        except:
            error_output(f"Page cannot be loaded")
        else:
            info_output(f"Page {page_num} is being scraped")

    def row_parsing(self, row) -> bool:
        """
        Parsing a row from data table. Used in Process function.
        Parameter 'row' is WebElement which points to table row.
        :param row: WebElement which points to table row.
        :return: True if row parsing is success finished or False if there is enough downloaded data
        """
        # Get ISIN from first column
        try:
            isin = row.find_element(By.XPATH, './/td[1]/a/span').text
        except:
            error_output(f"ISIN parameter can not be found")

        # Check second, third and forth column
        for n in range(0, len(self.doc_types)):
            # Check if specified number of entries have been downloaded
            if self.entry_counter >= max_entries:
                warning_output(f"First {self.entry_counter} fund data have been downloaded")
                return False

            # Get download url and effective date from second, third or forth column
            try:
                download_url = row.find_element(By.XPATH, f'.//td[{n + 2}]/span/a').get_attribute("href")
                effective_date = row.find_element(By.XPATH, f'.//td[{n + 2}]/span/span/span').text
            except:
                warning_output(f"{isin}: '{self.doc_types[n]}' document is not present")
                continue
            else:
                self.entry_counter += 1

                # Check if row exists in fundDatabase
                if self.df[(self.df.ISIN == isin) & (self.df.DownloadUrl == download_url)].values.any():
                    self.entry_skipped += 1
                    info_output(f"{self.entry_counter}. {isin}: '{self.doc_types[n]}' document is already downloaded")
                    continue

                # Check if PDF is already downloaded
                duplicated_url = self.df[self.df.DownloadUrl == download_url][["FilePath", "MD5Hash"]]
                if duplicated_url["FilePath"].any():
                    file_path = duplicated_url.values[0][0]
                    md5_hash = duplicated_url.values[0][1]
                else:
                    # Get the content of file
                    try:
                        response = requests.get(download_url)
                        response.raise_for_status()
                    except:
                        error_output(f"PDF file cannot be downloaded from url: '{download_url}'")

                    # Get the md5 hash
                    md5_hash = md5(response.content).hexdigest()

                    # Save the file
                    file_name = download_url.split('/')[-1]
                    file_path = f"{self.file_path_prefix}\\{isin}\\{file_name}"
                    create_parents(file_path)
                    try:
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                    except:
                        error_output(f"PDF file cannot be saved to path: '{file_path}'")

                # Get the file size and download date
                file_size = os.path.getsize(file_path)
                download_date = time.strftime("%d.%m.%Y")

                # Generate CSV row with metadata
                data = (f'"{isin}","{self.doc_types[n]}","{effective_date}","{download_date}",'
                        f'"{download_url}","{file_path}","{md5_hash}","{file_size}"')

                # Print metadata if debug mode is enabled
                info_output(f"{self.entry_counter}. Data is downloaded: [{data}]")

                # Append the metadata to DataFrame and to CSV
                self.df.loc[len(self.df)] = data[1:-1].split('","')
                self.csv_file.write(data + '\n')

        return True

    def next_page(self) -> bool:
        """
        Click to the next page button and go to the next Web-page. Used in Process function.
        :return: True if next page is present and button is clicked or False if there is no next page
        """
        try:
            # Get next button as web element
            next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="DataTables_Table_0_next"]')))

            # Check if next page is present
            if next_button.get_attribute("class") == "paginate_button page-item next disabled":
                warning_output("Next page is not present")
                return False

            # Move to the element and perform the click
            webdriver.ActionChains(self.driver).move_to_element(next_button).click().perform()
        except:
            error_output("Button 'Nächste' is not clickable")
        else:
            return True

    def process(self) -> None:
        """
        Process function for HansaInvest Web-page.
        """
        # Accept disclaimer
        self.accept_disclaimer()

        while self.entry_counter < max_entries:
            # Waiting for Webpage response
            self.page_waiting()

            # Get all Fonds from page
            try:
                rows = self.driver.find_elements(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[*]')
            except:
                error_output("Table with fonds cannot be found on the Web-page")
            else:
                for row in rows:
                    if not self.row_parsing(row):
                        return

            # Go to the next page
            if not self.next_page():
                break
