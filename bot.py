import collections
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


class Browser:
    my_user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/92.0.4515.159 Safari/537.36")
    browser_options = uc.ChromeOptions()
    # browser_options.add_argument('--headless')
    browser_options.add_argument('--disable-blink-features=AutomationControlled')
    browser_options.add_argument(f"user-agent={my_user_agent}")


    # browser = webdriver.Chrome(browser_options)

    def __init__(self):

        self.class_name = None
        self.element = None
        self.browser = uc.Chrome(options=self.browser_options)
        self.class_elements = []
        self.tag_elements = []
        self.browser.implicitly_wait(15)
        self.wait = WebDriverWait(self.browser, timeout=15)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.browser.quit()

    def locate_by_id(self, url, **kwargs) -> WebElement:
        """
        take one or a list of url and id and return the element with that id.
        :param url: url to search
        :param kwargs: id argument
        :return:
        """
        global page_content
        element_id = kwargs['id']

        self.browser.get(url)
        time.sleep(1)
        page_content = self.wait.until(ec.presence_of_element_located((By.ID, element_id)))
        return page_content
        # self.id_elements.append(element)

    def locate_by_class_attr(self, class_name: str, **kwargs) -> list:
        """Find and element by class attribute
        :type class_name: str
        """

        site_url = kwargs.get('site_url', None)
        web_element = kwargs.get('web_element', None)

        if site_url:
            self.browser.get(site_url)
            time.sleep(.5)
            yield self.browser.find_elements(By.CLASS_NAME, class_name)
        else:
            yield web_element.find_elements(By.CLASS_NAME, class_name)

    def locate_by_tag(self, tag_name: str, **kwargs) -> list:
        """Find elements with specified tag name
        :type tag_name: str
        """

        site_url = kwargs.get('site_url', None)
        class_name = kwargs.get('class_name', None)
        web_element = kwargs.get('web_element', None)
        page_content = kwargs.get('page_content', None)

        if site_url:
            self.browser.get(site_url)
            time.sleep(.5)
            self.tag_elements = self.wait.until(ec.presence_of_element_located((By.TAG_NAME, tag_name)))
            return self.tag_elements
        elif web_element:
            yield web_element.find_elements(By.TAG_NAME, tag_name)
        elif class_name:
            for elm in self.locate_by_class_attr(class_name, page_content=page_content):
                time.sleep(.5)
                for e in elm:
                    yield e.find_elements(By.TAG_NAME, tag_name)
                # return self.tag_elements

    def locate_by_css_selector(self, css_selector: str, **kwargs) -> list:
        """
        Find the element with the given css_selector
        :param css_selector
        :param: page_content = kwargs['page_content']
        """

        site_url: str = kwargs.get('site_url', None)
        web_element = kwargs.get('web_element', None)

        if site_url:
            self.browser.get(site_url)
            time.sleep(.5)
            yield self.wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
        else:
            web = web_element.find_elements(By.CSS_SELECTOR, css_selector)
            yield web

    # def create_web_element_from_html(self, html_page, element_id):
    #     """take a html file path and create a web element from HTML source code"""
    #
    #     self.browser.get(html_page)
    #     time.sleep(1)
    #     page = self.wait.until(ec.presence_of_element_located(("id", element_id)))
    #     return page


if __name__ == '__main__':
    url = 'https://www.noelleeming.co.nz/p/apple-iphone-14-pro-128gb-gold/N214572.html'
    class_name = 'product-slider'
    tag = 'img'
    img_selector = "img.img-fluid"
    price_selector = "span.gep-price__integer"
    with Browser() as bot:
        # main_content = bot.locate_by_id(url, id='maincontent')
        # time.sleep(.15)
        # product_images = bot.locate_by_css_selector(img_selector, site_url=url, page_content=main_content)
        # product_price = bot.locate_by_css_selector(price_selector, site_url=None, page_content=main_content)
        # for elm in product_price:
        #     for i in elm:
        #         prod_price = i.text
        # images = []
        # count = 0
        # for elm in product_images:
        #     for img in elm:
        #         if count == 0:
        #             prod_name = img.get_attribute('title').strip(',')
        #         images.append(img.get_attribute('src'))
        page_url = r'C:\Users\Fred\PycharmProjects\noelleeming\page_content.html'
        page = bot.create_web_element_from_html(page_url, 'maincontent')
        print(page)
