from data_types.AbstractType import AbstractType


class LinkedInDailyFollowerStatsType(AbstractType):

    attributes_keep = {
        ("id", str): ["id"],
        ("timestamp", int): ["timestamp"],
        ("page", str): ["data", "page"],
        ("organicFollowerGain", int): ["data", "data", "followerGains", "organicFollowerGain"],
        ("paidFollowerGain", int): ["data", "data", "followerGains", "paidFollowerGain"],
        ("timeRangeStart", int): ["data", "data", "timeRange", "start"],
        ("timeRangeEnd", int): ["data", "data", "timeRange", "end"]
    }

    def get_create_table_sql(self, table_name):
        """
        :return: A sql string for creating a table for this specific type
        """
        sql = f"""
                CREATE TABLE {table_name} (
                    `id` VARCHAR(24) NOT NULL,
                    `timestamp` BIGINT NOT NULL,
                    `page` TEXT,
                    `organicFollowerGain` INT,
                    `paidFollowerGain` INT,
                    `timeRangeStart` BIGINT,
                    `timeRangeEnd` BIGINT,
                    PRIMARY KEY (id)
                );
                """
        return sql
