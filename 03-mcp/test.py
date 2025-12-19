import argparse
from server import fetch_page_markdown


def main():
    parser = argparse.ArgumentParser(description="Fetch page markdown via Jina reader")
    parser.add_argument("url", nargs="?", default="https://datatalks.club", help="URL to fetch")
    parser.add_argument("-n", "--preview", type=int, default=1000, help="Number of chars to preview")
    parser.add_argument("--user-agent", dest="user_agent", help="Optional User-Agent header to send to r.jina.ai")
    args = parser.parse_args()

    try:
        md = fetch_page_markdown(args.url, user_agent=args.user_agent)
    except Exception as e:
        print("Error fetching page:", e)
        return

    print(f"--- fetched markdown (first {args.preview} chars) ---")
    print(md[: args.preview])
    print(f"\n--- length: {len(md)}")


if __name__ == "__main__":
    main()
