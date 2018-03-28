from django.conf import settings
from django.test import LiveServerTestCase

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time, unittest


class FunctionalTests(LiveServerTestCase): 

    def setUp(self):
        self.screenshot_dir = "{}/{}/{}".format(settings.PROJ_DIR, 'logs', 'screenshots')
        
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

        self.base_url = 'http://localhost:8080'
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        
        self.driver.set_page_load_timeout(60)

    #helper function courtesy of http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    def test_titles_are_correct(self):
        driver = self.driver
        #open landing page
        driver.get(self.base_url + '/')
        #make sure title of landing page is Discovery
        self.assertEqual('Discovery', driver.title)
        #make sure subtitle of page is OASIS Market Research
        #this got removed when logo was updated
        #self.assertEqual('OASIS Market Research', driver.find_element_by_css_selector("span.oasis_subtitle").text)

    def test_veteran_owned_search(self):
        #on search results page, select veteran owned filter
        driver = self.driver
        driver.get(self.base_url + "/results?vehicle=oasis_sb&naics-code=541990&")
        driver.find_element_by_id("vet").click()
        time.sleep(5)
        self.assertEqual('Veteran Owned', driver.find_element_by_id('your_filters').text)
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]* vendors match your search$")

    def test_zero_results_indicator_on_search(self):
        #perform a search with zero expected results and make sure that it is clear that there are no results
        driver = self.driver
        driver.get(self.base_url + "/results?vehicle=oasis_sb&setasides=A6,A2,XX&naics-code=541990&")
        time.sleep(2)
        self.assertEqual("0 vendors match your search", driver.find_element_by_css_selector("span.matching_your_search").text)

    def test_socioeconomic_indicators_in_search_results(self):
        driver = self.driver
        #on search results page for a veteran owned search
        driver.get(self.base_url + "/results?vehicle=oasis_sb&setasides=A5&naics-code=541330&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure veteran owned filter is selected
        self.assertEqual("A5", driver.find_element_by_id("vet").get_attribute("value"))
        #make sure headers for each socioeconomic indicator exist
        self.assertEqual(driver.find_element_by_css_selector("th.h_8a").text, "8(a)")
        self.assertEqual(driver.find_element_by_css_selector("th.h_hubz").text, "HubZ")
        self.assertEqual(driver.find_element_by_css_selector("th.h_sdvo").text, "SDVO")
        self.assertEqual(driver.find_element_by_css_selector("th.h_wo").text, "WO")
        self.assertEqual(driver.find_element_by_css_selector("th.h_vo").text, "VO")
        self.assertEqual(driver.find_element_by_css_selector("th.h_sdb").text, "SDB")
        #make sure the first few results are all veteran owned
        try:
            self.assertTrue(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[2]/td[8]/img'))
        except:
            self.assertTrue(False)

    def test_result_count_on_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasis_sb&naics-code=541330&setasides=A5&pool=1_SB")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure number of search results are listed
        self.assertEqual("1 vendors match your search", driver.find_element_by_css_selector("span.matching_your_search").text)

    def test_search_criteria_on_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasis_sb&naics-code=541330&setasides=A5&pool=1_SB")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure selected filters are described above search results
        self.assertEqual("Engineering Services ( 541330 )", driver.find_element_by_id("your_search").text)


    def test_vendor_count_in_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasis_sb&naics-code=541330&setasides=A5&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure a count of vendors matching search is listed
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, "\d+ vendors match your search")

    def test_8a_and_hubzone_added(self):
        driver = self.driver
        #load 8(a) search results
        driver.get(self.base_url + "/results?setasides=A6&vehicle=oasis_sb&naics-code=541330B&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        try:
            self.assertTrue(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[2]/td[4]/img'))
        except Exception as e:
            raise

        #load HubZone search results
        driver.get(self.base_url + "/results?setasides=XX&vehicle=oasis_sb&naics-code=541330&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure first few results are for HubZ vendors
        try:
            self.assertTrue(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[2]/td[5]/img'))
        except Exception as e:
            raise

    def test_vendor_info(self):
        driver = self.driver
        #load vendor page
        driver.get(self.base_url + "/vendor/170203199/?setasides=A6&vehicle=oasis_sb&naics-code=541330&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #check CAGE code, DUNS number, employees, revenue, address, address2, poc_name, poc_phone
        self.assertEqual("35CZ6", driver.find_element_by_css_selector("span.cage_code.admin_data").text)
        self.assertEqual("170203199", driver.find_element_by_css_selector("span.duns_number.admin_data").text)
        self.assertTrue(62 <= int(driver.find_element_by_css_selector("span.number_of_employees.admin_data").text.replace(',', '')))
        self.assertTrue(5686000 <= int(driver.find_element_by_css_selector("span.annual_revenue.admin_data").text.replace(',', '').replace('$', '')))
        self.assertEqual("8610 Explorer Dr Ste 305", driver.find_element_by_css_selector("span.vendor_address1.admin_data2").text)
        self.assertEqual("Colorado Springs, CO 80920", driver.find_element_by_css_selector("span.vendor_address2.admin_data2").text)
        self.assertEqual("Bobby P. Veazey", driver.find_element_by_css_selector("span.vendor_poc_name.admin_data2").text)
        self.assertEqual("719-213-6199", driver.find_element_by_css_selector("span.vendor_poc_phone.admin_data2").text)
        self.assertEqual("OASISPOOL1@apogeemail.net", driver.find_element_by_css_selector("span.vendor_poc_email.admin_data2").text)

    def test_all_contracts_button(self):
        driver = self.driver
        #load vendor page with showall=true
        driver.get(self.base_url + "/vendor/118498067/?vehicle=oasis_sb&naics-code=541330C&showall=true")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        
        #make sure text of all contracts button is 'All Contracts'
        all_contracts_button = driver.find_element_by_id('all_contracts_button')
        self.assertEqual("All Contracts", all_contracts_button.text)
        #make sure text of NAICS button is 'NAICS <naics-code>'
        self.assertEqual("NAICS 541330", driver.find_element_by_id('naics_contracts_button').text)
        #click and make sure all contracts button is active
        all_contracts_button.click()
        self.assertTrue("contracts_button_active" in all_contracts_button.get_attribute("class"))

    def test_naics_contracts_button(self):
        driver = self.driver
        #load vendor page
        driver.get(self.base_url + "/vendor/049192649/?vehicle=oasis_sb&naics-code=541330&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure text of NAICS button is 'NAICS <naics-code>'
        naics_contracts_button = driver.find_element_by_id('naics_contracts_button')
        self.assertEqual("NAICS 541330", naics_contracts_button.text)
        #make sure text of all contracts button is 'All Contracts'
        self.assertEqual("All Contracts", driver.find_element_by_id('all_contracts_button').text)
        #click and make sure all contracts button is active
        naics_contracts_button.click()
        self.assertTrue("active" in naics_contracts_button.get_attribute("class"))

    def test_contract_info_displayed(self):
        driver = self.driver
        #load vendor page
        driver.get(self.base_url + "/vendor/623876096/?vehicle=oasis_sb&naics-code=541330&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #verify that contracts list isn't empty
        self.assertFalse(driver.find_element_by_id('no_matching_contracts').is_displayed())
        #make sure at least one row exists
        self.assertTrue(driver.find_element_by_xpath('//*[@id="ch_table"]/div/table/tbody/tr[2]'))
        #open vendor with naics subcategory
        driver.get(self.base_url + "/vendor/102067378/?vehicle=oasis_sb&naics-code=541712B&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure at least one row exists
        self.assertTrue(driver.find_element_by_xpath('//*[@id="ch_table"]/div/table/tbody/tr[2]'))

    def test_number_of_pools_not_displayed_in_search_results(self):
        driver = self.driver
        #open search results
        driver.get(self.base_url + "/results?setasides=A6&vehicle=oasis_sb&naics-code=541612&")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure format of result count is '* vendors match your search'
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]* vendors match your search$")
        #make sure format of result count is not '* vendors in * pool(s) match your search'
        self.assertNotRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]*in [\s\S]* pool\(s\)[\s\S]*$")

    def test_data_load_dates_displayed_on_landing_page(self):
        driver = self.driver
        #open landing page
        driver.get(self.base_url + '/')
        time.sleep(1)
        #make sure SAM load date is displayed and not 12/31/69
        self.assertRegexpMatches(driver.find_element_by_id("data_source_date_sam").text, r"^[\d]*/[\d]*/[\d]*$")
        self.assertNotEqual(driver.find_element_by_id("data_source_date_sam").text, "12/31/69")
        self.assertNotEqual(driver.find_element_by_id("data_source_date_sam").text, "NaN/NaN/NaN")
        #make sure FPDS load date is displayed and not 12/31/69
        self.assertRegexpMatches(driver.find_element_by_id("data_source_date_fpds").text, r"^[\d]*/[\d]*/[\d]*$")
        self.assertNotEqual(driver.find_element_by_id("data_source_date_sam").text, "12/31/69")
        self.assertNotEqual(driver.find_element_by_id("data_source_date_sam").text, "NaN/NaN/NaN")

    def test_csv_links_exist(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + '/results?vehicle=oasis_sb&naics-code=541620&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure csv link exists and is correct
        self.assertRegexpMatches(driver.find_element_by_link_text("download data (CSV)").get_attribute("href"), r"^[\s\S]*/results/csv[\s\S]*$")
        #load vendor detail page
        driver.get(self.base_url + "/vendor/626979228/?naics-code=541620&")
        time.sleep(2)
        #make sure csv link exists and is correct
        self.assertRegexpMatches(driver.find_element_by_link_text("Download vendor data (CSV)").get_attribute("href"), r"^[\s\S]*/vendor/[\s\S]*/csv[\s\S]*$")

    def test_footer_links(self):
        driver = self.driver
        #open landing page
        driver.get(self.base_url + '/')
        #check OASIS program home link text and href
        self.assertEqual(driver.find_element_by_link_text("OASIS Program Home").get_attribute("href"), "http://www.gsa.gov/oasis")
        #check GitHub link text and href
        self.assertEqual(driver.find_element_by_link_text("Check out our code on GitHub").get_attribute("href"), "https://github.com/PSHCDevOps/discovery")
        #load search results
        #check OASIS program home link text and href
        self.assertEqual(driver.find_element_by_link_text("OASIS Program Home").get_attribute("href"), "http://www.gsa.gov/oasis")
        #check GitHub link text and href
        self.assertEqual(driver.find_element_by_link_text("Check out our code on GitHub").get_attribute("href"), "https://github.com/PSHCDevOps/discovery")
        #load vendor detail page
        #check OASIS program home link text and href
        self.assertEqual(driver.find_element_by_link_text("OASIS Program Home").get_attribute("href"), "http://www.gsa.gov/oasis")
        #check GitHub link text and href
        self.assertEqual(driver.find_element_by_link_text("Check out our code on GitHub").get_attribute("href"), "https://github.com/PSHCDevOps/discovery")

    def test_vehicle_naics_filter_select_order_ensured(self):
        driver = self.driver
        #open landing page
        driver.get(self.base_url + '/?vehicle=oasis_sb')
        #if there's only one vehicle, make sure naics is enabled
        self.assertTrue(driver.find_element_by_id("naics-code").is_enabled())
        #make sure naics is enabled
        self.assertTrue(driver.find_element_by_id("placeholder").is_enabled())
        #make sure filters are not enabled
        self.assertFalse(driver.find_element_by_css_selector(".se_filter").is_enabled())

        #open search results
        driver.get(self.base_url + '/results?vehicle=oasis_sb&naics-code=541618&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        #make sure vehicle select is enabled
        self.assertTrue(driver.find_element_by_id("naics-code").is_enabled())
        #make sure naics is enabled
        self.assertTrue(driver.find_element_by_id("placeholder").is_enabled())
        #make sure filters are enabled
        self.assertTrue(driver.find_element_by_css_selector(".se_filter").is_enabled())        

    def test_poc_header_exists(self):
        driver = self.driver
        #open vendor detail page
        driver.get(self.base_url + '/vendor/786997739/?naics-code=541618&')
        #make sure title of point of contact section in header is 'OASIS POC'
        self.assertEqual(driver.find_element_by_css_selector('p.admin_title').text, 'POC')

    def test_no_matching_contracts_indicator(self):
        driver = self.driver
        #open vendor detail page where naics contract total is zero
        driver.get(self.base_url + '/vendor/053117149/?vehicle=bmo_sb&naics-code=561730B&')
        time.sleep(2)
        #make sure no matching contracts indicator is displayed
        self.assertTrue(driver.find_element_by_id('no_matching_contracts').is_displayed())
        #open vendor detail apge where naics contract total is one or more
        driver.get(self.base_url + '/vendor/080778868/?vehicle=bmo_sb&naics-code=541330D&')
        #make sure no matching contracts indicator is not displayed
        self.assertFalse(driver.find_element_by_id('no_matching_contracts').is_displayed())

    def test_small_business_badge(self):
        driver = self.driver
        #open vendor detail page where sb badge is expected
        driver.get(self.base_url + '/vendor/053117149/?vehicle=bmo_sb&naics-code=236220&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        self.assertTrue(driver.find_element_by_id('sb_badge').is_displayed())
        #open vendor detail page when sb badge is not expected
        driver.get(self.base_url + '/vendor/041733197/?vehicle=hcats&naics-code=541611&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        self.assertFalse(driver.find_element_by_id('sb_badge').is_displayed())

    def test_vendor_site(self):
        driver = self.driver
        #open page for vendor with site in SAM data
        driver.get(self.base_url + '/vendor/168719552/?vehicle=hcats_sb&naics-code=541611&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        
        #make sure link to site is displayed and href is valid
        self.assertTrue(driver.find_element_by_id('vendor_site_link').is_displayed())
        self.assertEqual(driver.find_element_by_id('vendor_site_link').get_attribute("href"), 'http://www.arcaspicio.com/')
        #open vendor with no site in SAM data
        driver.get(self.base_url + '/vendor/626979228/?vehicle=oasis_sb&naics-code=541330&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_row_data"))
        )
        
        #make sure link to site is NOT displayed
        self.assertFalse(driver.find_element_by_id('vendor_site_link').is_displayed())

    def test_unrestricted_socioeconomic_factors(self):
        driver = self.driver
        #open page for vendor list in OASIS Unrestricted
        driver.get(self.base_url + '/results?vehicle=oasis&naics-code=541618&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vendor_name"))
        )   
        
        #make sure socioeconomic indicator headers exist
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[4]').text, '8(a)')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[5]').text, 'HubZ')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[6]').text, 'SDVO')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[7]').text, 'WO')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[8]').text, 'VO')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[9]').text, 'SDB')
        #make sure "OASIS SB Only" column exists in results table
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[2]/td[4]').text, 'Not Applicable\n(SB Only)')
        #make sure filter selection says "OASIS SB Only"
        self.assertEqual(driver.find_element_by_id('choose_filters').text, 'Choose filters (SB Only)')
        #make sure filter selection remains disabled after NAICS is selected
        self.assertFalse(driver.find_element_by_css_selector(".se_filter").is_enabled())

    def test_number_of_contracts_column(self):
        driver = self.driver
        #open a search results page
        driver.get(self.base_url + '/results?vehicle=oasis_sb&naics-code=541618&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vendor_name"))
        )  
        
        #make sure header for number of results column exists
        self.assertEqual(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[1]/th[3]').text, 'Contracts')
        #make sure value for number of contracts in row 1 is greater than or equal to value in row 2
        self.assertGreater(int(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[2]/td[3]').text), int(driver.find_element_by_xpath('//*[@id="pool_vendors"]/tbody/tr[3]/td[3]').text))

    def test_contracts_sorting(self):
        driver = self.driver
        driver.get(self.base_url + '/vendor/049192649/?vehicle=oasis_sb&naics-code=541330&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table_row_data"))
        )
        second_row = driver.find_element_by_xpath('//*[@id="ch_table"]/div/table/tbody/tr[4]')
        driver.find_element_by_class_name("h_value").click()
    
        def rows_are_stale():
            try: 
                text = second_row.get_attribute('text')
            except StaleElementReferenceException: 
                return True
       
        self.wait_for(rows_are_stale)
        rows = driver.find_elements_by_xpath('//*[@id="ch_table"]/div/table/tbody/tr')
        prev_value = None
        for row in rows[1:]:
            cell = row.find_element_by_class_name('value')
            value = cell.get_attribute('innerText').replace(',', '').replace('$', '')
            
            if value:
                value = float(cell.get_attribute('innerText').replace(',', '').replace('$', ''))
                if not prev_value:
                    prev_value = value
                else:
                    self.assertTrue(value <= prev_value)
                    prev_value = value

    def test_contract_pagination(self):
        driver = self.driver
        #open a vendor page where vendor has more than 100 search results
        driver.get(self.base_url + '/vendor/926451519/?vehicle=oasis&test=true&')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agency"))
        )
        #no more than 100 contracts are listed
        self.assertEqual(driver.find_element_by_id('contracts_current').text, '1 - 5')
        #total number of contracts is displayed
        self.assertTrue(int(driver.find_element_by_id('contracts_total').text.replace(',', '')) >=  10)
        self.assertTrue(driver.find_element_by_id('pagination_container').is_displayed())
        self.assertTrue(driver.find_element_by_id('viewing_contracts').is_displayed())

        #open a vendor page where vendor has zero naics results
        driver.get(self.base_url + '/vendor/097967608/?vehicle=oasis_sb&naics-code=541330&test=true&')
        self.assertFalse(driver.find_element_by_id('pagination_container').is_displayed())
        self.assertFalse(driver.find_element_by_id('viewing_contracts').is_displayed())

    def test_back_button_doesnt_break_naics_select(self):
        pass

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
