# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Main module for the FlowKit service."""

try:
    from aali.flowkit.config._config import CONFIG
    import uvicorn
except ImportError:
    raise ImportError("Please install uvicorn to run the service: pip install aali-flowkit-python[all]")
import argparse
import multiprocessing
from urllib.parse import urlparse


def parse_cli_args():
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, required=False, default="0.0.0.0", help="The host to run the service on. By default 0.0.0.0"
    )
    parser.add_argument(
        "--port", type=int, required=False, default="50052", help="The port to run the service on. By default 50052"
    )
    parser.add_argument(
        "--workers", type=int, required=False, default="4", help="The number of workers to use. By default 4"
    )
    parser.add_argument("--use-ssl", required=False, default=False, help="Enable SSL for the service. By default False")
    parser.add_argument("--ssl-keyfile", type=str, required=False, help="The SSL key file path")
    parser.add_argument("--ssl-certfile", type=str, required=False, help="The SSL certificate file path")
    args, _ = parser.parse_known_args()
    return args


def handle_legacy_port_config():
    """Handle legacy port configuration."""
    if CONFIG.flowkit_python_address != "" or CONFIG.flowkit_python_address:
        return CONFIG.flowkit_python_address
    if CONFIG.flowkit_python_endpoint != "" or CONFIG.flowkit_python_endpoint:
        return CONFIG.flowkit_python_endpoint


def substitute_empty_values(args):
    """Substitute the empty values with configuration values."""
    CONFIG.flowkit_python_address = (
        f"{args.host}:{args.port}" if args.host is not None and args.port is not None else CONFIG.flowkit_python_address
    )
    CONFIG.flowkit_python_workers = args.workers or CONFIG.flowkit_python_workers
    CONFIG.use_ssl = args.use_ssl or CONFIG.use_ssl
    CONFIG.ssl_cert_private_key_file = args.ssl_keyfile or CONFIG.ssl_cert_private_key_file
    CONFIG.ssl_cert_public_key_file = args.ssl_certfile or CONFIG.ssl_cert_public_key_file
    return


def main():
    """Run entrypoint for the FlowKit service."""
    # Always parse args, but only use them conditionally
    args = parse_cli_args()

    if not CONFIG.extract_config_from_azure_key_vault:
        # Substitute the empty values with configuration values
        substitute_empty_values(args)

    address = handle_legacy_port_config()
    # Add scheme if missing
    if not address.startswith(("http://", "https://")):
        address = "http://" + address
    host = urlparse(address).hostname or args.host
    port = urlparse(address).port or args.port

    # Run the service
    uvicorn.run(
        "aali.flowkit.flowkit_service:flowkit_service",
        host=host,
        port=port,
        workers=CONFIG.flowkit_python_workers,
        ssl_keyfile=CONFIG.ssl_cert_private_key_file if CONFIG.use_ssl else None,
        ssl_certfile=CONFIG.ssl_cert_public_key_file if CONFIG.use_ssl else None,
    )


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
