from data_types.AbstractType import AbstractType


class JiraUpdatedType(AbstractType):
    attributes_keep = {
        ("issue", str): ["data", "issue"],
        ("status", str): ["data", "status"],
        ("updated", str): ["data", "updated"]
    }
