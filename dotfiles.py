import click

from features import FolderContentSync


@click.command()
@click.option("--config", default="home.json", help="see config.schema.json")
@click.option(
    "--source", help="parent folder where files in --config are expected to be found"
)
@click.argument("dest")
def main(config, source, dest):
    FolderContentSync(config, source, dest).install()


if __name__ == "__main__":
    main()
