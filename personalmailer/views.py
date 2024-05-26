from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import openai
import os
from dotenv import load_dotenv
from .enhancedQueryParsing import query_emails_with_filters
from .utils import generate_human_readable_summary, extract_email_bodies
import json

load_dotenv()
# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@csrf_exempt
def mailer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            
            if not query:
                return JsonResponse({"error": "No query provided"}, status=400)
            
            results = query_emails_with_filters(query)
            if not results:
                return JsonResponse({"summary": "No results found."})
            
            email_bodies = extract_email_bodies(results)
            human_readable_summary = generate_human_readable_summary(email_bodies)
            return JsonResponse({"summary": human_readable_summary})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def fetch_csv_data(request):
    if request.method == 'GET':
        csv_file_path = 'emails.csv'
        
        try:
            df = pd.read_csv(csv_file_path)
            data = df.to_dict(orient="records")
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
