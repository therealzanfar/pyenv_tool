#! /usr/bin/env python3

"""Console Entry Point for pyenv_tool Utility."""

import logging
import sys

import click

from pyenv_tool.cli import CLICK_CONTEXT, setup_logging


@click.command(context_settings=CLICK_CONTEXT)
@click.option("-v", "--verbose", count=True)
def cli_main(verbose: int = 0) -> int:
    """Convienience wrapper for common pyenv operations."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
