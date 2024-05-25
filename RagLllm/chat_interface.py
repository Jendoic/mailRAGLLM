import openai
from enhancedQueryParsing import query_emails_with_filters

# Set up your OpenAI API key
openai.api_key = 'sk-proj-2dsvG2wn88x9LMuRASQsT3BlbkFJA2sDDmnFsWWeSwTMeUFe'

def generate_human_readable_summary(email_bodies):
    # Prepare the prompt for GPT-4
    prompt = "Summarize the following email contents in an engaging, comprehensive, concise, brief and human-readable manner:\n\n"
    
    for body in email_bodies:
        prompt += f"{body}\n\n"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes email contents in an engaging, comprehensive, concise, brief and human-readable manner."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=8192,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].message['content'].strip()

def extract_email_bodies(emails):
    email_bodies = []
    for email in emails:
        body = email['body']
        email_bodies.append(body)
    return email_bodies

def main():
    print("Welcome to the Email Query System!")
    while True:
        query = input("Enter your query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        results = query_emails_with_filters(query)
        if not results:
            print("No results found.")
        else:
            email_bodies = extract_email_bodies(results)
            human_readable_summary = generate_human_readable_summary(email_bodies)
            print(human_readable_summary)

if __name__ == "__main__":
    main()
