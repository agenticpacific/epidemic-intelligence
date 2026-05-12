from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
WORKSPACE_ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve Pacific Epidemic Intelligence dashboard locally.")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Interface to bind to. Default: {DEFAULT_HOST}")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to serve on. Default: {DEFAULT_PORT}")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the dashboard in the default browser after the server starts.",
    )
    return parser.parse_args()


def build_server(host: str, port: int) -> ThreadingHTTPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(WORKSPACE_ROOT))
    return ThreadingHTTPServer((host, port), handler)


def main() -> int:
    args = parse_args()
    url = f"http://{args.host}:{args.port}/index.html"

    try:
        with build_server(args.host, args.port) as server:
            print(f"Serving Pacific Epidemic Intelligence Atlas at {url}", flush=True)
            print("Press Ctrl+C to stop the server.", flush=True)
            if not args.no_browser:
                webbrowser.open(url)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nStopping dashboard server.", flush=True)
    except OSError as error:
        print(f"Could not start dashboard server on {args.host}:{args.port}: {error}", flush=True)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())