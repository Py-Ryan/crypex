from crypex import client
from discord.ext.commands import Bot
from contextlib import contextmanager
from logging import getLogger, Logger, FileHandler, Formatter, INFO


@contextmanager
def setup_logging() -> None:
    try:
        getLogger().setLevel(INFO)

        log: Logger = getLogger()
        log.setLevel(INFO)
        handler: FileHandler = FileHandler(filename='.client.log', encoding='utf-8', mode='w')
        dt_fmt: str = '%Y-%m-%d %H:%M:%S'
        fmt: Formatter = Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        for handle in log.handlers[:]:
            handle.close()
            log.removeHandler(handle)


def initalize_client() -> None:
    log: Logger = getLogger()
    bot: Bot = client.Crypex(log)

    bot.run()


if __name__ == '__main__':
    with setup_logging():
        initalize_client()
