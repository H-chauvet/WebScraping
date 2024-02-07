import re

from bs4 import BeautifulSoup
from scrapy.selector.unified import Selector


def has_numbers(input_string):
    # return true if there is a number in the string
    return bool(re.search(r"\d", input_string))


def full_price(excl_tax_price, vat, ecotaxes=0):
    """
    :param excl_tax_price : excluded tax amount
    :param vat : in decimal (usually 20% in France)
    :param ecotaxes :  tax levied on activities which are considered to be harmful to the environment
    :return: full price with taxes
    """
    return excl_tax_price * (1 + vat) + ecotaxes


def add_space_between_words_in_block(unformatted_string):
    """
    modify the string to separate words starting with a capital letter
    :param unformatted_string: string with words in a block
    :return: formatted string with a space between words in a block
    """
    pattern = r"([^\sA-Z/.-_])([ÀA-Z])"
    return re.sub(
        pattern, lambda match: f"{match.group(1)} {match.group(2)}", unformatted_string
    )


def extract_text_from_html(html_elt: Selector):
    selector = html_elt.get()

    if not selector:
        return None

    return BeautifulSoup(selector, "html.parser").get_text("", strip=True)


def extract_price(price_text) -> float:
    return float(price_text.replace(",", ".").replace("€", "").replace(" ", ""))


def extract_currency(price_text) -> str:
    return price_text.strip(" 0123456789,").strip()
