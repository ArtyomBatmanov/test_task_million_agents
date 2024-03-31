from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame(columns=['Product Name', 'Brand', 'Price', 'Link'])
page_number = 0
status = True

while status:
    page_number += 1
    url = f"https://online.metro-cc.ru/category/myasnye/ptica?page={page_number}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        product_cards = soup.find_all("div", class_="subcategory-or-type__products-item")

        for product_card in product_cards:
            product_price_element = product_card.find("span", class_="product-price__sum-rubles")

            if product_price_element:
                product_name_element = product_card.find("span", class_="product-card-name__text")
                product_price = product_price_element.text.strip()

                if product_name_element:
                    product_name = product_name_element.text.strip()
                    brand = ''
                    words = product_name.split()
                    brand_started = False

                    for word in words[1:]:
                        if word.istitle():
                            brand = word
                            break

                    product_link = product_card.find("a", class_="product-card-photo__link")["href"]
                    print("Название товара:", product_name)
                    print("Бренд:", brand.strip())
                    print("Цена товара:", product_price, 'руб')
                    print("Ссылка на товар:", product_link)
                    print()
                    df = df._append(
                        {'Product Name': product_name, 'Brand': brand, 'Price': product_price, 'Link': product_link},
                        ignore_index=True)
            else:
                status = False
                break

    else:
        break

df.to_excel('products.xlsx', index=False)
