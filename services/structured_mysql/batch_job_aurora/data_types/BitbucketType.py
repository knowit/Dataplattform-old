from data_types.AbstractType import AbstractType


class BitbucketType(AbstractType):
    attributes_keep = {
        ("id", str): ["id"],
        ("displayId", str): ["displayId"],
        ("authorTimestamp", int): ["authorTimestamp"],
        ("committerTimestamp", int): ["committerTimestamp"],
        ("message", str): ["message"],
        ("parentCommitId", str): ["parents", "id"],
        ("parentCommitDisplayId", str): ["parents", "displayId"],
        ("repositoryId", int): ["repo", "id"]}
