import os
import requests
from requests.exceptions import HTTPError
import json

from dotenv import load_dotenv
from poller_util import PollerUtil

load_dotenv(dotenv_path='.env')

BITBUCKET_TYPE = "BitbucketType"
BITBUCKET_API_URL = "https://kode.knowit.no/rest/api/1.0"


def create_project_data(project):
    data_point = {
        "id": project["id"],
        "key": project["key"],
        "name": project["name"],
        "public": project["public"],
        "url": project["links"]["self"][0]["href"]
    }
    if "description" in project:
        data_point["description"] = project["description"]

    return data_point


def get(path, query_params=None):
    """
    Make a get request to path with query_params
    :param path: url for the get request
    :param query_params: a dictionary with the query params for the request
    :return: the response from the request
    """
    try:
        response = requests.get(
            f'{BITBUCKET_API_URL}/{path}', params=query_params)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return
    except Exception as err:
        print(f'Other error occurred: {err}')
        return
    response = response.json()
    return response


def get_all_pages(url, params=None):
    """
    Bitbucket API uses pagination. This function retrieves items from
    all the pages by requesting more items until isLastPage: false is returned
    by the API.
    :param url: the url to get items from
    :param params: query parameters
    :return: a list of the items
    """
    if params is None:
        params = {}

    response = get(url, params)
    res = response["values"]

    while not response["isLastPage"]:
        params["start"] = response["nextPageStart"]
        response = get(url, query_params=params)
        res.extend(response["values"])
    return res


def get_projects():
    """
    Get all bitbucket projects
    """
    response = get_all_pages("projects")

    projects = []
    for elem in response:
        res = create_project_data(elem)
        projects.append(res)

    return projects


def get_repo_url(repo):
    """
    create the url for a repo when given a repo object
    :param repo: the repo we want to create a url for
    :return: the url as a string
    """
    projectKey = repo["project"]["key"]
    slug = repo["slug"]
    return f"projects/{projectKey}/repos/{slug}"


def get_commits(repo):
    """
    get all commits, for the given repo, which have not yet been posted to
    the ingest api
    """
    last = PollerUtil.fetch_last_inserted_doc("BitbucketType" + repo["slug"])
    params = {"since": last}
    url = f"{get_repo_url(repo)}/commits"
    commits = get_all_pages(url, params=params)
    for commit in commits:
        del commit["committer"]
        del commit["author"]
        commit["repo"] = repo

    for commit in commits:
        print(commit["committerTimestamp"])

    # Make sure commits are in order with olderst first and newest last
    commits = sorted(commits, key=lambda it: it["committerTimestamp"])

    return commits


def get_branches(repo):
    """
    get all branches for a repository
    """
    url = f"{get_repo_url(repo)}/branches"
    return get_all_pages(url)


def get_pull_requests(repo):
    """
    get all pull requests for a repository
    """
    url = f"{get_repo_url(repo)}/pull-requests"
    return get_all_pages(url)


def get_forks(repo):
    """
    get all forks for a repository
    """
    url = f"{get_repo_url(repo)}/forks"
    return get_all_pages(url)


def get_repos():
    """
    gets all repositories.
    :return: list of the repositories
    """
    response = get_all_pages("repos")
    repos = []
    for elem in response:
        del elem["links"]
        elem["project"] = {"id": elem["project"]
                           ["id"], "key": elem["project"]["key"]}

        # elem["commits"] = get_commits(elem)
        # elem["branches"] = get_branches(elem)
        # elem["forks"] = get_forks(elem)
        # elem["pull-requets"] = get_pull_requests(elem)
        repos.append(elem)

    return repos


def poll():
    """
    find all repos using get_repos(), then find all commits for those repos using
    get_commits(), and finally post all new commits using post_commits()
    """
    repos = get_repos()
    for repo in repos:
        repo_commits = get_commits(repo)
        post_commits(repo_commits, repo)


def post_commits(commits, repo):
    """
    post the given commits, and update last_inserted_doc for the repo
    :param commits: A list of commits to post into ingest
    :param repo: the repo which the commits are associated with
    """
    last_inserted_id = None
    for commit in commits:
        result = PollerUtil.post_to_ingest_api(
            type=BITBUCKET_TYPE, data=commit)
        if result is 200:
            print(result)
            last_inserted_id = commit["id"]

    if last_inserted_id is not None:
        last_inserted_name = BITBUCKET_TYPE + repo["slug"]
        PollerUtil.upload_last_inserted_doc(
            last_inserted_doc=last_inserted_id, type=last_inserted_name)
