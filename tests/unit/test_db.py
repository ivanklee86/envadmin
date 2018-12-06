from tinydb import Query
from envadmin.utilities import config, db
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_get_db(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    parser = config.get_config(temp_git_folder)
    database = db.get_db(parser.get("main", "repo_path"))

    database.insert({'name': 'John', 'age': 22})
    User = Query()
    result = database.search(User.name == 'John')
    assert result[0]['name'] == 'John'
