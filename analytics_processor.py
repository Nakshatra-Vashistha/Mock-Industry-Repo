# analytics_processor.py – Version 1 (Buggy commit)

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