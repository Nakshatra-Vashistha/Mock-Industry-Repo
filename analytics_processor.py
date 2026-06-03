# analytics_processor.py – Version 2 (Correct wrapper added, bug still present)

def calculate_user_retention(user_data: dict):
    """
    Calculates user retention based on activity logs.
    BUG: No null-check or default for 'activity_logs'.
    """
    # Direct access – will raise KeyError if 'activity_logs' missing
    logs = user_data['activity_logs']
    # Splitting without checking if logs is None or empty
    active_days = logs.split(',')
    return len(active_days)


def process_daily_metrics(payload: dict):
    """
    Extracts user profile and passes it to calculate_user_retention.
    """
    user_profile = payload.get('user', {})
    retention = calculate_user_retention(user_profile)
    return {
        'user_id': payload.get('user_id'),
        'retention_days': retention
    }


def parse_webhook_event(event: dict):
    """
    New function – correctly extracts data from a modern webhook payload
    and calls process_daily_metrics. Even though this function is written
    perfectly, it will crash because the underlying calculate_user_retention
    lacks a null‑guard for 'activity_logs'.
    """
    # Extract relevant fields from the webhook payload
    user_data = {
        'user_id': event.get('payload', {}).get('user', {}).get('id'),
        'user': {
            'activity_logs': event.get('payload', {})
                           .get('user', {})
                           .get('activity_summary', {}).get('logs')
            # If 'logs' is missing or None, calculate_user_retention will fail
        }
    }
    # Call the existing (buggy) processing chain
    result = process_daily_metrics(user_data)
    result['webhook_processed'] = True
    return result