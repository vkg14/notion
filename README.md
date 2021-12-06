## Instructions
- You will need a `private_credentials.py` file which specifies two variables:
  - `TOKEN_V2` (your API token)
  - `URL` (the URL for the page)
- Run `python movie_list_updater.py`
## Errors

>>  Traceback (most recent call last):
>>    File "movie_list_updater.py", line 60, in <module>
>>      update_movies()
>>    File "movie_list_updater.py", line 28, in update_movies
>>      client = get_client()
>>    File "/Users/vkg/PythonWorkspace/Notion/notion_tools.py", line 10, in get_client
>>      return NotionClient(token_v2=TOKEN_V2)
>>    File "/Users/vkg/.pyenv/versions/notion-workspace/lib/python3.7/site-packages/notion/client.py", line 68, in __init__
>>      self._update_user_info()
>>    File "/Users/vkg/.pyenv/versions/notion-workspace/lib/python3.7/site-packages/notion/client.py", line 74, in _update_user_info
>>      records = self.post("loadUserContent", {}).json()["recordMap"]
>>    File "/Users/vkg/.pyenv/versions/notion-workspace/lib/python3.7/site-packages/notion/client.py", line 188, in post
>>      response.raise_for_status()
>>    File "/Users/vkg/.pyenv/versions/notion-workspace/lib/python3.7/site-packages/requests/models.py", line 941, in raise_for_st
>>  atus
>>      raise HTTPError(http_error_msg, response=self)
>>  requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: https://www.notion.so/api/v3/loadUserContent

- Go to chrome, log into notion -> inspect -> application -> cookies -> token_v2
Will occasionally have to change as per the above instructions.
The error experienced was as follows:

- Change token_v2

## Current Fixes

- Have sourced a PR that has not been merged that addresses a paralyzing `get_block`
issue: https://github.com/jamalex/notion-py/pull/294#issuecomment-804306525

- A new error cropped up which is fixed in this PR along with the fix above: https://github.com/jamalex/notion-py/pull/352

## Helpful Info
https://pythonrepo.com/repo/jamalex-notion-py-python-third-party-apis-wrappers
