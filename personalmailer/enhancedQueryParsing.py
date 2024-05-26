from datetime import datetime
from .ragSystem import query_emails

def parse_query(query):
    # Basic example of parsing a query for a specific sender and date range
    parts = query.split(" ")
    sender = None
    start_date = None
    end_date = None
    
    for part in parts:
        if "from:" in part:
            sender = part.replace("from:", "")
        elif "start:" in part:
            start_date = datetime.strptime(part.replace("start:", ""), "%Y-%m-%d")
        elif "end:" in part:
            end_date = datetime.strptime(part.replace("end:", ""), "%Y-%m-%d")

    return sender, start_date, end_date

def query_emails_with_filters(query):
    sender, start_date, end_date = parse_query(query)
    results = query_emails(query)
    
    if sender:
        results = [result for result in results if sender.lower() in result['from'].lower()]
    if start_date:
        results = [result for result in results if datetime.strptime(result['date'], "%a, %d %b %Y %H:%M:%S %z") >= start_date]
    if end_date:
        results = [result for result in results if datetime.strptime(result['date'], "%a, %d %b %Y %H:%M:%S %z") <= end_date]
    
    return results
