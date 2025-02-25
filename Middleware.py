import LarkController as lark

def process_event(event, data):
    """
    Process GitHub events and send a corresponding message to a Lark group.

    Args:
        event (str): The type of the GitHub event (e.g., 'push', 'pull_request').
        data (dict): The payload data from the GitHub event.
    
    Returns:
        None
    """
    message = ''
    
    if event == 'push':
        # Handle push events
        branch = data['ref'].split('/').pop()  # Extract branch name from ref
        commits = '\n'.join([f"- {commit['message']} by {commit['author']['name']}" for commit in data['commits']])
        message = f"New push to {data['repository']['name']} on branch {branch} by {data['pusher']['name']}:\n{commits}"
    
    elif event == 'pull_request':
        # Handle pull request events
        source_branch = data['pull_request']['head']['ref']
        target_branch = data['pull_request']['base']['ref']
        message = f"New pull request #{data['number']} in {data['repository']['name']} from {source_branch} to {target_branch}."
    
    else:
        # Handle other events
        message = f"New event: {event}"
    
    print('Message to send to Lark:', message)
    lark.send_message_to_lark_group(message)
