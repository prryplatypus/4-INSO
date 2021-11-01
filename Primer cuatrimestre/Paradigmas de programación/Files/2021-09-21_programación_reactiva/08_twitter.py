from os import getenv
from tkinter import Button, Entry, Text, Tk, END

from rx import create, operators
from rx.core import Observer
from rx.scheduler.mainloop import TkinterScheduler

import tweepy


def observable(*args):
    def observe_tweets(observer, scheduler):
        class TweetStream(tweepy.Stream):
            def on_status(self, status):
                observer.on_next(status)

            def on_error(self, error):
                observer.on_error(error)

        stream = TweetStream(
            getenv('CONSUMER_KEY'),
            getenv('CONSUMER_SECRET'),
            getenv('ACCESS_TOKEN'),
            getenv('ACCESS_TOKEN_SECRET'),
        )
        stream.filter(track=args, threaded=True)
    return create(observe_tweets)


class Ui(object):
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title = 'KalkuleiTor!'

        self.filter = Entry(font=('Arial Bold', 25))
        self.filter.grid(column=0, row=0, columnspan=3, sticky='nsew')

        self.button = Button(text='Search', font=('Arial Bold', 15), command=self.search)
        self.button.grid(column=3, row=0, columnspan=1, sticky='nsew')

        self.results = Text(font=('Arial Bold', 10))
        self.results.grid(column=0, row=1, columnspan=4, sticky='nsew')
        self.results.config(state='disabled')

        self.window.mainloop()

    def _new_tweet(self, data):
        self.results.config(state='normal')
        self.results.insert(END, data)
        self.results.update()
        self.results.config(state='disabled')
        self.results.see(END)

    def search(self):
        # self.filter.config(state='disabled')
        # self.button.config(state='disabled')
        observable(self.filter.get()).pipe(
            operators.map(lambda d: f"{d.user.name}: {d.text}\n")
        ).subscribe(self._new_tweet)

if __name__ == '__main__':
    Ui()
