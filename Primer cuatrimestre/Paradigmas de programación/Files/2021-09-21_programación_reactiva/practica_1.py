import asyncio
import io

from functools import partial
from typing import Dict, Union, Tuple, Optional

import aiohttp

from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from rx import create
from rx.core import Observer
from tkinter import Canvas, Tk, Listbox, Button, Entry, HORIZONTAL, END
from tkinter.ttk import Progressbar


class CustomProgressbar(Progressbar, Observer):
    def __init__(self, *args, **kwargs):
        Progressbar.__init__(self, *args, **kwargs)
        Observer.__init__(self)
        self._shown = False

    def on_next(
        self, value: Union[int, Tuple[Optional[str], Optional[bytes]]]
    ) -> None:
        if isinstance(value, int):
            self['value'] = 0
            self.configure(length=value)
            self.grid()
            return
        self.step()

    def on_completed(self) -> None:
        self.grid_remove()


class CustomListbox(Listbox, Observer):
    def __init__(self, *args, **kwargs):
        Listbox.__init__(self, *args, **kwargs)
        Observer.__init__(self)

    def on_next(
        self, value: Union[int, Tuple[Optional[str], Optional[bytes]]]
    ) -> None:
        if isinstance(value, int):
            self.delete(0, END)
            return

        alt, img = value
        if not alt or not img:
            return

        self.insert(0, alt)


class CustomEntry(Entry, Observer):
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        Observer.__init__(self)

    def on_next(
        self, value: Union[int, Tuple[Optional[str], Optional[bytes]]]
    ) -> None:
        if isinstance(value, int):
            self.grid_remove()

    def on_completed(self) -> None:
        self.configure(background="white")
        self.grid()


class CustomButton(Button, Observer):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        Observer.__init__(self)

    def on_next(
        self, value: Union[int, Tuple[Optional[str], Optional[bytes]]]
    ) -> None:
        if isinstance(value, int):
            self.grid_remove()

    def on_completed(self) -> None:
        self.grid()


class Gui(object):
    def __init__(self, loop, interval=1/120):
        self.__alt_img_map = dict()

        self.window = Tk()
        self.window.title = 'Image viewer'

        self.window.loop = loop
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.tasks = []
        self.window.tasks.append(loop.create_task(self.updater(interval)))

        # Left Side
        self.entry = entry = CustomEntry(font=('Arial', 12))
        entry.grid(column=0, row=0, sticky='nsew')

        self.search_btn = btn = CustomButton(
            text='Buscar', command=self.on_submit
        )
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

    def _get_images(
        self, entry: str, observer: Observer, scheduler
    ) -> Dict[str, Dict[str, str]]:
        async def _run():
            async with aiohttp.ClientSession() as session:
                content = await session.get(entry)
                content = await content.text()

                soup = BeautifulSoup(content, 'html.parser')
                src_alt_map = dict()
                alts = set()
                tasks = list()

                for img in soup.find_all('img'):
                    try:
                        alt = img["alt"]
                        src = img["src"]
                    except KeyError:
                        continue

                    if (
                        not alt.strip() or alt in alts
                        or not src.strip() or src in src_alt_map
                    ):
                        continue

                    src_alt_map[src] = alt
                    alts.add(alt)
                    tasks.append(session.get(src))

                total = len(tasks)
                observer.on_next(total)

                for coro in asyncio.as_completed(tasks):
                    try:
                        resp = await coro
                        img_bytes = await resp.read()
                        img_alt = src_alt_map[str(resp.url)]
                    except Exception as e:
                        print(str(e.with_traceback(None)))
                        img_alt, img_bytes = None, None
                    observer.on_next((img_alt, img_bytes))
                observer.on_completed()

        self.window.loop.create_task(_run())

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
        observable.subscribe(on_next=self.on_next)

    def on_next(
        self, value: Union[int, Tuple[Optional[str], Optional[str]]]
    ) -> None:
        if isinstance(value, int):
            self.__alt_img_map = dict()
            return

        alt, img = value
        if not alt or not img:
            return

        self.__alt_img_map[alt] = img

    def on_list_select(self, _event):
        curr = self.list.curselection()
        if not curr:
            return

        value = str(self.list.get(curr))

        img = ImageTk.PhotoImage(
            Image.open(io.BytesIO(self.__alt_img_map[value]))
        )

        self.canvas.background = img
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.create_image(
            width/2, height/2, anchor='center', image=self.canvas.background
        )

    async def updater(self, interval):
        while True:
            self.window.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.window.tasks:
            task.cancel()
        self.window.loop.stop()
        self.window.destroy()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = Gui(loop)
    loop.run_forever()
    loop.close()
