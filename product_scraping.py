from tasks.Scraper import Scraper
import sys


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print('Use: python product_scraping.py <arquivo de saída> <quantidade de produtos> <tempo de espera>')
        sys.exit(1)

    quantity_products = int(sys.argv[1])
    wait_time = float(sys.argv[2])
    
    scraper = Scraper(quantity_products, wait_time)
    scraper.run()

if __name__ == '__main__':
    main()
