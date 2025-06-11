from datetime import datetime, timedelta

def get_iso_time(hours_ago=24):
    return (datetime.now() - timedelta(hours=hours_ago)).isoformat()