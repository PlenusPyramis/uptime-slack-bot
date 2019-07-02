#!/usr/bin/env python

import sys
import os
import time
import requests
import logging
from collections import namedtuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

try:
    SLACK_WEBHOOK=os.environ['SLACK_WEBHOOK']
except KeyError:
    print("You must provide the SLACK_WEBHOOK environment variable.")

def send_message(message):
    logger.info("Sending message to Slack: {}".format(message))
    requests.post(SLACK_WEBHOOK, json={"text": message})

Status = namedtuple('Status', 'is_live status_code reason')

def check_url_liveness(url):
    try:
        response = requests.head(url)
        if response.ok:
            logger.info("{} - UP - {}".format(url, response.status_code))
            return Status(True, response.status_code, response.reason)
        else:
            logger.info("{} - DOWN - {}".format(url, response.status_code))
            return Status(False, response.status_code, response.reason)
    except Exception as e:
        logger.error("{} - DOWN - {}".format(url, e))
        return Status(False, 0, str(e))

def main():
    ## Required arguments:
    ## url - url to check
    ## delay - delay between checks in seconds
    ## threshold - number of times the url must be down before reporting
    try:
        url = sys.argv[1]
        delay = int(sys.argv[2])
        threshold = int(sys.argv[3])
    except:
        print("Required arguments:")
        print("url - url to check")
        print("delay - delay between checks in seconds")
        print("threshold - number of  times the url must be down before reporting")
        sys.exit(1)

    is_up = True
    consecutive_down_count = 0
    while True:
        status = check_url_liveness(url)
        if status.is_live:
            consecutive_down_count = 0
        else:
            consecutive_down_count += 1

        if is_up and consecutive_down_count >= threshold:
            is_up = False
            try:
                send_message("URL is down ({threshold} times in a row) : {url} : {reason}".format(
                    threshold=threshold, url=url, reason=status.reason))
            except Exception as e:
                logger.error("Problem posting message to slack: {e}".format(e=e))

        if not is_up and status.is_live:
            is_up = True
            try:
                send_message("URL is back UP : {url} : {reason}".format(
                    threshold=threshold, url=url, reason=status.reason))
            except Exception as e:
                logger.error("Problem posting message to slack: {e}".format(e=e))

        time.sleep(delay)

if __name__ == "__main__":
    main()

