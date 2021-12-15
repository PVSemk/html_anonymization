from argparse import ArgumentParser
from anonymizer import DownloadParseHTML, AnonymizerHTML


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url", type=str, help="Url to website for anonymization", required=True)
    parser.add_argument("--output_folder", type=str, help="Path to output folder", default="./")
    parser.add_argument("--save_media_content", action="store_true", help="Try to store both the site's content (e.g images) and text")
    parser.add_argument("--page_filename", type=str, default="page", help="Filename to store the result html")
    return parser.parse_args()


def main():
    args = parse_args()
    html_parser = DownloadParseHTML(**vars(args))
    soup = html_parser.get_soup()
    html_parser.save_page()
    html_anonymizer = AnonymizerHTML(soup, args.output_folder, args.page_filename)
    html_anonymizer.anonymize_html_content()
    html_anonymizer.save_anonymized_page()


if __name__ == "__main__":
    main()
