import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread, current_thread
import logging

"""
--source [-s] 
--output [-o] default folder = result
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="result")

args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

threads = []


def grabs_folder(path: Path) -> None:
    logging.info(f"Start thread {current_thread().name} in {path}")
    for el in path.iterdir():
        if el.is_dir():
            inner_thread = Thread(target=grabs_folder, args=(el,))
            inner_thread.start()
            threads.append(inner_thread)
        else:
            copy_file(el)


def copy_file(path: Path) -> None:
    ext = path.suffix[1:]
    ext_folder = output / ext
    try:
        ext_folder.mkdir(exist_ok=True, parents=True)
        copyfile(path, ext_folder / path.name)
    except OSError as err:
        logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    th = Thread(target=grabs_folder, args=(source,))
    th.start()
    threads.append(th)

    [th.join() for th in threads]

    print(f"Можна видалять {source}")
