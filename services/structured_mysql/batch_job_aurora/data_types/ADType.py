from data_types.AbstractType import AbstractType

class ADType(AbstractType):

    attributes_keep = {
        ("retrieved", int): ["data", "retrieved"],
        ("count_employees", int): ["data", "count_employees"],
        ("count_discontinued_employees", int): ["data", "count_discontinued_employees"],
        ("count_subcontractors", int): ["data", "count_subcontractors"],
        ("count_discontinued_subcontractors", int): ["data", "count_discontinued_subcontractors"],
        ("count_all", int): ["data", "count_all"],
        ("count_discontinued_all", int): ["data", "count_discontinued_all"],
    }
