import pandas as pd
import openai

openai.api_key = 'sk-proj-9RpVp58Bseeqzy7yJYgIT3BlbkFJYnz3LINeg4bTSfDRfdYg'
def generate_human_readable_summary(email_bodies):
    # Prepare the initial part of the prompt for GPT-4
    prompt = """Write a friendly and detailed brief about the following topics. Provide the information in a clear, organized manner with headings and bullet points. Include a summary or call to action at the end. Make sure the entire response is within 8149 tokens. Here are the details:

1. **[Title of the first topic]**
   - **Details:** [Details about the first topic]

2. **[Title of the second topic]**
   - **Details:** [Details about the second topic]

3. **[Title of the third topic]**
   - **Details:** [Details about the third topic]

[Continue this format for all topics provided]

### Summary or Call to Action:
Provide a brief summary or call to action based on the topics covered. Be friendly and encouraging. 

Ensure the entire response, including all topics and this summary, is within 8149 tokens.

Warm Regards,  
[Your Name or Team Name]

Include any relevant links or additional information here.

"""
    
    max_tokens_for_completion = 2048  # Leave space for the completion to ensure we don't exceed the limit
    token_budget = 8192 - max_tokens_for_completion - len(prompt.split())
    
    chunks = []
    current_chunk = ""
    
    for body in email_bodies:
        body_tokens = len(body.split())
        if len(current_chunk.split()) + body_tokens < token_budget:
            current_chunk += body + "\n\n"
        else:
            chunks.append(current_chunk)
            current_chunk = body + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    summaries = []
    for chunk in chunks:
        full_prompt = prompt + chunk
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=max_tokens_for_completion,
            n=1,
            stop=None,
            temperature=0.7,
        )
        summaries.append(response.choices[0].message['content'].strip())
    
    return "\n\n".join(summaries)

def extract_email_bodies(emails):
    email_bodies = []
    for email in emails:
        body = email['body']
        email_bodies.append(body)
    return email_bodies