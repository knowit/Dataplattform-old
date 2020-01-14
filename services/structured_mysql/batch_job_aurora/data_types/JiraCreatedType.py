from data_types.AbstractType import AbstractType


class JiraCreatedType(AbstractType):
    attributes_keep = {
        ("issue", str): ["data", "issue"],
        ("customer", str): ["data", "customer"],
        ("created", str): ["data", "created"]
    }
