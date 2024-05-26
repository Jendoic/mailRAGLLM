from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import pandas as pd
import openai
import logging
from enhancedQueryParsing import query_emails_with_filters
from utils import generate_human_readable_summary, extract_email_bodies

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/mailer', methods=['POST'])
def mailer():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    results = query_emails_with_filters(query)
    if not results:
        return jsonify({"summary": "No results found."})
    
    email_bodies = extract_email_bodies(results)
    human_readable_summary = generate_human_readable_summary(email_bodies)
    return jsonify({"summary": human_readable_summary})


# @app.route('/twilio/whatsapp', methods=['POST'])
# def whatsapp():
#     incoming_msg = request.form.get('Body')
#     logging.debug(f"Incoming message: {incoming_msg}")
#     response = MessagingResponse()
#     if incoming_msg:
#         results = query_emails_with_filters(incoming_msg)
#         if not results:
#             response.message("No results found.")
#         else:
#             email_bodies = extract_email_bodies(results)
#             human_readable_summary = generate_human_readable_summary(email_bodies)
#             response.message(human_readable_summary)
#     else:
#         response.message("Please provide a query.")
        
#     logging.debug(f"Response: {str(response)}")
#     return str(response)



@app.route('/fetch-csv-data', methods=['GET'])
def fetchCsvData():
    csvFilePath = 'emails.csv'
    
    try:
        df = pd.read_csv(csvFilePath)
        
        data = df.to_dict(orient="records",)
        
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}), 500
   
   
    
if __name__ == '__main__':
    app.run(port=8000, debug=True)