import typer

from embedding_search.commands import download, embed, index, prepare

app = typer.Typer()

app.command()(download.download)
app.command()(embed.embed)
app.command()(index.index)

app.add_typer(prepare.app, name="prepare")

if __name__ == "__main__":
    app()
