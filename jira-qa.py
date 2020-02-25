import os

from datetime import datetime

from jira import JIRA
from flask import Flask, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sprint = '76'
qa_column = 'In Testing'

date_format = '%Y-%m-%dT%H:%M:%S.%f%z'

user = os.getenv('OM_JIRA_USER')
token = os.getenv('OM_JIRA_TOKEN')

options = {'server': 'https://ometria.atlassian.net/'}

jira = JIRA(options, basic_auth=(user, token))


def get_time_spent_in_qa(sprint):
    issues = jira.search_issues(f'Sprint={sprint}', expand='changelog')
    result = {}

    for issue in issues:
        summary = issue.fields.summary
        changelog = issue.changelog
    
        transitioned_to_testing = None
        transitioned_from_testing = None
    
        for history in changelog.histories:
    
            created_at = history.created
    
            for item in history.items:
                if item.field == 'status':
                    if item.toString == qa_column:
                        transitioned_to_testing = datetime.strptime(created_at, date_format)
                    if item.fromString == qa_column:
                        transitioned_from_testing = datetime.strptime(created_at, date_format)
    
        if not all([transitioned_to_testing, transitioned_from_testing]):
            continue
        
        time_spent_in_qa = transitioned_from_testing - transitioned_to_testing
    
        result[summary] = time_spent_in_qa.total_seconds()

    return result


@app.route('/qa-time/<sprint>')
def qa_time(sprint):
    result = get_time_spent_in_qa(sprint)
    response = make_response(result, 200)
    return response

if __name__ == '__main__':
    app.run()
