import os
from poller_util import PollerUtil
import integration_tests_util as util

POLLER_CONFIG = util.read_serverless_output("poller")


def test_load_config():
    assert "PollingStatusTableName" in POLLER_CONFIG


def test_upload_and_fetch_last_inserted():
    os.environ["DATAPLATTFORM_POLLING_STATUS_TABLENAME"] = POLLER_CONFIG["PollingStatusTableName"]

    TESTING_TYPE = "TestingTestingType"
    last_inserted_correct = "123"

    PollerUtil.upload_last_inserted_doc(last_inserted_correct, TESTING_TYPE)
    last_inserted = PollerUtil.fetch_last_inserted_doc(TESTING_TYPE)
    assert last_inserted == last_inserted_correct

    last_inserted_correct_2 = "12739jldfjlka"
    PollerUtil.upload_last_inserted_doc(last_inserted_correct_2, TESTING_TYPE)
    last_inserted = PollerUtil.fetch_last_inserted_doc(TESTING_TYPE)
    assert last_inserted == last_inserted_correct_2
