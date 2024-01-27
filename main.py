import csv
from noelleeming import Noelleeming

urls = ['https://www.noelleeming.co.nz/p/apple-iphone-14-pro-128gb-gold/N214572.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-13-128gb---midnight/N208211.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-15-pro-max-256gb---blue-titanium/N220903.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-15-plus-128gb---black/N220861.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-15-256gb---pink/N220883.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-12-64gb---black/N201464.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-15-128gb---pink/N220863.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-14-128gb-midnight/N214540.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-13-512gb---%28product%29-red/N208223.html',
        'https://www.noelleeming.co.nz/p/apple-iphone-14-pro-128gb-space-black/N214570.html']

crawler = Noelleeming(urls=urls)
data = crawler.prod_details

# Specify the CSV file path
csv_file_path = 'product_data.csv'

# Specify the CSV header
csv_header = ['Product Name', 'Description', 'Price', 'Images']

# Write to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(csv_header)

    # Write data
    for product_name, product_data in data.items():
        row = [
            product_name,
            product_data.get('description', ''),
            product_data.get('price', ''),
            ', '.join(product_data.get('images', []))
        ]
        csv_writer.writerow(row)
