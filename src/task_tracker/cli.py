"""CLI interface for Task Tracker."""

import click


@click.command()
@click.version_option()
def cli():
    """Task Tracker - A simple CLI demonstrating ATDD."""
    click.echo("Hello, Task Tracker!")


if __name__ == "__main__":
    cli()
