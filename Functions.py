from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_in_new_tab(driver , element):
    ActionChains(driver).scroll_to_element(element)
    ActionChains(driver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])

def click_element(driver , element):
    action = ActionChains(driver)
    action.scroll_to_element(element)
    driver.implicitly_wait(1)
    action.click(element)
    action.perform()

def get_page_source(driver , element):
    open_in_new_tab(driver , element)
    time.sleep(5)
    page = driver.page_source
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return page

def get_pages(name):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")    # Open in incognito mode

    service = Service(r'C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('https://www.imdb.com/')

    try:
        search = driver.find_element(By.ID , 'suggestion-search')
        search.send_keys(name)

        first_option = WebDriverWait(driver , 10).until(
            EC.visibility_of_element_located((By.XPATH , '//li[@id = "react-autowhatever-navSuggestionSearch--item-0" and @data-suggestion-index = "0"]')))
        
        first_option.click()
        time.sleep(2)
    except:
        print("Can't find search element!")

    try:
        see_all = driver.find_element(By.CLASS_NAME , "ipc-see-more__text")
        click_element(driver, see_all)
        time.sleep(2)
    except:
        print("Can't find See_all")

    try:
        prof = driver.find_element(By.XPATH , '//div[contains(@class,"ipc-title ipc-title--base ipc-title--title ipc-title--on-textPrimary sc-26510472-5 kdBGGy")]').text
        prof_uc = prof.lower().replace(' ' , '_')
    except:
        print("Can't find prof")

    try:
        movie_section = driver.find_element(By.XPATH , f'//div[@id="accordion-item-{prof_uc}-previous-projects"]')
    except:
        print("Can't find movie_section")

    movies = movie_section.find_elements(By.XPATH , '//li[@class="ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-e73a2ab4-3 hEfisp"]')
    links = movie_section.find_elements(By.XPATH , '//li[@class="ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-e73a2ab4-3 hEfisp"]//a[@class="ipc-metadata-list-summary-item__t"]')

    pages = []
    roles = []

    for movie,link in zip(movies , links):
        if prof.lower() in movie.get_attribute('data-testid'):
            try:
                role = movie.find_element(By.XPATH , './/ul[@class="ipc-inline-list ipc-inline-list--show-dividers credit-text-list base" and @role="presentation"]//li[@class = "ipc-inline-list__item" and @role = "presentation"]//span')
                roles.append(role.text)
            except:
                print("Can't find role.")
            page = get_page_source(driver , link)
            pages.append(page)
        else:
            continue

    driver.quit()
    return pages , roles