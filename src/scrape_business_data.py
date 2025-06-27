from seleniumbase import SB
import urllib.parse

GMAPS_PLACE_SELECTOR = 'a[href*="https://www.google.com/maps/place"]'


def scroll_down(sb, scroll_feed, amount=2000):
    sb.driver.execute_script(
        "arguments[0].scrollTop += arguments[1];",
        scroll_feed,
        amount,
    )


def scroll_top(sb, scroll_feed):
    sb.driver.execute_script(
        "arguments[0].scrollTop = 0;",
        scroll_feed,
    )


def scrape_business_data(query, max_results=10, headless=False):
    formatted_query = urllib.parse.quote_plus(query)

    with SB(uc=True, headless=headless) as sb:
        sb.uc_open(f"https://www.google.com/maps/search/{formatted_query}")
        first_place = sb.find_element(GMAPS_PLACE_SELECTOR, timeout=15)
        scroll_feed = first_place
        for _ in range(3):
            scroll_feed = sb.get_parent(scroll_feed, by="css selector")

        current_count = 0

        while current_count < max_results:
            elements = sb.find_elements(GMAPS_PLACE_SELECTOR)
            if not elements:
                return None, "No places found."

            current_count = len(elements)

            if current_count >= max_results:
                break

            scroll_down(sb, scroll_feed)

            new_elements = sb.find_elements(GMAPS_PLACE_SELECTOR)
            if len(new_elements) == current_count:
                break

        final_elements = sb.find_elements(GMAPS_PLACE_SELECTOR)[:max_results]
        print(f"Found {len(final_elements)} business listings")

        sb.sleep(20)
