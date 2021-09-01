import argparse
import logging
from urllib.parse import urljoin

from operatorcert import pyxis, store_results

LOGGER = logging.getLogger("operator-cert")


def setup_argparser() -> argparse.ArgumentParser:
    """
    Setup argument parser

    Returns:
        Any: Initialized argument parser
    """
    parser = argparse.ArgumentParser(
        description="Get the Certification Project related data"
    )
    parser.add_argument(
        "--cert-project-id",
        help="Identifier of certification project from Red Hat Connect",
    )
    parser.add_argument(
        "--pyxis-url",
        default="https://pyxis.engineering.redhat.com/",
        help="Base URL for Pyxis container metadata API",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    return parser


def get_cert_project_related_data(pyxis_url: str, cert_project_id: str) -> None:
    rsp = pyxis.get(
        urljoin(
            pyxis_url,
            f"/v1/projects/certification/id/{cert_project_id}",
        )
    )

    rsp.raise_for_status()

    cert_project = rsp.json()

    try:
        results = {
            "isv_pid": cert_project["container"]["isv_pid"],
            "repo_name": cert_project["container"]["repository_name"],
            "dist_method": cert_project["container"]["distribution_method"],
            "org_id": cert_project["org_id"],
        }
    except KeyError as e:
        logging.error("Expected data not found in Certification Project!")
        raise e

    store_results(results)


def main() -> None:
    parser = setup_argparser()
    args = parser.parse_args()

    log_level = "INFO"
    if args.verbose:
        log_level = "DEBUG"
    logging.basicConfig(level=log_level)

    get_cert_project_related_data(args.pyxis_url, args.cert_project_id)


if __name__ == "__main__":
    main()
