from data_types.AbstractType import AbstractType


class LinkedInDailyPageStatsType(AbstractType):

    attributes_keep = {
        ("id", str): ["id"],
        ("timestamp", int): ["timestamp"],
        ("page", str): ["data", "page"],
        ("allPageViews", int): ["data", "data", "totalPageStatistics", "views", "allPageViews", "pageViews"],
        ("allPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "allPageViews", "uniquePageViews"],
        ("overviewPageViews", int): ["data", "data", "totalPageStatistics", "views", "overviewPageViews", "pageViews"],
        ("overviewPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "overviewPageViews", "uniquePageViews"],
        ("jobsPageViews", int): ["data", "data", "totalPageStatistics", "views", "jobsPageViews", "pageViews"],
        ("jobsPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "jobsPageViews", "uniquePageViews"],
        ("careersPageViews", int): ["data", "data", "totalPageStatistics", "views", "careersPageViews", "pageViews"],
        ("careersPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "careersPageViews", "uniquePageViews"],
        ("peoplePageViews", int): ["data", "data", "totalPageStatistics", "views", "peoplePageViews", "pageViews"],
        ("peoplePageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "peoplePageViews", "uniquePageViews"],
        ("lifeAtPageViews", int): ["data", "data", "totalPageStatistics", "views", "lifeAtPageViews", "pageViews"],
        ("lifeAtPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "lifeAtPageViews", "uniquePageViews"],
        ("insightsPageViews", int): ["data", "data", "totalPageStatistics", "views", "insightsPageViews", "pageViews"],
        ("insightsPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "insightsPageViews", "uniquePageViews"],
        ("aboutPageViews", int): ["data", "data", "totalPageStatistics", "views", "aboutPageViews", "pageViews"],
        ("aboutPageViewsUnique", int): ["data", "data", "totalPageStatistics", "views", "aboutPageViews", "uniquePageViews"],
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
                    `allPageViews` INT,
                    `allPageViewsUnique` INT,
                    `overviewPageViews` INT,
                    `overviewPageViewsUnique` INT,
                    `jobsPageViews` INT,
                    `jobsPageViewsUnique` INT,
                    `careersPageViews` INT,
                    `careersPageViewsUnique` INT,
                    `peoplePageViews` INT,
                    `peoplePageViewsUnique` INT,
                    `lifeAtPageViews` INT,
                    `lifeAtPageViewsUnique` INT,
                    `insightsPageViews` INT,
                    `insightsPageViewsUnique` INT,
                    `aboutPageViews` INT,
                    `aboutPageViewsUnique` INT,
                    `timeRangeStart` BIGINT,
                    `timeRangeEnd` BIGINT,
                    PRIMARY KEY (id)
                );
                """
        return sql
