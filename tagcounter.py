import argparse
from urllib import parse

import logger

from application import utils

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="tagcounter")
    parser.add_argument("--get")
    parser.add_argument("--view")
    args = parser.parse_args()

    if args.get or args.view:

        tags_dict = {}
        elapsed = ''
        url = utils.format_url(args.get or args.view)

        parsed_url = parse.urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')

        if args.get:
            tags_dict, elapsed = utils.get_tag_count_with_timer(url, domain)

        elif args.view:
            tags_dict, elapsed = utils.get_from_db(domain=domain)

            if tags_dict:
                for tag in tags_dict:
                    logger.logger.info(f'{tag}: {tags_dict[tag]}')

            else:
                logger.logger.info(f'Данных по домену "{domain}" в базе нет')

        logger.logger.info(f'Время выполнения: {elapsed}')

    else:
        from application.app import TagCounter

        TagCounter()
