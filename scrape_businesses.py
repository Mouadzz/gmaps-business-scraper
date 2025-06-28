import re
from seleniumbase import SB
import urllib.parse
from gmaps_selectors import (
    ADDRESS_SELECTOR,
    GMAPS_PLACE_SELECTOR,
    OPENS_AT_SELECTOR2,
    REVIEWS_CONTAINER_SELECTOR,
    PLACE_TYPE_SELECTOR,
    NAME_SELECTOR,
    PHONE_SELECTOR,
    WEBSITE_SELECTOR,
    OPENS_AT_SELECTOR,
)


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


def extract_detailed_business_data(sb):
    data = {}

    try:
        data["name"] = sb.get_text(NAME_SELECTOR, timeout=2)
    except:
        data["name"] = "N/A"

    try:
        lines = sb.get_text(REVIEWS_CONTAINER_SELECTOR, timeout=2).split()
        data["reviews_average"] = lines[0] if len(lines) > 0 else "N/A"
        data["reviews_count"] = lines[1].strip("()") if len(lines) > 1 else "N/A"
    except:
        data["reviews_average"] = "N/A"
        data["reviews_count"] = "N/A"

    try:
        data["place_type"] = sb.get_text(PLACE_TYPE_SELECTOR, timeout=2)
    except:
        data["place_type"] = "N/A"

    try:
        data["address"] = sb.get_text(ADDRESS_SELECTOR, timeout=2)
    except:
        data["address"] = "N/A"

    try:
        data["website"] = sb.get_text(WEBSITE_SELECTOR, timeout=2)
    except:
        data["website"] = "N/A"

    try:
        data["phone"] = sb.get_text(PHONE_SELECTOR, timeout=2)
    except:
        data["phone"] = "N/A"

    try:
        try:
            opens_at_text = sb.get_text(OPENS_AT_SELECTOR, timeout=2).strip()
        except:
            opens_at_text = ""

        if not opens_at_text:
            opens_at_text = sb.get_text(OPENS_AT_SELECTOR2, timeout=2).strip()

        clean_text = re.sub(r"\s*⋅\s*", " - ", opens_at_text).strip()
        clean_text = clean_text.replace("", "").strip()
        data["opens_at"] = clean_text
    except:
        data["opens_at"] = "N/A"

    data["url"] = sb.get_current_url()

    return data


def extract_all_business_details(sb, places):
    all_business_data = []

    for i, place in enumerate(places):
        try:
            print(f"Scraping business {i+1}/{len(places)}")

            place.click()
            sb.sleep(2.5)

            # Extract detailed data
            business_data = extract_detailed_business_data(sb)
            all_business_data.append(business_data)

            print(f"Scraped: {business_data.get('name', 'Unknown')}")

        except Exception as e:
            print(f"Error processing place {i+1}: {e}")
            # Add basic error data
            all_business_data.append({"error": str(e)})

    return all_business_data, None


def scrape_businesses(query, max_results=10, headless=False):
    try:
        formatted_query = urllib.parse.quote_plus(query)

        with SB(uc=True, headless=headless) as sb:
            sb.uc_open(f"https://www.google.com/maps/search/{formatted_query}?hl=en")
            first_place = sb.find_element(GMAPS_PLACE_SELECTOR, timeout=15)
            scroll_feed = first_place
            for _ in range(3):
                scroll_feed = sb.get_parent(scroll_feed, by="css selector")

            current_count = 0

            while current_count < max_results:
                places = sb.find_elements(GMAPS_PLACE_SELECTOR)
                if not places:
                    return None, "No places found."

                current_count = len(places)

                if current_count >= max_results:
                    break

                scroll_down(sb, scroll_feed)

                new_places = sb.find_elements(GMAPS_PLACE_SELECTOR)
                if len(new_places) == current_count:
                    break

            final_places = sb.find_elements(GMAPS_PLACE_SELECTOR)[:max_results]
            print(f"Found {len(final_places)} business listings")

            return extract_all_business_details(sb, final_places)
    except Exception as e:
        return None, f"Scraping failed: {e}"
