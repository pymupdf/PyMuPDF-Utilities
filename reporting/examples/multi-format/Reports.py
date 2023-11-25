# written by Green

import io
import sys
from pprint import pprint

import fitz

HEADER_RECT = None
FOOTER_RECT = None
HEADER_LAST_COL_RECT = None


class Block(object):
    def __init__(
        self, html=None, archive=None, report=None, css=None, story=None
    ):
        if not report:
            raise ValueError("need a report for creating this object")
        self.html = html
        self.report = report
        self.archive = self.report.archive
        if archive is not None:
            self.archive.add(archive)

        self.css = css if css else ""
        if self.report.css is not None:  # prepend CSS of owning report
            self.css = self.report.css + self.css

        self.story = story
        self.reset = True  # this building must be reset each time
        self.advance = True

    def make_story(self):
        if not isinstance(self.story, fitz.Story):
            self.story = fitz.Story(
                self.html, user_css=self.css, archive=self.archive
            )


class ImageBlock(object):
    def __init__(
        self,
        url=None,
        archive=None,
        report=None,
        css=None,
        story=None,
        width=None,
        height=None,
    ):
        if not report:
            raise ValueError("need a report for creating this object")

        w, h = width, height
        if w == h:
            if w != None:
                self.html = f'<img src="{url}" width={width} height={height}/>'
            else:
                self.html = f'<img src="{url}" width=100 height=100/>'
        elif w == None:
            self.html = f'<img src="{url}" height={height}/>'
        elif h == None:
            self.html = f'<img src="{url}" width={width}/>'
        else:
            self.html = f'<img src="{url}" width={width} height={height}/>'

        self.archive = fitz.Archive(archive) if archive else fitz.Archive(".")
        self.story = story
        self.report = report
        self.advance = True
        self.css = css if css else ""
        if self.report.css is not None:  # prepend CSS of owning report
            self.css = self.report.css + self.css

    def make_story(self):
        if not isinstance(self.story, fitz.Story):
            self.story = fitz.Story(
                self.html, user_css=self.css, archive=self.archive
            )


class Table(object):
    def __init__(
        self,
        report=None,
        html=None,
        story=None,
        fetch_rows=None,
        top_row=None,
        last_row_bg=None,
        archive=None,
        css=None,
        alternating_bg=None,
    ):
        if not report:
            raise ValueError("need a report for creating this object")
        self.report = report
        self.mediabox = report.mediabox
        self.where = report.where
        self.html = html
        self.story = story
        self.top_row = top_row
        self.advance = True

        # prepend archive of owning report
        self.archive = self.report.archive
        if archive is not None:
            self.archive.add(archive)

        self.css = css if css else ""
        if self.report.css is not None:  # prepend CSS of owning report
            self.css = self.report.css + self.css

        self.fetch_rows = fetch_rows
        self.HEADER_RECT = []
        self.HEADER_BLOCKS = None
        self.HEADER_FONT = None
        self.HEADER_PATHS = None
        self.header_tops = []  # list where.y0 coordinates
        self.reset = False  # this building must not be reset
        self.alternating_bg = alternating_bg
        self.last_row_bg = last_row_bg

    def extract_header(self):
        """Extract top row from table for later reproduction."""
        global HEADER_RECT  # the rectangle wrapping the top row
        global HEADER_LAST_COL_RECT  # the rectangle of last column in top row

        def recorder(pos):
            """small recorder function for determining the top row rectangle."""
            global HEADER_RECT
            global HEADER_LAST_COL_RECT

            if pos.depth == 2:  # select column in template
                HEADER_LAST_COL_RECT = fitz.Rect(pos.rect)

            if pos.open_close != 2:  # only look at "close"
                return
            if pos.id != pos.header:  # only look at 'id' of top row
                return
            HEADER_RECT = fitz.Rect(pos.rect)  # found:store header rect

        # write first occurrence of table to find header information
        fp = io.BytesIO()  # for memory PDF
        writer = fitz.DocumentWriter(fp)
        self.story.reset()

        current_section = self.report.get_current_section()
        current_mediabox = (
            fitz.paper_rect(current_section[2])
            if len(current_section) == 3
            else self.mediabox
        )
        self.where = self.report.set_margin(current_mediabox)

        dev = writer.begin_page(current_mediabox)

        # customize for mulit columns
        columns = (
            current_section[1]
            if len(current_section) >= 2
            else self.report.COLS
        )  # get columns from parent report
        CELLS = []
        if columns > 1:  # n columns
            TABLE = fitz.make_table(self.where, cols=columns, rows=1)  # layouts
            CELLS = [TABLE[i][j] for i in range(1) for j in range(columns)]
            CELLS.reverse()
        else:
            CELLS = [self.where]

        for CELL in CELLS:
            _, _ = self.story.place(CELL)
            self.story.element_positions(
                recorder, {"page": 0, "header": self.top_row}
            )  # get rectangle of top row
            self.HEADER_RECT.append(HEADER_RECT)

        if (
            HEADER_LAST_COL_RECT != None
            and HEADER_LAST_COL_RECT.x1 > HEADER_RECT.x1
        ):  # check last column is over top row
            raise ValueError(
                "Not enough to place it in {0} columns".format(columns)
            )

        self.story.draw(dev)
        writer.end_page()
        writer.close()

        # re-open temp PDF and load page 0
        doc = fitz.open("pdf", fp)
        page = doc[0]
        paths = [
            p for p in page.get_drawings() if p["rect"].intersects(HEADER_RECT)
        ]
        blocks = page.get_text(
            "dict", clip=HEADER_RECT, flags=fitz.TEXTFLAGS_TEXT
        )["blocks"]
        if blocks:  # extract the font name for text in the header
            self.HEADER_FONT = page.get_fonts()[0][3]
        doc.close()
        self.story.reset()
        # self.HEADER_RECT = +HEADER_RECT
        self.HEADER_RECT.reverse()
        HEADER_RECT = None
        self.HEADER_BLOCKS = blocks
        self.HEADER_PATHS = paths
        return

    def make_story(self):
        if self.story == None:
            self.story = fitz.Story(
                self.html, user_css=self.css, archive=self.archive
            )
            body = self.story.body
            table = body.find("table", None, None)
            if table == None:
                raise ValueError("no table found in the HTML")

            templ = body.find(None, "id", "template")  # locate template row
            if templ == None and callable(self.fetch_rows):
                raise ValueError("cannot find row 'template'")

            if callable(self.fetch_rows):
                rows = self.fetch_rows()
                fields = rows[0]
                rows = rows[1:]
            else:
                rows = []
            for j, data in enumerate(rows):
                row = templ.clone()  # clone model row
                if isinstance(self.alternating_bg, (tuple, list)):
                    if len(self.alternating_bg) >= 2:
                        bg_color = self.alternating_bg[
                            j % len(self.alternating_bg)
                        ]
                        row.set_properties(bgcolor=bg_color)
                    elif len(self.alternating_bg) == 1:
                        row.set_properties(bgcolor=self.alternating_bg[0])
                elif isinstance(self.alternating_bg, str):
                    row.set_properties(bgcolor=self.alternating_bg)
                else:
                    bg_color = "#fff"
                if self.last_row_bg and j == len(rows) - 1:
                    row.set_properties(bgcolor=self.last_row_bg)
                for i in range(len(data)):
                    text = (
                        str(data[i]).replace("\\n", "\n").replace("<br>", "\n")
                    )
                    tag = row.find(None, "id", fields[i])
                    if tag == None:
                        raise ValueError(
                            f"id '{fields[i]}' not in template row."
                        )
                    if bg_color:
                        tag.set_properties(bgcolor=bg_color)
                    if text.startswith("|img|"):
                        _ = tag.add_image(text[5:])
                    else:
                        _ = tag.add_text(text)
                table.append_child(row)
                # print("row appended")

            if templ:
                templ.remove()
        else:
            body = self.story.body
            body.add_style("margin-top:0;")

        if self.top_row != None:
            self.extract_header()

    def repeat_header(self, page, rect, font_dict):
        """Recreate the top row header of the table on given page, rectangle"""

        def make_fontname(page, font, font_dict):
            xref, refname, pno = font_dict[font]
            if pno == page.number:
                return refname
            font_items = page.get_fonts()
            refnames = [item[4] for item in font_items if item[3] == font]
            if refnames != []:
                return refnames[0]
            refnames = [item[4] for item in font_items]
            i = 1
            fontname = "F1"
            while fontname in refnames:
                i += 1
                fontname = f"F{i}"
            font_ex = page.parent.extract_font(xref)
            font_buff = font_ex[-1]
            page.insert_font(fontname=fontname, fontbuffer=font_buff)
            return fontname

        mat = self.HEADER_RECT[0].torect(rect)

        for p in self.HEADER_PATHS:
            for item in p["items"]:
                if item[0] == "l":
                    page.draw_line(
                        item[1] * mat, item[2] * mat, color=p["color"]
                    )
                elif item[0] == "re":
                    page.draw_rect(
                        item[1] * mat, color=p["color"], fill=p["fill"]
                    )

        fontname = make_fontname(page, self.HEADER_FONT, font_dict)
        for block in self.HEADER_BLOCKS:
            for line in block["lines"]:
                for span in line["spans"]:
                    point = fitz.Point(span["origin"]) * mat
                    page.insert_text(
                        point,
                        span["text"],
                        fontname=fontname,
                        fontsize=span["size"],
                    )


class Report(object):
    def __init__(
        self,
        mediabox,
        margins=None,
        logo=None,
        columns=1,
        header=[],
        footer=[],
        css=None,
        archive=None,
        font_families=None,
    ):
        self.mediabox = mediabox
        self.margins = margins
        self.columns = columns  # column number, 2 as default
        self.sections = []  # sections list
        self.header = header
        self.footer = footer
        self.sindex = 0
        self.COLS = columns
        self.archive = fitz.Archive(archive) if archive else fitz.Archive(".")
        self.HEADER_RECT = None
        self.FOOTER_RECT = None

        self.css = css if css else ""
        self.where = self.set_margin(self.mediabox)

        if isinstance(logo, str):
            self.logo_file = logo
            self.logo_rect = fitz.Rect(
                self.where.tl, self.where.x0 + 100, self.where.y0 + 100
            )
        else:
            self.logo_file = None

        if font_families and isinstance(font_families, dict):
            for family, fitz_code in font_families.items():
                temp = [
                    k
                    for k in fitz.fitz_fontdescriptors.keys()
                    if k.startswith(fitz_code)
                ]
                if temp == []:
                    print(
                        f"'{fitz_code}' not in pymupdf-fonts - ignored",
                        file=sys.stderr,
                    )
                    continue
                self.css = fitz.css_for_pymupdf_font(
                    fitz_code, CSS=self.css, archive=self.archive, name=family
                )

    def set_margin(self, rect):
        if self.margins == None:
            result = rect + (36, 36, -36, -50)
        else:
            L, T, R, B = self.margins
            result = rect + (L, T, -R, -B)
        return result

    def current(self):
        if isinstance(self.sections[self.sindex], list):
            return self.sections[self.sindex][0]
        return self.sections[self.sindex]

    def check_cols(self):
        if len(self.sections) > self.sindex and isinstance(
            self.sections[self.sindex], list
        ):
            if len(self.sections[self.sindex]) < 2:
                BufferError("Size is not matched")

            if not isinstance(self.sections[self.sindex][1], int):
                TypeError("Columns type error")

            self.COLS = self.sections[self.sindex][1]
            return True
        else:
            return False  # continue

    def get_pagerect(self, old_pagebox):
        if len(self.sections) > self.sindex and isinstance(
            self.sections[self.sindex], list
        ):
            if len(self.sections[self.sindex]) < 3:
                return old_pagebox, False

            if not isinstance(self.sections[self.sindex][2], str):
                TypeError("Paper Type error")

            pagebox = fitz.paper_rect(self.sections[self.sindex][2])
            return pagebox, True
        else:
            return old_pagebox, False

    def get_current_section(self, index=None):
        if index == None:
            index = self.sindex
        return (
            self.sections[index]
            if isinstance(self.sections[index], list)
            else [self.sections[index]]
        )

    def isover(self):
        return self.sindex >= len(self.sections)

    def run(self, filename):
        # init
        if self.header == None:  # set empty list
            self.header = []
        if self.footer == None:
            self.footer = []

        self.sindex = 0
        footer_height = 30.0
        header_height = 0.0
        more = True  # need more pages or not
        pno = 0
        section_mediabox = self.mediabox
        section_mediabox, _ = self.get_pagerect(section_mediabox)  # init

        fileobject = io.BytesIO()  # let DocumentWriter write to memory
        writer = fitz.DocumentWriter(fileobject)  # define output writer

        if len(self.header):
            for hElement in self.header:
                if not isinstance(hElement.story, fitz.Story):
                    hElement.make_story()
                _, self.HEADER_RECT = hElement.story.place(self.where)

                if (
                    header_height < self.HEADER_RECT[3]
                ):  # select max value for header height
                    header_height = self.HEADER_RECT[3]

            self.HEADER_RECT = tuple(
                [  # Header Rect
                    self.HEADER_RECT[0],
                    self.HEADER_RECT[1],
                    self.HEADER_RECT[2],
                    header_height,
                ]
            )

        if len(self.footer):  # calculate Footer rectangle
            for fElement in self.footer:
                if not isinstance(fElement.story, fitz.Story):
                    fElement.make_story()
                _, self.FOOTER_RECT = fElement.story.place(self.mediabox)

                if footer_height < self.FOOTER_RECT[3]:
                    footer_height = self.FOOTER_RECT[3]  # set footer height max

            self.FOOTER_RECT = tuple(
                [  # footer rect
                    self.where.x0,
                    self.where.y1 - footer_height,
                    self.where.x1,
                    self.mediabox.y1,
                ]
            )

        self.COLS = self.columns  # init COLS
        self.current().make_story()
        _ = self.check_cols()

        while more:  # loop until all input text has been written out
            dev = writer.begin_page(
                section_mediabox
            )  # prepare a new output page

            self.where = self.set_margin(section_mediabox)
            self.where.y0 = (
                self.where.y0
                if self.where.y0 > header_height
                else header_height
            )
            self.where.y1 = (
                self.where.y1
                if (section_mediabox.y1 - self.where.y1) > footer_height
                else section_mediabox.y1 - footer_height
            )

            ROWS = 1  # default
            TABLE = fitz.make_table(
                self.where, cols=self.COLS, rows=ROWS
            )  # layouts
            CELLS = [TABLE[i][j] for i in range(ROWS) for j in range(self.COLS)]
            CELL_LENGTH = len(CELLS)  # get Length of Cells

            more_cell = True
            cell_index = 0  # columns index
            where = CELLS[cell_index]  # temp where

            if len(self.header) != 0:  # draw Header
                for hElement in self.header:
                    hElement.story = None  # delete
                    hElement.make_story()
                    hElement.story.place(self.HEADER_RECT)
                    hElement.story.draw(dev, None)

            while (
                more_cell
            ):  # loop until it reach out max column count in one page
                # content may be complete after any cell, ...
                if (
                    hasattr(self.current(), "HEADER_RECT")
                    and len(self.current().HEADER_RECT) != 0
                ):  # this section store Table headers positions
                    self.current().header_tops.append(
                        {
                            "pno": pno,
                            "left": self.current().HEADER_RECT[cell_index].x0,
                            "top": where.y0,
                        }
                    )  # issue
                    if (
                        len(self.current().header_tops) > 1
                    ):  # skip first piece of table because that has a top row
                        where.y0 += (
                            self.current().HEADER_RECT[cell_index].height
                        )  # move beginning of table as much as top row height
                    where.y1 = round(where.y1 - 0.5)  # make integer for safety

                if more:  # so check this status
                    more, filled = self.current().story.place(
                        where
                    )  # draw current section
                    self.current().story.draw(dev, None)

                if more == 0:
                    if filled[3] < self.where.y1:  # check and add section/block
                        if self.current().advance:
                            where.y0 = filled[
                                3
                            ]  # update latest position for next drawing
                    self.sindex += 1

                    if not self.isover():
                        self.current().make_story()

                    section_mediabox, is_newpage = self.get_pagerect(
                        section_mediabox
                    )
                    if self.check_cols() or is_newpage:
                        more_cell = False  # set End value to create new page
                else:  # check and select next column
                    cell_index += 1

                if (
                    cell_index is CELL_LENGTH
                ):  # check whether one page is completed
                    more_cell = False
                else:
                    where = CELLS[cell_index]

                more = True
                if self.isover():  # check completion of PDF
                    more = False
                    break

            if len(self.footer) != 0:  # draw Header
                for fElement in self.footer:
                    fElement.story = None  # delete
                    fElement.make_story()
                    fElement.story.place(self.FOOTER_RECT)
                    fElement.story.draw(dev, None)

            writer.end_page()  # finish the PDF page
            pno += 1
        writer.close()

        doc = fitz.open("pdf", fileobject)
        page_count = doc.page_count
        font_dict = dict()

        for page in doc:  # draw footer with page number
            page.wrap_contents()

            for item in page.get_fonts():
                xref, _, _, fontname, refname, _ = item
                font_dict[fontname] = (xref, refname, page.number)

            btm_rect = fitz.Rect(
                self.where.x0, page.rect.y1 - 30, page.rect.x1, page.rect.y1
            )
            page.insert_textbox(  # draw page number
                btm_rect,
                f"Page {page.number+1} of {page_count}",
                align=fitz.TEXT_ALIGN_CENTER,
            )

        for i in range(0, len(self.sections)):
            self.sindex = i
            if (
                hasattr(
                    self.current(), "HEADER_RECT"
                )  # check whether HEADER_RECT exists and be available
                and len(self.current().HEADER_RECT) != 0
            ):
                _ = self.check_cols()  # init COLS
                header_rect = self.current().HEADER_RECT

                self.current().header_tops.pop(
                    0
                )  # remove first element not draw in following loop
                for i in range(
                    0, len(self.current().header_tops)
                ):  # draw Top Row
                    header = self.current().header_tops[i]
                    page = doc.load_page(header["pno"])

                    x1 = (
                        header["left"] + header_rect[(i + 1) % self.COLS].width
                    )  # get right
                    y1 = (
                        header["top"] + header_rect[(i + 1) % self.COLS].height
                    )  # get bottom

                    self.current().repeat_header(
                        page,
                        fitz.Rect(header["left"], header["top"], x1, y1),
                        font_dict,
                    )

        doc.subset_fonts()
        doc.ez_save(filename)  # save
