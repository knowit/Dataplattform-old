import hashlib
from data_types.AbstractType import AbstractType
from data_types.linkedin_util import resolve_industry, resolve_country, resolve_function, resolve_region, resolve_seniority


class LinkedInPageStatisticsType(AbstractType):

    attributes_keep = {
        ("page", str): ["data", "page"],
        ("time", str): ["data", "time"],
    }

    inner_attributes_keep = {
        ("allMobileViews", int): ["pageStatistics", "views", "allM", "v"],
        ("allDesktopViews", int): ["pageStatistics", "views", "allD", "v"],
        ("allViews", int): ["pageStatistics", "views", "all", "v"],
        ("mobileJobsViews", int): ["pageStatistics", "views", "mJobs", "v"],
        ("desktopJobsViews", int): ["pageStatistics", "views", "dJobs", "v"],
        ("jobsViews", int): ["pageStatistics", "views", "jobs", "v"],
        ("mobileCareersViews", int): ["pageStatistics", "views", "mCareers", "v"],
        ("desktopCareersViews", int): ["pageStatistics", "views", "dCareers", "v"],
        ("careersViews", int): ["pageStatistics", "views", "careers", "v"],
        ("mobileLifeAtViews", int): ["pageStatistics", "views", "mLifeAt", "v"],
        ("desktopLifeAtViews", int): ["pageStatistics", "views", "dLifeAt", "v"],
        ("lifeAtViews", int): ["pageStatistics", "views", "lifeAt", "v"],
        ("mobileInsightsViews", int): ["pageStatistics", "views", "mInsights", "v"],
        ("desktopInsightsViews", int): ["pageStatistics", "views", "dInsights", "v"],
        ("insightsViews", int): ["pageStatistics", "views", "insights", "v"],
        ("mobileAboutViews", int): ["pageStatistics", "views", "mAbout", "v"],
        ("desktopAboutViews", int): ["pageStatistics", "views", "dAbout", "v"],
        ("aboutViews", int): ["pageStatistics", "views", "about", "v"],
        ("mobilePeopleViews", int): ["pageStatistics", "views", "mPeople", "v"],
        ("desktopPeopleViews", int): ["pageStatistics", "views", "dPeople", "v"],
        ("peopleViews", int): ["pageStatistics", "views", "people", "v"],
        ("mobileOverviewViews", int): ["pageStatistics", "views", "mOverview", "v"],
        ("desktopOverviewViews", int): ["pageStatistics", "views", "dOverview", "v"],
        ("overviewViews", int): ["pageStatistics", "views", "about", "v"],
    }

    def generate_id(self, timestamp, page, type, typeVariable):
        string = str(timestamp)+str(page)+str(type)+str(typeVariable)
        return str((hashlib.md5(string.encode('utf8'))).hexdigest())

    def get_type_data(self, data, type):
        if type == "LinkedInPageStatisticsByIndustryType":
            return resolve_industry(data['industry']), "industry"
        elif type == "LinkedInPageStatisticsByFunctionType":
            return resolve_function(data['function']), "function"
        elif type == "LinkedInPageStatisticsByCountryType":
            return resolve_country(data['country']), "country"
        elif type == "LinkedInPageStatisticsByRegionType":
            return resolve_region(data['region']), "region"
        elif type == "LinkedInPageStatisticsBySeniorityType":
            return resolve_seniority(data['seniority']), "seniority"
        elif type == "LinkedInPageStatisticsByStaffCountRangeType":
            return data['staffCountRange'], "staffCountRange"
        elif type == "LinkedInPageStatisticsTotalType":
            return None, "total"

    def get_column_values(self, doc):
        """
        :param doc: A raw document from get_docs API.
        :return: a dictionary containing every key, value that you want to insert into Aurora DB.
        """
        outputs = []
        inner_docs = doc['data']['data']
        if isinstance(inner_docs, list):
            for inner_doc in inner_docs:
                output = {}
                output = self.get_outer_attributes(doc, output)
                output = self.get_inner_attributes(inner_doc, doc['type'], output)
                outputs.append(output)

        else:
            output = {}
            output = self.get_outer_attributes(doc, output)
            output = self.get_inner_attributes(inner_docs, doc['type'], output)
            return output

        return outputs

    def get_outer_attributes(self, doc, output):
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

        return output

    def get_inner_attributes(self, inner_doc, data_type, output):
        #check if inner_doc conforms to attribute format
        if "pageStatistics" not in inner_doc.keys():
            new_doc = {}
            new_doc['pageStatistics'] = inner_doc
            inner_doc = new_doc

        for inner_attr, inner_attribute_path in self.inner_attributes_keep.items():
            inner_attr_name = inner_attr[0]
            value = inner_doc.copy()
            is_ok = True
            for inner_attr in inner_attribute_path:
                # If the attr is an int, it is actually an index. And therefore we need to
                # make sure that our value list is long enough.
                if type(inner_attr) is int and type(value) is list and inner_attr <= (len(value) - 1):
                    value = value[inner_attr]
                # if not then we need to make sure that attr is a key in the dictionary value.
                elif type(inner_attr) is str and type(value) is dict and inner_attr in value:
                    value = value[inner_attr]
                else:
                    is_ok = False
                    break
            if is_ok:
                output[inner_attr_name] = value

        # check type and get typevariable
        var, var_type = self.get_type_data(inner_doc, data_type)
        output['type'] = var_type
        output['typeVariable'] = var

        # generate id
        output['id'] = self.generate_id(output['timestamp'], output['page'], output['type'], output['typeVariable'])
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
                    `type` ENUM('function', 'industry', 'region', 'seniority', 'staffCountRange', 'country', 'total'),
                    `typeVariable` VARCHAR(255),
                    `allMobileViews` INT,
                    `allDesktopViews` INT,
                    `allViews` INT,
                    `mobileJobsViews` INT,
                    `desktopJobsViews` INT,
                    `jobsViews` INT,
                    `mobileCareersViews` INT,
                    `desktopCareersViews` INT,
                    `careersViews` INT,
                    `mobileLifeAtViews` INT,
                    `desktopLifeAtViews` INT,
                    `lifeAtViews` INT,
                    `mobileInsightsViews` INT,
                    `desktopInsightsViews` INT,
                    `insightsViews` INT,
                    `mobileAboutViews` INT,
                    `desktopAboutViews` INT,
                    `aboutViews` INT,
                    `mobilePeopleViews` INT,
                    `desktopPeopleViews` INT,
                    `peopleViews` INT,
                    `mobileOverviewViews` INT,
                    `desktopOverviewViews` INT,
                    `overviewViews` INT,
                    PRIMARY KEY (id)
                );
                """
        return sql
