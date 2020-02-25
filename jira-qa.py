import os
import sys

from datetime import datetime

from jira import JIRA

qa_column = 'In Testing'

date_format = '%Y-%m-%dT%H:%M:%S.%f%z'

user = os.getenv('OM_JIRA_USER')
token = os.getenv('OM_JIRA_TOKEN')

options = {'server': 'https://ometria.atlassian.net/'}

jira = JIRA(options, basic_auth=(user, token))


def get_time_spent_in_qa(sprint):
    """
    Returns the time spent (in seconds) in the qa_column for each Jira issue
    """
    issues = jira.search_issues(f'Sprint={sprint}', expand='changelog')
    result = {}

    for issue in issues:
        summary = issue.fields.summary
        key = issue.key

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

        result[key] = {'summary': summary, 'time_in_qa': time_spent_in_qa.total_seconds()}

    return result


if __name__ == '__main__':
    sprint_id = sys.argv[1]
    if not sprint_id:
        print("Sprint ID missing")
        sys.exit()

    print(f"Time spent in QA in sprint {sprint_id}")
    results = get_time_spent_in_qa(sprint_id)
    for k,v in results.items():
        output = f"""
        Key:                   {k}
        Summary:               {v['summary']}
        Time in QA (minutes):  {round(v['time_in_qa']/60, 2)}
        ---
        """
        print(output)
