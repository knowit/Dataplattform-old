import blog_poller
import ubw_poller
import traceback
import yr_poller
import twitter_search_poller
import twitter_account_poller
import linkedin_stats_poller
import linkedin_dailyStats_poller
import bitbucket_poller


def lambda_handler(event, context):
    # This is a list of polling methods that should be run once every day.
    pollings = [
        ubw_poller.poll,
        blog_poller.poll,
        yr_poller.poll,
        twitter_search_poller.poll,
        twitter_account_poller.poll,
        linkedin_stats_poller.poll,
        linkedin_dailyStats_poller.poll,
        bitbucket_poller.poll
    ]
    errors = 0
    for poll in pollings:
        try:
            poll()
        except:
            # If one of the polling methods fails it should not stop the others from running.
            traceback.print_exc()
            errors += 1

    if errors == 0:
        return {
            'statusCode': 200,
            'body': ''
        }

    else:
        return {
            'statusCode': 500,
            'body': ''
        }
