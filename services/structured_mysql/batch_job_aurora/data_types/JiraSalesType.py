from data_types.AbstractType import AbstractType


class JiraSalesType(AbstractType):
    attributes_keep = {
        ("jira_timestamp", str): ["data", "timestamp"],
        ("customer", str): ["data", "customer"],
        ("status", str): ["data", "status"],
        ("issue", str): ["data", "issue"]
    }
