import typer

from .manual import app as manual_app
from .package import app as package_app


app = typer.Typer()

app.add_typer(manual_app)
app.add_typer(package_app)

app()
