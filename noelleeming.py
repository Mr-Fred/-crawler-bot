from bot import Browser
from dataclasses import dataclass
import time
import json


@dataclass
class Noelleeming(Browser):
    prod_details: dict

    def __init__(self, urls: list):
        super().__init__()
        self.urls = urls
        self.prod_details = self.get_maincontent()

    @staticmethod
    def extract_iphone_name_from_url(url):
        print(url)
        list_of_elm = url.split('/')
        for elm in list_of_elm:
            if elm.startswith('apple'):
                prod_name = elm
                return prod_name

    def get_maincontent(self):

        main_content_id = 'maincontent'
        details = {}

        try:
            for url in self.urls:
                prod_name = self.extract_iphone_name_from_url(url)

                time.sleep(2)
                details[prod_name] = {}

                main_content = self.locate_by_id(url, id=main_content_id)

                if 'images' not in details[prod_name] or not details[prod_name]['images']:
                    images = self.extract_img_url(main_content)
                    details[prod_name]['images'] = images

                if 'price' not in details[prod_name] or not details[prod_name]['price']:
                    prod_price = self.extract_prod_price(main_content)
                    details[prod_name]['price'] = prod_price

                if 'description' not in details[prod_name] or not details[prod_name]['description']:
                    description = self.extract_long_desc(main_content)
                    details[prod_name]['description'] = description

                time.sleep(5)
            return details

        except OSError as e:
            print('Graceful exception')
        finally:
            self.browser.quit()

    def extract_img_url(self, web_element):

        img_selector = "img.img-fluid"
        prod_buying_area = 'div.product-buying-area'

        prod_info = self.locate_by_css_selector(prod_buying_area, web_element=web_element)
        time.sleep(2)
        for elm in prod_info:
            for content in elm:
                prod_images = self.locate_by_css_selector(img_selector, web_element=content)
                time.sleep(2)
                for child in prod_images:
                    images = []
                    for img in child:
                        images.append(img.get_attribute('src'))
                    return images

    def extract_long_desc(self, web_element):

        desc_selector = ".long-description"
        generated_extra_info = self.locate_by_css_selector(desc_selector, web_element=web_element)
        for generator in generated_extra_info:
            for wb_elm in generator:
                return wb_elm.text

    def extract_prod_price(self, web_element):

        price_selector = "span.gep-price__integer"
        prod_buying_area = 'div.product-buying-area'

        product_buying_area = self.locate_by_css_selector(prod_buying_area, web_element=web_element)
        time.sleep(2)

        for list_items in product_buying_area:
            for wb_elm in list_items:
                price_generator = self.locate_by_css_selector(price_selector, web_element=wb_elm)
                for price_list in price_generator:
                    for price in price_list:
                        return int(price.text.replace(',', '')) / 2


if __name__ == '__main__':
    urls = ['https://www.noelleeming.co.nz/p/apple-iphone-14-pro-128gb-gold/N214572.html',
            'https://www.noelleeming.co.nz/p/apple-iphone-13-128gb---midnight/N208211.html']
    crawler = Noelleeming(urls)
    # crawler.extract_img_url()
    # crawler.extract_prod_price()
    # crawler.extract_long_desc()
    print(crawler.prod_details)
