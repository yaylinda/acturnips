import praw
import time
from twilio.rest import Client

import config


"""
"""
def create_twilio_client():
  return Client(config.twilio_account_sid, config.twilio_auth_token)


"""
"""
def create_reddit_client():
  return praw.Reddit()


"""
"""
def poll(current_utc_timestamp, reddit_client, twilio_client):
  print('Starting polling at %d (UTC)\n' % current_utc_timestamp)

  for submission in reddit_client.subreddit(config.subreddit_name).stream.submissions():
    handle_submission(current_utc_timestamp, submission, twilio_client)


"""
"""
def handle_submission(current_utc_timestamp, submission, twilio_client):
  if (current_utc_timestamp < submission.created_utc):
    print('[NEW] [%d] %s' % (submission.created_utc, submission.title))
    message = twilio_client.messages.create(
        to = config.to_number, 
        from_ = config.from_number,
        body = '%s\n%s' % (submission.title, submission.url))
  else:
    print('[OLD] [%d] %s' % (submission.created_utc, submission.title))


"""
"""
def main():
  reddit_client = create_reddit_client()
  print('Initialized Reddit Client\n')

  twilio_client = create_twilio_client()
  print('Initialized Twilio Client\n')
  
  current_utc_timestamp = time.time()

  poll(current_utc_timestamp, reddit_client, twilio_client)


"""
"""
if __name__ == '__main__':
  main()