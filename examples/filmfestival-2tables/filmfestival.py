import sqlite3

import fitz
from fitz.reports import Report, Block, Table

# -----------------------------------------------------------------------------
# HTML sources
# -----------------------------------------------------------------------------
HEADER = """<h1 style="text-align:center">Hook Norton Film Festival</h1>"""

# HTML for movies
FILM_HTML = """
<style>
table {border-spacing: 0;}
td,th {border: .2px solid #bbb;}
td {padding-left: 3px;padding-right: 3px;}
</style>
<h2>Films and Actors by Movie Title</h2>
<table>
    <tr id="toprow" style="background-color: #ffff00">
        <th>Film Title</th>
        <th>Director</th>
        <th>Publication Year</th>
        <th>Actors</th>
    </tr>
    <tr id="template" style="margin-top: 2px;">
        <td id="film"></td>
        <td id="director"></td>
        <td style="text-align: center;" id="year"></td>
        <td id="actors"></td>
    </tr>
</table>
"""

# HTML for actors
ACTOR_HTML = """
<style>
table {border-spacing: 0;}
td,th {border: .2px solid #ccc;}
td {padding-left: 3px;padding-right: 3px;}
</style>
<h2>Actors and their Films</h2>
<table>
    <tr id="toprow" style="background-color: #ffff00">
        <th>Actor</th>
        <th>Movie Participation</th>
    </tr>
    <tr id="template" style="margin-top: 2px;">
        <td id="actor"></td>
        <td id="films"></td>
    </tr>
</table>
"""

mediabox = fitz.paper_rect("a4")
report = Report(mediabox, font_families={"sans-serif": "ubuntu", "serif": "ubuntu"})
header = Block(html=HEADER, report=report)


def get_film_items():
    """Return the table rows for films."""
    dbfilename = "filmfestival.db"  # the SQLITE database file name
    database = sqlite3.connect(dbfilename)  # open database

    # SQL for the films
    cursor_films = database.cursor()  # cursor for selecting the films
    select_films = """SELECT title, director, year FROM films ORDER BY title"""

    # SQL for the actors
    cursor_casts = database.cursor()  # cursor for selecting actors per film
    select_casts = """SELECT name FROM actors WHERE film = "%s" ORDER BY name"""

    cursor_films.execute(select_films)  # execute cursor, and ...
    films = cursor_films.fetchall()  # read out what was found

    # we will return this list:
    rows = [["film", "director", "year", "actors"]]

    for film_row in films:
        film_row = list(film_row)
        title = film_row[0]  # take film title for actor seletion
        cursor_casts.execute(select_casts % title)  # execute cursor
        casts = cursor_casts.fetchall()  # read actors for the film
        # each actor name appears in its own tuple, so extract it from there
        # actors = "\n".join([f"{chr(0xb7)} " + c[0] for c in casts])
        actors = ", ".join([c[0] for c in casts])
        film_row.append(actors)
        rows.append(film_row)

    return rows


def get_actor_items():
    dbfilename = "filmfestival.db"  # the SQLITE database file name
    database = sqlite3.connect(dbfilename)  # open database

    # SQL for the films
    cursor_films = database.cursor()  # cursor for selecting films
    select_films = """SELECT year FROM films where title = "%s" """

    # SQL for the actors
    cursor_casts = database.cursor()  # cursor for selecting actors
    select_casts = """SELECT name, film FROM actors ORDER BY name, film"""

    cursor_casts.execute(select_casts)  # execute cursor, and ...
    actor_rows = cursor_casts.fetchall()  # read all actor, film rows
    rows = [["actor", "films"]]
    actor_info = {}
    for actor_row in actor_rows:
        actor, film = actor_row
        films = actor_info.get(actor, [])
        cursor_films.execute(select_films % film)
        year_info = cursor_films.fetchall()
        if year_info:  # film found - extract the year
            year = year_info[0][0]
        else:
            year = "????"  # else indicate missing data
        films.append(f"{film} ({year})")
        actor_info[actor] = films
    for actor, films in actor_info.items():
        rows.append([actor, ", ".join(films)])

    return rows


film_items = Table(
    report=report,
    html=FILM_HTML,
    fetch_rows=get_film_items,
    top_row="toprow",
)

actor_items = Table(
    report=report,
    html=ACTOR_HTML,
    fetch_rows=get_actor_items,
    top_row="toprow",
)

report.sections = [film_items, actor_items]
report.header = [header]
report.run("output.pdf")
