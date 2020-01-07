from data_types.AbstractType import AbstractType


class BitbucketType(AbstractType):
    attributes_keep = {
        ("id", str): ["data", "id"],
        ("displayId", str): ["data", "displayId"],
        ("authorTimestamp", int): ["data", "authorTimestamp"],
        ("committerTimestamp", int): ["data", "committerTimestamp"],
        ("message", str): ["data", "message"],
        # ("parentCommitId", str): ["data", "parents", "id"],
        # ("parentCommitDisplayId", str): ["data", "parents", "displayId"],
        ("repositoryName", str): ["data", "repo", "name"],
        ("repositoryId", int): ["data", "repo", "id"]}
