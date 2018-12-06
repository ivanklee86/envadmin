import os
import pathlib
from tinydb import TinyDB
from envadmin.constants import ENVADMIN_DB_NAME


def get_db(path_to_dir: pathlib.Path) -> TinyDB:
    path_to_db = os.path.join(path_to_dir, ENVADMIN_DB_NAME)

    return TinyDB(str(path_to_db))
