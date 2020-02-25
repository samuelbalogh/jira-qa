
```
mkvirtualenv jira-qa --python=python3
pip install -r requirements
export OM_JIRA_TOKEN=<your Jira token here>
export OM_JIRA_USER=<your email here>
python jira_qa.py <sprint ID>
```
