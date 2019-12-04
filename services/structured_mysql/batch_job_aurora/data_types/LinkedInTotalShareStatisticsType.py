import hashlib
from data_types.AbstractType import AbstractType


class LinkedInTotalShareStatisticsType(AbstractType):

    attributes_keep = {
        ("page", str): ["data", "page"],
        ("time", str): ["data", "time"],
        ("shareCount", int): ["data", "data", "shareCount"],
        ("uniqueImpressionsCount", int): ["data", "data", "uniqueImpressionsCount"],
        ("clickCount", int): ["data", "data", "clickCount"],
        ("engagement", float): ["data", "data", "engagement"],
        ("shareMentionsCount", int): ["data", "data", "shareMentionsCount"],
        ("likeCount", int): ["data", "data", "likeCount"],
        ("impressionCount", int): ["data", "data", "impressionCount"],
        ("commentMentionsCount", int): ["data", "data", "commentMentionsCount"],
        ("commentCount", int): ["data", "data", "commentCount"],
    }

    def generate_id(self, timestamp, page):
        string = str(timestamp)+str(page)
        return str((hashlib.md5(string.encode('utf8'))).hexdigest())

    def get_column_values(self, doc):
        """
        :param doc: A raw document from get_docs API.
        :return: a dictionary containing every key, value that you want to insert into Aurora DB.
        """
        output = {}
        for attr, attribute_path in self.attributes_keep.items():
            attr_name = attr[0]
            value = doc.copy()
            is_ok = True

            if len(attr) >= 3:
                # Then we have a special case and we need to run a different function in order
                # to get the values.
                func = attr[2]
                value = func(doc)
                output[attr_name] = value
                continue

            for attr in attribute_path:
                # If the attr is an int, it is actually an index. And therefore we need to
                # make sure that our value list is long enough.
                if type(attr) is int and type(value) is list and attr <= (len(value) - 1):
                    value = value[attr]
                # if not then we need to make sure that attr is a key in the dictionary value.
                elif type(attr) is str and type(value) is dict and attr in value:
                    value = value[attr]
                else:
                    is_ok = False
                    break
            if is_ok:
                output[attr_name] = value

        output['id'] = self.generate_id(output['timestamp'], output['page'])
        return output

    def get_create_table_sql(self, table_name):
        """
        :return: A sql string for creating a table for this specific type
        """
        sql = f"""
                CREATE TABLE {table_name} (
                    `id` VARCHAR(32) NOT NULL,
                    `timestamp` BIGINT NOT NULL,
                    `time` TEXT,
                    `page` TEXT,
                    `shareCount` INT,
                    `uniqueImpressionsCount` INT,
                    `clickCount` INT,
                    `engagement` VARCHAR(25),
                    `shareMentionsCount` INT,
                    `likeCount` INT,
                    `impressionCount` INT,
                    `commentMentionsCount` INT,
                    `commentCount` INT,
                    PRIMARY KEY (id)
                );
                """
        return sql
