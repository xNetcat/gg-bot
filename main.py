# python libs
import logging
import argparse

# custom libs
from src.bot import GGBot


def main():
    # config file parser initialization
    parser = argparse.ArgumentParser(prog="gg-bot", description="Bot for a gg.pl")
    parser.add_argument(
        "-u",
        "--username",
        dest="username",
        help="gg.pl id/mail/phone number",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        help="gg.pl password",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        help="number of seconds before timing out",
        type=int,
        required=False,
        default=10,
    )
    parser.add_argument(
        "-hl",
        "--headless",
        dest="headless",
        help="Start webdriver in headless mode",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        help="Debugging mode",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-sd",
        "--selenium-debug",
        dest="selenium_debug",
        help="Selenium debugging",
        action="store_true",
        required=False,
        default=False,
    )
    args = parser.parse_args()

    # custom logging format
    logging.basicConfig(
        level=logging.DEBUG if args.debug == True else logging.INFO,
        format="%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s",
    )

    bot = GGBot(timeout=args.timeout, selenium_debug=args.selenium_debug)
    try:
        bot.close_consent()
        bot.login(username=args.username, password=args.password)
        bot.start_roulette()
        input()
    finally:
        bot.quit()


if __name__ == "__main__":
    main()
