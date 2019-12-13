import unittest
from unittest import mock
from unittest.mock import patch

import jira_poller
import poller_util


class JiraPollerTestCase(unittest.TestCase):

    @patch('jira_poller.create_status_code_dict')
    def test_handle_request_status_should_call_create_status_code_dict_once_when_input_data_contains_status_code_other_than_200(
            self,
            mock_create_status_code_dict
    ):
        mock_object = mock.Mock()
        mock_object.status_code = 404
        jira_poller.handle_request_status(mock_object)
        self.assertEqual(mock_create_status_code_dict.call_count, 1)

    @patch('jira_poller.create_status_code_dict')
    def test_handle_request_status_should_call_create_status_code_dict_once_when_input_data_contains_status_code_200_and_the_data_contains_less_than_1_element(
            self,
            mock_create_status_code_dict
    ):
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_object.json.return_value = {
            'issues': []
        }
        jira_poller.handle_request_status(mock_object)
        self.assertEqual(mock_create_status_code_dict.call_count, 1)

    def test_handle_request_status_should_return_none_when_input_data_contains_status_code_200_and_the_data_contains_more_than_0_elements(
            self):
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_object.json.return_value = {
            'issues': ['mock']
        }
        result = jira_poller.handle_request_status(mock_object)
        self.assertEqual(result, None)

    @patch('jira_poller.create_status_code_dict')
    @patch('jira_util.handle_http_request')
    def test_post_jira_data_should_call_create_status_code_dict_once_when_mock_handle_http_request_returns_object_with_status_code_other_than_200(
            self, mock_handle_http_request, mock_create_status_code_dict):
        mock_data = [1, 2, 3]
        mock_object = mock.Mock()
        mock_object.status_code = 404
        mock_handle_http_request.return_value = mock_object
        jira_poller.post_jira_data(mock_data)
        self.assertEqual(mock_create_status_code_dict.call_count, 1)

    @patch('jira_util.upload_last_inserted_doc')
    @patch('jira_poller.create_status_code_dict')
    @patch('jira_util.handle_http_request')
    def test_post_jira_data_should_call_upload_last_inserted_doc_once_and_create_status_code_dict_once_when_handle_http_request_returns_object_with_status_code_200(
            self, mock_handle_http_request, mock_create_status_code_dict, mock_upload_last_inserted_doc):
        mock_data = [1, 2, {'timestamp': 'mock'}]
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_handle_http_request.return_value = mock_object
        jira_poller.post_jira_data(mock_data)
        self.assertEqual(mock_upload_last_inserted_doc.call_count, 1)
        self.assertEqual(mock_create_status_code_dict.call_count, 1)

    @patch('jira_poller.create_status_code_dict')
    @patch('poller_util.PollerUtil.fetch_last_inserted_doc')
    def test_handler_should_call_create_status_code_dict_once_when_fetch_last_inserted_doc_returns_none(
            self,
            mock_fetch_last_inserted_doc,
            mock_create_status_code_dict
    ):
        mock_fetch_last_inserted_doc.return_value = None
        jira_poller.handler(None, None)
        self.assertEqual(mock_create_status_code_dict.call_count, 1)

    @patch('jira_util.format_string_containing_iso_date')
    @patch('jira_poller.handle_request_status')
    @patch('jira_poller.poll_daily_jira_data')
    @patch('poller_util.PollerUtil.fetch_last_inserted_doc')
    def test_handler_should_return_status_code_dict_if_fetch_last_inserted_doc_not_returns_none_and_handle_request_status_returns_not_none(
            self,
            mock_fetch_last_inserted_doc,
            mock_poll_daily_jira_data,
            mock_handle_request_status,
            mock_format_string_containing_iso_date
    ):
        mock_fetch_last_inserted_doc.return_value = mock.Mock()
        mock_format_string_containing_iso_date.return_value = mock.Mock()
        mock_object = mock.Mock()
        mock_handle_request_status.return_value = mock_object
        result = jira_poller.handler(None, None)
        self.assertEqual(result, mock_object)

    @patch('jira_util.format_string_containing_iso_date')
    @patch('jira_poller.post_jira_data')
    @patch('jira_util.strip_data')
    @patch('jira_poller.handle_request_status')
    @patch('jira_poller.poll_daily_jira_data')
    @patch('poller_util.PollerUtil.fetch_last_inserted_doc')
    def test_handler_should_call_post_jira_data_if_fetch_last_inserted_doc_not_returns_none_and_handle_request_status_returns_none(
            self,
            mock_fetch_last_inserted_doc,
            mock_poll_daily_jira_data,
            mock_handle_request_status,
            mock_strip_data,
            mock_post_jira_data,
            mock_format_string_containing_iso_date
    ):
        mock_fetch_last_inserted_doc.return_value = mock.Mock()
        mock_handle_request_status.return_value = None
        mock_strip_data.return_value = [{'timestamp': 1}, {'timestamp': 2}]
        mock_format_string_containing_iso_date.return_value = mock.Mock()
        jira_poller.handler(None, None)
        self.assertEqual(mock_post_jira_data.call_count, 1)


if __name__ == '__main__':
    unittest.main()
