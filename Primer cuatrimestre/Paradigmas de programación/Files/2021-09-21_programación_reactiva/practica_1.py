import asyncio
import io

from functools import partial
from typing import Dict

import aiohttp

from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from rx import create
from rx.core import Observer
from tkinter import Canvas, Tk, Listbox, Button, Entry, HORIZONTAL, END
from tkinter.ttk import Progressbar


class CustomProgressbar(Progressbar, Observer):
    def __init__(self, *args, **kwargs):
        self._shown = False
        return super().__init__(*args, **kwargs)

    def on_next(self, value) -> None:
        if not self._shown:
            self.grid()
            self._shown = True
        self.step()

    def on_completed(self) -> None:
        self.grid_remove()
        self._shown = False


class CustomListbox(Listbox, Observer):
    def __init__(self, *args, **kwargs):
        self._completed = True
        return super().__init__(*args, **kwargs)

    def on_next(self, value) -> None:
        if self._completed is True:
            self.delete(0, END)
            self._completed = False
        self.insert(0, value)

    def on_completed(self) -> None:
        self._completed = True


class CustomEntry(Entry, Observer):
    def __init__(self, *args, **kwargs):
        self._removed = False
        return super().__init__(*args, **kwargs)

    def on_next(self, value) -> None:
        if not self._removed:
            self.grid_remove()
            self._removed = True

    def on_completed(self) -> None:
        self.configure(background="white")
        self.grid()
        self._removed = False


class CustomButton(Button, Observer):
    def __init__(self, *args, **kwargs):
        self._removed = False
        return super().__init__(*args, **kwargs)

    def on_next(self, value) -> None:
        if not self._removed:
            self.grid_remove()
            self._removed = True

    def on_completed(self) -> None:
        self.grid()
        self._removed = False


class Gui:
    def __init__(self):
        self.__alt_img_map = dict()

        self.window = Tk()
        self.window.title = 'Image viewer'

        # Left Side
        self.entry = entry = CustomEntry(font=('Arial', 12))
        entry.grid(column=0, row=0, sticky='nsew')

        self.search_btn = btn = CustomButton(text='Buscar', command=self.on_submit)
        btn.grid(column=2, row=0, sticky='nsew')

        self.progress = progress = CustomProgressbar(
            orient=HORIZONTAL, length=100, mode='determinate'
        )
        progress.grid(column=0, row=0, columnspan=3, sticky='nsew')
        progress.grid_remove()

        self.list = listb = CustomListbox(font=('Arial', 12))
        listb.bind('<<ListboxSelect>>', self.on_list_select)
        listb.grid(column=0, row=1, columnspan=3, sticky='nsew')
        # End left side

        # Right side
        self.canvas = canvas = Canvas(background='black')
        canvas.grid(column=3, row=0, rowspan=2, sticky='nsew')
        # End right side

        self.window.columnconfigure(0, weight=2)
        self.window.columnconfigure(3, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.window.mainloop()

    def _get_images(
        self, entry: str, observer: Observer, scheduler
    ) -> Dict[str, Dict[str, str]]:
        async def _run():
            async with aiohttp.ClientSession() as session:
                content = await session.get(entry)
                content = await content.text()

                soup = BeautifulSoup(content, 'html.parser')
                img_alt_map = dict()
                img_src_map = dict()
                img_tasks = list()

                for img in soup.find_all('img'):
                    try:
                        alt = img["alt"]
                        src = img["src"]
                    except KeyError:
                        continue
                    img_alt_map[alt] = {"src": src}
                    img_src_map[src] = alt
                    img_tasks.append(session.get(src))

                self.progress.configure(length=len(img_tasks))
                self.progress['value'] = 0
                self.window.update_idletasks()

                for coro in asyncio.as_completed(img_tasks):
                    resp = await coro
                    img_bytes = await resp.read()
                    img_alt = img_src_map[str(resp.url)]
                    img_alt_map[img_alt]["img"] = img_bytes
                    observer.on_next(img_alt)
                    # self.window.update_idletasks()
                    self.window.update()

                await asyncio.sleep(3)

                observer.on_completed()
            self.__alt_img_map = img_alt_map
        asyncio.run(_run())

    def on_submit(self):
        entry = self.entry.get()

        if not entry:
            self.entry.configure(background="red")
            self.window.update_idletasks()
            return

        func = partial(self._get_images, entry)
        observable = create(func)
        observable.subscribe(self.progress)
        observable.subscribe(self.list)
        observable.subscribe(self.entry)
        observable.subscribe(self.search_btn)

    def on_list_select(self, _event):
        curr = self.list.curselection()
        if not curr:
            return

        value = str(self.list.get(curr))

        img = ImageTk.PhotoImage(
            Image.open(io.BytesIO(self.__alt_img_map[value]["img"]))
        )

        self.canvas.background = img
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.create_image(
            width/2, height/2, anchor='center', image=self.canvas.background
        )


if __name__ == '__main__':
    Gui()
