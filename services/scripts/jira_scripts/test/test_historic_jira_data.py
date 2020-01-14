import unittest
from unittest import mock
from unittest.mock import patch

import historic_jira_data


class HistoricJiraDataTestCase(unittest.TestCase):

    @patch('services.poller.jira_poller.jira_util.strip_data')
    @patch('services.poller.jira_poller.jira_util.handle_http_request')
    def test_get_jira_data_should_make_20_calls_to_handle_http_request_and_return_list_with_as_many_elements_as_the_number_of_times_strip_data_returns_a_list_with_elements(
            self, mock_handle_http_request, mock_strip_data):
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_handle_http_request.return_value = mock_object

        mock_strip_data.return_value = ['mock mock']
        data = historic_jira_data.get_jira_data()
        self.assertEqual(mock_handle_http_request.call_count, 20)
        self.assertEqual(len(data), 20)

    @patch('sys.exit')
    @patch('services.poller.jira_poller.jira_util.handle_http_request')
    def test_get_jira_data_calls_sys_exit_when_handle_http_request_returns_object_with_status_code_other_than_200(
            self,
            mock_handle_http_request,
            mock_sys_exit
    ):
        mock_object = mock.Mock()
        mock_object.status_code = 404
        mock_handle_http_request.return_value = mock_object
        historic_jira_data.get_jira_data()
        self.assertEqual(mock_sys_exit.call_count, 20)

    @patch('services.poller.jira_poller.jira_util.handle_http_request')
    def test_post_to_ingest_loop_should_call_handle_http_request_3_times(self, mock_handle_http_request):
        mock_data = [1, 2, 3]
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_handle_http_request.return_value = mock_object
        historic_jira_data.post_to_ingest_loop(data=mock_data, ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 3)

    @patch('services.poller.jira_poller.jira_util.handle_http_request')
    @patch('sys.exit')
    def test_post_to_ingest_loop_should_call_sys_exit_when_return_value_is_none(
            self,
            mock_exit,
            mock_handle_http_request
    ):
        historic_jira_data.post_to_ingest_loop(data=[1], ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 1)
        self.assertEqual(mock_exit.call_count, 1)

    @patch('services.poller.jira_poller.jira_util.handle_http_request')
    @patch('sys.exit')
    def test_post_to_ingest_loop_should_call_sys_exit_when_status_code_is_not_200(
            self,
            mock_exit,
            mock_handle_http_request
    ):
        mock_data = [1]
        mock_object = mock.Mock()
        mock_object.status_code = 500
        mock_handle_http_request.return_value = mock_object
        historic_jira_data.post_to_ingest_loop(data=mock_data, ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 1)
        self.assertEqual(mock_exit.call_count, 1)


if __name__ == '__main__':
    unittest.main()
