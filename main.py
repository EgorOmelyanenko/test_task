import asyncio
import functools
import signal

from aiohttp.web import Application as Server
from aiohttp.web import run_app
from application import Application

SETTINGS = {
    "host": "127.0.0.1",
    "port": 8080,
}


def start_server(host, port):
    try:
        Application.start_application()
        run_server(host, port)
    except Exception as e:
        print(e)


def stop_server():
    asyncio.get_event_loop().stop()


def run_server(host, port, handle_signals=False):
    event_loop = asyncio.get_event_loop()
    event_loop.add_signal_handler(signal.SIGINT, functools.partial(stop_server))
    event_loop.add_signal_handler(signal.SIGTERM, functools.partial(stop_server))

    server = Server()
    init_handlers(server)
    run_app(server, host=host, port=port, handle_signals=handle_signals)


def init_handlers(server):

    server.router.add_get(
        "/get_similar_vacancy",
        Application.get_similar_vacancy
    )
    pass


def main():
    start_server(
        **SETTINGS
    )


if __name__ == "__main__":
    main()
