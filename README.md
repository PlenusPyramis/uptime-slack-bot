# URL status checker for Slack

A slack bot that tells you if a website goes down, and when it comes back.

* Create a Slack app - https://api.slack.com/apps
* Enable incoming webhook
* Copy the webhook URL and bind to an environment variable called `SLACK_WEBHOOK` (see below).
* Run the docker container with the `SLACK_WEBHOOK` and three additional arguments:
  * The URL to check
  * The delay between checks
  * The threshold number of times that a URL must be down before reporting it.

## Example:

```
# Set your own slack webhook:
export SLACK_WEBHOOK=https://hooks.slack.com/services/XXXX/YYY/ZZZ
# The url to check
export URL=http://www.example.com
# Delay between checks (seconds)
export DELAY=10
# Number of checks site must be down before reporting:
export THRESHOLD=3

sudo docker run --rm -it \
   -e SLACK_WEBHOOK=$SLACK_WEBHOOK \
   plenuspyramis/uptime-slack-bot \
   $URL $DELAY $THRESHOLD
```
