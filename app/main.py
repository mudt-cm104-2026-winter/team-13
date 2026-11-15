"""Reading List: our team reading tracker.

What happens where:
- main.py      the web part: which address shows what (the "routes")
- storage.py   where the entries are kept
- templates/   the HTML page
- static/      the stylesheet
"""

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import storage

HERE = Path(__file__).parent

app = FastAPI(title="Reading List")
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
templates = Jinja2Templates(directory=HERE / "templates")


@app.get("/")
def show_list(request: Request):
    """The start page: the form and all entries."""
    return templates.TemplateResponse(
        request, "index.html", {"entries": storage.all_entries()}
    )


@app.post("/add")
def add(title: str = Form(...), author: str = Form(...)):
    """The form on the start page sends book title and author here."""
    storage.add_entry(title=title.strip(), author=author.strip())
    # Back to the start page. 303 tells the browser: load it with GET.
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{entry_id}")
def delete(entry_id: int):
    """Remove a book entry by its id."""
    storage.delete_entry(entry_id)
    return RedirectResponse("/", status_code=303)


@app.post("/clear")
def clear():
    """Remove all book entries."""
    storage.clear_entries()
    return RedirectResponse("/", status_code=303)
