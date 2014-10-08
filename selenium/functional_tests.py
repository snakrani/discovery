from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, unittest


class FunctionalTests(unittest.TestCase): 

    def setUp(self):
        self.base_url = 'http://localhost:8000'
        self.driver = webdriver.Firefox()

    def test_titles_are_correct(self):
        #checks document title and title and subtitle of page
        driver = self.driver
        driver.get(self.base_url + '/')
        self.assertEqual('Mirage', driver.title)
        self.assertEqual('MIRAGE', driver.find_element_by_css_selector("span.oasis_title").text)
        self.assertEqual('OASIS Market Research', driver.find_element_by_css_selector("span.oasis_subtitle").text)

    def test_veteran_owned_search(self):
        #on search results page, select veteran owned filter
        driver = self.driver
        driver.get(self.base_url + "/results?vehicle=oasissb&naics-code=541990&")
        driver.find_element_by_id("vet").click()
        element = WebDriverWait(driver, 3).until(
            EC.text_to_be_present_in_element((By.ID, "your_filters"), 'Veteran Owned')
            )
        self.assertEqual('Veteran Owned', driver.find_element_by_id('your_filters').text)
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]* vendors match your search$")

    def test_zero_results_indicator_on_search(self):
        #perform a search with zero expected results and make sure that it is clear that there are no results
        driver = self.driver
        driver.get(self.base_url + "/results?vehicle=oasissb&setasides=A6,A2,XX&naics-code=541990&")
        self.assertEqual("0 vendors match your search", driver.find_element_by_css_selector("span.matching_your_search").text)

    def test_socioeconomic_indicators_in_search_results(self):
        driver = self.driver
        #on search results page for a veteran owned search
        driver.get(self.base_url + "/results?vehicle=oasissb&setasides=A5&naics-code=541330&")
        #make sure veteran owned filter is selected
        self.assertEqual("A5", driver.find_element_by_id("vet").get_attribute("value"))
        #make sure headers for each socioeconomic indicator exist
        self.assertEqual(driver.find_element_by_css_selector("td.h_8a").text, "8(a)")
        self.assertEqual(driver.find_element_by_css_selector("td.h_hubz").text, "HubZ")
        self.assertEqual(driver.find_element_by_css_selector("td.h_sdvo").text, "SDVO")
        self.assertEqual(driver.find_element_by_css_selector("td.h_wo").text, "WO")
        self.assertEqual(driver.find_element_by_css_selector("td.h_vo").text, "VO")
        self.assertEqual(driver.find_element_by_css_selector("td.h_sdb").text, "SDB")
        #make sure the first few results are all veteran owned
        self.assertEqual("X", driver.find_element_by_xpath("//table//tr[2]/td[7]").text)
        self.assertEqual("X", driver.find_element_by_xpath("//table//tr[3]/td[7]").text)
        self.assertEqual("X", driver.find_element_by_xpath("//table//tr[4]/td[7]").text)

    def test_result_count_on_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasissb&naics-code=541330&setasides=A5&pool=1_SB")
        #make sure number of search results are listed
        self.assertEqual("11 vendors match your search", driver.find_element_by_css_selector("span.matching_your_search").text)

    def test_search_criteria_on_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasissb&naics-code=541330&setasides=A5&pool=1_SB")
        #make sure selected naics is described above search results
        element = WebDriverWait(driver, 3).until(
            EC.text_to_be_present_in_element((By.ID, "your_filters"), 'Veteran Owned')
            )        
        #make sure selected filters are described above search results
        self.assertEqual("541330 - Engineering Services", driver.find_element_by_id("your_search").text)


    def test_vendor_count_in_search_results(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasissb&naics-code=541330&setasides=A5&")
        #make sure a count of vendors matching search is listed
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, "\d+ vendors match your search")

    def test_8a_and_hubzone_added(self):
        driver = self.driver
        #load search results
        driver.get(self.base_url + "/results?vehicle=oasissb&setasides=A6&naics-code=541620&")
        #select 8(a) filter
        
        #make sure first few results are for 8(a) vendors
        #uncheck 8(a) and select HubZone filter
        #make sure first few results are for HubZ vendors

    def test_vendor_info(self):
        driver = self.driver
        #load vendor page
        #check CAGE code, DUNS number, employees, revenue, address, address2, poc_name, poc_phone

    def test_all_contracts_button(self):
        driver = self.driver
        #load vendor page with showall=true
        #make sure all contracts button is active
        #make sure text of all contracts button is 'All Contracts'
        #make sure text of NAICS button is 'NAICS <naics-code>'

    def test_naics_contracts_button(self):
        driver = self.driver
        #load vendor page (without showall=true)
        #make sure NAICS button is active
        #make sure text of all contracts button is 'All Contracts'
        #make sure text of NAICS button is 'NAICS <naics-code>'

    def test_contract_info_displayed(self):
        driver = self.driver
        #load vendor page
        #check headers for contracts table
        #find way to verify contract data

    def test_number_of_pools_not_displayed_in_search_results(self):
        driver = self.driver
        #open search results
        driver.get(self.base_url + "/results?vehicle=oasissb&setasides=A6&naics-code=541330&")
        #make sure format of result count is '* vendors match your search'
        self.assertRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]* vendors match your search$")
        #make sure format of result count is not '* vendors in * pool(s) match your search'
        self.assertNotRegexpMatches(driver.find_element_by_css_selector("span.matching_your_search").text, r"^[\s\S]*in [\s\S]* pool\(s\)[\s\S]*$")


    def test_data_load_dates_displayed_on_landing_page(self):
        driver = self.driver
        #make sure SAM load date is displayed and not 12/31/69
        #make sure FPDS load date is displayed and not 12/31/69

    def test_csv_links_exist(self):
        driver = self.driver
        #load search results
        #make sure csv link exists and is correct
        #load vendor detail page
        #make sure csv link exists and is correct

    def test_footer_links(self):
        driver = self.driver
        #load landing page
        #check OASIS program home link text and href
        #check GitHub link text and href
        #load search results
        #check OASIS program home link text and href
        #check GitHub link text and href
        #load vendor detail page
        #check OASIS program home link text and href
        #check GitHub link text and href

    def test_vehicle_naics_filter_select_order_ensured(self):
        driver = self.driver
        #open landing page
        #if there's only one vehicle, make sure naics is editable
        #if there's more than one vehicle, make sure naics is not editable
        #make sure filters are not editable
        #open search results
        #make sure vehicle select is editable
        #make sure naics dropdown is editable
        #make sure filters are editable

    def test_poc_header_exists(self):
        driver = self.driver
        #open vendor detail page
        #make sure title of point of contact section in header is 'OASIS POC'

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
