
# coding: utf-8

# how to get all the vocab terms and data about them from hatebase.org's API
# and save it all in a csv

import requests
import pandas as pd

# from https://github.com/HatebaseInc/API-Docs/blob/master/README.md
authurl = 'https://api.hatebase.org/4-0/authenticate'

# your API key, get it from your account at hatebase.org
# register, log in, go to 'API Key', copy and paste
key = '' # your key here

# first you must get an authentication token from the authentication API
# set parameters for that request
authparams = {
  'api_key': key,
}

# make your authentication request
payload = requests.post(authurl, data=authparams).json()

# grab the token to use for later requests
auth_token = payload['result']['token']

# check out your new token. The documentatoin says it will expire within an hour
print(auth_token)

# set endpoint for the vocab API

# the vocabulary is paginated, and you can only get one page (100 terms as of Dec. 1, 2018)
# at a time. So now we get the number of pages
vocab_params = {   
    'token': auth_token,
}

# make first request to vocab API to get number of pages
vocab_payload = requests.post(vocab_url, data=vocab_params).json()


# set number of pages
pages = vocab_payload['number_of_pages']

# initialize vocab list
final_vocab = []

# add first page of terms to vocab list
for item in vocab_payload['result']:
    final_vocab.append(item)

# send a request for each page, you already have page 1
for page in range(2,pages +1):
    # if you do not want to filter the terms these are then only params you need
    new_vocab_params = {
        'token': auth_token,
        'page': page,
    }
    vocab_payload = requests.post(vocab_url, data=new_vocab_params).json()
    # add each dict to the vocab list
    for item in vocab_payload['result']:
        final_vocab.append(item)
    
# take a look
len(final_vocab)


# looks OK, look some more
for item in final_vocab:
    print(item['term'])

# still looks good, make into a dataframe
vocab_df = pd.DataFrame(final_vocab)

# checks out
print(len(vocab_df))
vocab_df.head()

# save it
vocab_df.to_csv('hatebase_vocab_120118.csv')

