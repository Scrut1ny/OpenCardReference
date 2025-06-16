import requests
from bs4 import BeautifulSoup

def extract_text_or_none(tag):
    """Extracts text from a tag, stripping whitespace and replacing multiple spaces."""
    return ' '.join(tag.stripped_strings) if tag else None

def scrape_bin_details(bin_iin):
    """Fetches and parses details of a BIN IIN from bincheck.io."""
    url = f"https://bincheck.io/details/{bin_iin}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; BINChecker/1.0)"}

    # Use a try-except for the HTTP request to catch network issues
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch data: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the container div that holds all the details
    container = soup.find("div", class_="p-2 sm:p-5")
    if not container:
        raise Exception("Could not find details container on page")

    # Find all tables in the container, ensure we have at least two
    tables = container.find_all("table", class_="w-full table-auto")
    if len(tables) < 2:
        raise Exception("Expected two detail tables not found")

    # Define fields for each table
    table1_fields = {
        "BIN/IIN", "Card Brand", "Card Type", "Card Level",
        "Issuer Name / Bank", "Issuer's / Bank's Website", "Issuer / Bank Phone"
    }
    table2_fields = {
        "ISO Country Name", "Country Flag", "ISO Country Code A2",
        "ISO Country Code A3", "ISO Country Currency"
    }

    # Result dictionary
    data = {}

    # Helper function to parse a table
    def parse_table(table, expected_fields):
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) != 2:
                continue  # Skip malformed rows
            label = extract_text_or_none(tds[0])
            if label in expected_fields:
                value_td = tds[1]

                # Handle specific cases
                value = None
                if label == "Issuer Name / Bank":
                    value = ", ".join(link.get_text(strip=True) for link in value_td.find_all("a"))
                    if not value:
                        value = extract_text_or_none(value_td)
                elif label == "Issuer's / Bank's Website":
                    value = extract_text_or_none(value_td)
                elif label == "Country Flag":
                    img = value_td.find("img")
                    value = img['src'] if img and img.has_attr('src') else None
                else:
                    value = extract_text_or_none(value_td)

                if value:
                    data[label] = value.strip()

    # Parse both tables
    parse_table(tables[0], table1_fields)
    parse_table(tables[1], table2_fields)

    return data

def main():
    user_input = input("Enter a BIN/IIN (e.g., 1234 56## #### ####): ").strip()

    # Ensure valid input (at least 6 digits)
    if len(user_input) < 6 or not user_input[:6].isdigit():
        print("Please enter at least 6 digits.")
        return

    bin_iin = user_input[:6]

    try:
        details = scrape_bin_details(bin_iin)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Print results in a clean format
    print("\nBIN/IIN Details:")
    print("-" * 40)
    fields = [
        "BIN/IIN", "Card Brand", "Card Type", "Card Level",
        "Issuer Name / Bank", "Issuer's / Bank's Website", "Issuer / Bank Phone",
        "ISO Country Name", "Country Flag", "ISO Country Code A2",
        "ISO Country Code A3", "ISO Country Currency"
    ]
    for field in fields:
        print(f"{field:<25} : {details.get(field, 'N/A')}")

if __name__ == "__main__":
    main()
