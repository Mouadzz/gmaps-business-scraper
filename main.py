import argparse
from export_to_excel import export_to_excel
from scrape_businesses import scrape_businesses


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
        default="output.xlsx",
        help="xlsx output file",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser headless",
    )

    args = parser.parse_args()

    results, error = scrape_businesses(args.q, args.max, args.headless)

    if error:
        print(f"Error: {error}")
    else:
        export_to_excel(results, args.o)


if __name__ == "__main__":
    main()
