from celery_worker import celery_app
from crew_runner import run_crew

def make_json_safe(result):
    # If it's a dict, list, str, int, float, bool, or None, return as is
    if isinstance(result, (dict, list, str, int, float, bool, type(None))):
        return result
    # Otherwise, return string representation
    return str(result)

@celery_app.task
def analyze_blood_report_task(query, file_path):
    print("TASK STARTED", query, file_path)
    result = run_crew(query, file_path)
    # Always return a JSON-serializable result
    return make_json_safe(result)