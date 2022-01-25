from pytest import fixture

from favorite_products.main import app


@fixture
def username():
    return "test123"


@fixture
def user_id():
    return 123


@fixture
def owner(username, user_id):
    return {"id": user_id, "login": username}


@fixture
def repository_name():
    return "test_repository1"


@fixture
def repository_name2():
    return "test_repository2"


@fixture
def repository(owner, repository_name):
    return {
        "name": repository_name,
        "size": 150,
        "owner": owner,
        "html_url": "https://test.com/test-repository-1",
        "private": False,
        "created_at": "2020-03-05T01:40:36Z",
        "updated_at": "2020-04-05T07:41:10Z",
        "stargazers_count": "135",
        "watchers_count": "120",
    }


@fixture
def repository2(owner, repository_name2):
    return {
        "name": repository_name2,
        "size": 3,
        "owner": owner,
        "html_url": f"https://test.com/test-repository-2",
        "private": False,
        "created_at": "2019-03-05T01:40:36Z",
        "updated_at": "2029-01-05T07:41:10Z",
        "stargazers_count": "135",
        "watchers_count": "120",
    }


@fixture
def user(username, user_id):
    return {"user_id": user_id, "username": username}


@fixture
def parsed_repository(repository_name):
    return {
        "name": repository_name,
        "size": 150,
        "url": "https://test.com/test-repository-1",
        "access_type": False,
        "created_at": "2020-03-05T01:40:36Z",
        "updated_at": "2020-04-05T07:41:10Z",
        "stars": "135",
        "watchers": "120",
    }


@fixture
def parsed_repository2(repository_name2):
    return {
        "name": repository_name2,
        "size": 3,
        "url": "https://test.com/test-repository-2",
        "access_type": False,
        "created_at": "2019-03-05T01:40:36Z",
        "updated_at": "2029-01-05T07:41:10Z",
        "stars": "135",
        "watchers": "120",
    }


@fixture
def repositories(repository, repository2):
    return [repository, repository2]


@fixture
def parsed_repositories(parsed_repository, parsed_repository2):
    return [parsed_repository, parsed_repository2]


@fixture
def user_repositories(username, user_id, parsed_repositories):
    return {
        "username": username,
        "user_id": user_id,
        "repositories": parsed_repositories,
    }


@fixture
def client():
    client = app.test_client()
    client.testing = True
    return client
