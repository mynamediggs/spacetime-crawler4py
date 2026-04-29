from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()

    from scraper import word_counts, unique_urls, longest_page, subdomains

    print("Unique pages: ", len(unique_urls))
    print("Longest page: ", longest_page)

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]
    print("\nTop 50 words:")
    for word, freq in sorted_words:
        print(word, freq)

    sorted_subdomains = sorted(subdomains.items())
    print("\nSubdomains: ")
    for sub, count in sorted_subdomains:
        print(f"{sub}: {count}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
