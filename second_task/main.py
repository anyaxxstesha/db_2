from second_task.config.database import create_tables
from second_task.parser_engine.db_loader import database_load
from second_task.parser_engine.exel_scraper import parse_tables

url = "https://spimex.com/markets/oil_products/trades/results/"

def main():
    create_tables()
    gen = parse_tables(url)
    database_load(gen)

if __name__ == "__main__":
    main()
