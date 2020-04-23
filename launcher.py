import contextlib
import logging
from crypex import client


@contextlib.contextmanager
def setup_logging() -> None:
    try:
        logging.getLogger().setLevel(logging.INFO)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='.client.log', encoding='utf-8', mode='w')
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        for handle in log.handlers[:]:
            handle.close()
            log.removeHandler(handle)


def initalize_client() -> None:
    log = logging.getLogger()
    bot = client.Crypex()

    bot.run()


if __name__ == '__main__':
    with setup_logging():
        initalize_client()
