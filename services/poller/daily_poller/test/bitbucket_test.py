from unittest.mock import patch
# import daily_poller.bitbucket_poller
import unittest
import bitbucket_poller
import poller_util


class TestBitbucketMethods(unittest.TestCase):

    def test_get_repo_url(self):
        mock_repo = {"project": {"key": "KEY"}, "slug": "SLUG"}
        self.assertEqual(bitbucket_poller.get_repo_url(mock_repo),
                         "projects/KEY/repos/SLUG")

    def mocked_bitbucket_poller_get(url, query_params):
        values = ["AAAA", "BBBBBBB", "CCCCCCCCC", "DDDDDDDDDD", "EEEEEEEEEEE",
                  "FFFFFF", "GGG", "HHH", "IIIIIII", "JJJJJJJ"]
        items_per_page = 3

        start = 0
        if "start" in query_params:
            start = query_params["start"]

        paged_values = values[start:start+items_per_page]
        return {"isLastPage": len(values) < (start + items_per_page),
                "values": paged_values, "nextPageStart": start + items_per_page}

    @patch("bitbucket_poller.get", side_effect=mocked_bitbucket_poller_get)
    def test_get_all_pages_when_all_values_does_not_fit_one_page(self, mock_get):
        mock_get.items_per_page = 1
        expected_values = ["AAAA", "BBBBBBB", "CCCCCCCCC", "DDDDDDDDDD", "EEEEEEEEEEE",
                           "FFFFFF", "GGG", "HHH", "IIIIIII", "JJJJJJJ"]
        self.assertEqual(bitbucket_poller.get_all_pages(
            "some_url", {"start": 0}), expected_values)
        self.assertEqual(mock_get.call_count, 4)

    @patch("bitbucket_poller.get")
    def test_get_all_pages_when_all_values_fit_one_page(self, mock_get):
        expected_values = ["AAA", "BBB"]
        mock_get.return_value = {"isLastPage": True, "values": expected_values}
        self.assertEqual(bitbucket_poller.get_all_pages(
            "url"), expected_values)

    @patch('poller_util.PollerUtil.fetch_last_inserted_doc')
    @patch("bitbucket_poller.get_all_pages")
    def test_that_get_commits_returns_the_correct_output(self, mock_get, mock_last_inserted):
        mock_repo = {"project": {"key": "KEY"}, "slug": "SLUG"}
        mock_get.return_value = [{
            "id": "BBBBBBBBBBBBBbb",
            "displayId": "BBBBB",
            "author": {
                "name": "navn navnesen",
                "emailAddress": "name@email.address"
            },
            "authorTimestamp": 1412769340000,
            "committer": {
                "name": "navn navnesen",
                "emailAddress": "name@email.address"
            },
            "committerTimestamp": 1412768561002,
            "message": "the message",
            "parents": [
                {
                    "id": "AAAAAAAAAAAAAAAA",
                    "displayId": "AAAAAA"
                }
            ]
        }]
        expected = [{
            "id": "BBBBBBBBBBBBBbb", "repo": mock_repo,
            "displayId": "BBBBB",
            "authorTimestamp": 1412769340000,
            "committerTimestamp": 1412768561002,
            "message": "the message",
            "parents": [
                {
                    "id": "AAAAAAAAAAAAAAAA",
                    "displayId": "AAAAAA"
                }
            ]
        }]
        self.assertEqual(bitbucket_poller.get_commits(mock_repo), expected)

    @patch("bitbucket_poller.get_all_pages")
    def test_that_get_repos_returns_empty_list_when_not_finding_any_repos(self, mock_get_all_pages):
        mock_get_all_pages.return_value = []
        expected = []
        self.assertEqual(bitbucket_poller.get_repos(), expected)

    @patch("bitbucket_poller.get_all_pages")
    def test_that_get_repos_returns_expected_repos(self, mock_get_all_pages):
        mock_return = []
        mock_return.append({"id": 123, "slug": "some_slug", "name": "a_name", "links": {
                           "href": [{"self": "the_url"}]}, "project": {"key": "asd", "id": 2448}})
        mock_get_all_pages.return_value = mock_return
        expected = [{"id": 123, "slug": "some_slug",
                     "name": "a_name", "project": {"key": "asd", "id": 2448}}]
        self.assertEqual(bitbucket_poller.get_repos(), expected)


if __name__ == '__main__':
    unittest.main()
