
```
mkvirtualenv jira-qa --python=python3
pip install -r requirements
export OM_JIRA_TOKEN=<your Jira token here>
export OM_JIRA_USER=<your email here>
python jira_qa.py <sprint ID>
```

> Note: you might have to modify the `qa_column` in the script so that it conforms to your conventions
