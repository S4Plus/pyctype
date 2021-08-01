import requests
import json
import git

# import os
# os.environ["GIT_PYTHON_REFRESH"] = "quiet"
# &access_token=?


url_python_repos = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=100&page={}"

url_search_code = "https://api.github.com/search/code?q=from+PIL+import+in:file+language:python+repo:{}"

def query(s):
    return json.loads(requests.get(s).content.decode('UTF-8'))

for i in range(1, 3):
    try:
        repos = query(url_python_repos.format(i))
        for repo in repos['items']:
            search = query(url_search_code.format(repo['full_name']))
            if search['total_count']:
                print(repo['stargazers_count'], repo['html_url'])
    except Exception as e:
        print(search)