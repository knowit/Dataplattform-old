import unittest
from unittest import mock
from unittest.mock import patch
import json
import requests

import jira_util
import poller_util


class JiraUtilTestCase(unittest.TestCase):

    @patch('jira_util.format_string_containing_iso_date')
    @patch('poller_util.PollerUtil.upload_last_inserted_doc')
    def test_upload_last_inserted_doc_should_call_format_string_containing_iso_date_once_and_pollerutil_upload_last_inserted_doc_once(
            self, mock_format_string_containing_iso_date, mock_upload_last_inserted_doc):
        jira_util.upload_last_inserted_doc(timestamp='mock timestamp', data_type='mock type')
        self.assertEqual(mock_format_string_containing_iso_date.call_count, 1)
        self.assertEqual(mock_upload_last_inserted_doc.call_count, 1)

    def test_string_containing_iso_date_should_be_correctly_formatted(self):
        iso_date_string = '2019-12-09T13:05:22.000+0100'
        formatted_string = jira_util.format_string_containing_iso_date(iso_date_string)
        self.assertEqual(formatted_string, "'2019/12/09'")

    def test_should_strip_data_correctly(self):
        input_data = {
            'issues': [
                {
                    'fields': {
                        'created': 'a date',
                        'labels': ['a customer'],
                        'status': {
                            'name': 'accepted'
                        }
                    },
                    'key': 'SALG-50'
                },
                {
                    'fields': {
                        'created': 'a date',
                        'labels': [''],
                        'status': {
                            'name': 'accepted'
                        }
                    },
                    'key': 'SALG-51'
                }
            ]
        }
        stripped_data = jira_util.strip_data(input_data)
        expected_data = [
            {
                'timestamp': 'a date',
                'customer': 'a customer',
                'status': 'accepted',
                'issue': 'SALG-50'
            },
            {
                'timestamp': 'a date',
                'customer': '',
                'status': 'accepted',
                'issue': 'SALG-51'
            }
        ]
        self.assertListEqual(stripped_data, expected_data)

    @patch('requests.get')
    def test_get_sales_data_from_jira_should_call_get_request(self, mock_get):
        url = 'http://123-mock-api.com'
        mock_username = 'mock_user'
        mock_password = 'mock_password'
        jira_util.get_sales_data_from_jira(
            url=url,
            username=mock_username,
            password=mock_password,
            params={}
        )
        self.assertEqual(mock_get.call_count, 1)

    def test_create_params_dict_returns_a_dict_with_the_expected_format(self):
        params = {
            'jql': "project=SALG and status != 'Rejected'",
            'fields': 'labels, status, created, updated',
            'maxResults': 500,
            'startAt': 0
        }
        result = jira_util.create_params_dict()
        self.assertEqual(result, params)

    @patch('requests.get')
    def test_get_sales_data_from_jira_should_call_get_request_with_expected_expected_parameters(self, mock_get):
        mock_url = 'http://123-mock-api.com'
        mock_username = 'mock_user'
        mock_password = 'mock_password'
        jira_util.get_sales_data_from_jira(
            url=mock_url,
            username=mock_username,
            password=mock_password,
            params={}
        )

        self.assertIn(
            mock.call(
                auth=(mock_username, mock_password),
                params={},
                url=mock_url
            ),
            mock_get.call_args_list)

    @patch('requests.post')
    def test_post_to_ingest_should_call_post_request(self, mock_post):
        mock_url = 'http://123-mock-api.com'
        mock_api_key = 'mock api key'
        mock_data = {
            'mock data': 'mock mock'
        }
        jira_util.post_to_ingest(
            url=mock_url,
            api_key=mock_api_key,
            data=mock_data
        )
        self.assertEqual(mock_post.call_count, 1)

    @patch('requests.post')
    def test_post_to_ingest_should_call_post_request_with_expected_parameters(self, mock_post):
        mock_url = 'http://123-mock-api.com'
        mock_api_key = 'mock api key'
        mock_data = {
            'mock data': 'mock mock'
        }
        encoded_mock_data = json.dumps(mock_data).encode()
        jira_util.post_to_ingest(
            url=mock_url,
            api_key=mock_api_key,
            data=mock_data
        )
        self.assertIn(
            mock.call(
                url=mock_url,
                data=encoded_mock_data,
                headers={'x-api-key': mock_api_key}
            ), mock_post.call_args_list)

    @patch('jira_util.handle_http_request')
    def test_post_to_ingress_loop_should_call_handle_http_request_3_times(self, mock_handle_http_request):
        mock_data = [1, 2, 3]
        mock_object = mock.Mock()
        mock_object.status_code = 200
        mock_handle_http_request.return_value = mock_object
        jira_util.post_to_ingest_loop(data=mock_data, ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 3)

    @patch('jira_util.handle_http_request')
    @patch('sys.exit')
    def test_post_to_ingress_loop_should_call_sys_exit_when_return_value_is_none(
            self,
            mock_exit,
            mock_handle_http_request
    ):
        jira_util.post_to_ingest_loop(data=[1], ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 1)
        self.assertEqual(mock_exit.call_count, 1)

    @patch('jira_util.handle_http_request')
    @patch('sys.exit')
    def test_post_to_ingress_loop_should_call_sys_exit_when_status_code_is_not_200(
            self,
            mock_exit,
            mock_handle_http_request
    ):
        mock_data = [1]
        mock_object = mock.Mock()
        mock_object.status_code = 500
        mock_handle_http_request.return_value = mock_object
        jira_util.post_to_ingest_loop(data=mock_data, ingest_url='mock url', ingest_api_key='mock api key')
        self.assertEqual(mock_handle_http_request.call_count, 1)
        self.assertEqual(mock_exit.call_count, 1)

    @patch('requests.get')
    def test_handle_http_request_should_return_500_for_http_error_500(self, mock_request):
        def mock_request_function():
            return requests.get(url='http://123-mock-api.com')

        mock_response = requests.models.Response()
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        response = jira_util.handle_http_request(mock_request_function)
        self.assertEqual(response.status_code, 500)

    @patch('requests.get')
    def test_handle_http_request_should_return_200_for_ok_get_request(self, mock_request):
        def mock_request_function():
            return requests.get(url='http://123-mock-api.com')

        mock_response = requests.models.Response()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        response = jira_util.handle_http_request(mock_request_function)
        self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        unittest.main()
