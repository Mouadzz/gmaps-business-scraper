import argparse
from src.scrape_business_data import scrape_business_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        type=str,
        required=True,
        help="Google Maps search query",
    )
    parser.add_argument(
        "-max",
        type=int,
        default=10,
        help="Max results to scrape",
    )
    parser.add_argument(
        "-o",
        type=str,
        default="output.csv",
        help="CSV output file",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser headless",
    )

    args = parser.parse_args()

    results = scrape_business_data(args.q, args.max, args.headless)


if __name__ == "__main__":
    main()
