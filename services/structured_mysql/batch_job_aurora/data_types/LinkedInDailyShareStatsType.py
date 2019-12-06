from data_types.AbstractType import AbstractType


class LinkedInDailyShareStatsType(AbstractType):

    attributes_keep = {
        ("id", str): ["id"],
        ("timestamp", int): ["timestamp"],
        ("page", str): ["data", "page"],
        ("shareCount", int): ["data", "data", "totalShareStatistics", "shareCount"],
        ("uniqueImpressionsCount", int): ["data", "data", "totalShareStatistics", "uniqueImpressionsCount"],
        ("clickCount", int): ["data", "data", "totalShareStatistics", "clickCount"],
        ("engagement", float): ["data", "data", "totalShareStatistics", "engagement"],
        ("likeCount", int): ["data", "data", "totalShareStatistics", "likeCount"],
        ("impressionCount", int): ["data", "data", "totalShareStatistics", "impressionCount"],
        ("commentCount", int): ["data", "data", "totalShareStatistics", "commentCount"],
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
                    `shareCount` INT,
                    `uniqueImpressionsCount` INT,
                    `clickCount` INT,
                    `engagement` VARCHAR(25),
                    `likeCount` INT,
                    `impressionCount` INT,
                    `commentCount` INT,
                    `timeRangeStart` BIGINT,
                    `timeRangeEnd` BIGINT,
                    PRIMARY KEY (id)
                );
                """
        return sql
