import json
from time import sleep
from boto import sqs
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from worker import config
from worker.models import Account
from worker.logs import get_logger


LOGGER = get_logger()
FEED_ITEMS = Table('feed_items')


def add_feed_item(new_feed_item):
    try:
        FEED_ITEMS.put_item(data=new_feed_item)
    except ConditionalCheckFailedException:
        message = "Feed item already exists for {0} on {1}".format(
            new_feed_item['spotify_username'],
            new_feed_item['date_posted'])
        LOGGER.exception(message)
        return False
    except:
        message = "Failed to add feed item for {0}".format(new_feed_item['spotify_username'])
        LOGGER.exception(message)
        return False
    return True


def process_message(m):
    try:
        data = json.loads(m.get_body())
    except ValueError:
        LOGGER.exception("Invalid JSON message")
        return

    date_to_process = data['date_to_process']
    spotify_username = data['spotify_username']

    try:
        account = Account(spotify_username)
    except:
        message = "Failed to load account for {0}".format(spotify_username)
        LOGGER.exception(message)
        return

    new_feed_item = account.feed_item(date_to_process)
    if new_feed_item:
        item_added = add_feed_item(new_feed_item)
        if item_added:
            account.update_last_processed(date_to_process)


def main():
    conn = sqs.connect_to_region(config.SQS_REGION)
    q = conn.create_queue(config.SQS_QUEUE_NAME)
    while True:
        messages = q.get_messages(
            num_messages=5,
            wait_time_seconds=config.SQS_WAIT_TIME)
        if messages:

            for m in messages:
                process_message(m)
                m.delete()
        else:
            sleep(config.SLEEP_TIME)


if __name__ == '__main__':
    main()
