import openai
from celery import shared_task

openai.api_key = "your-openai-api-key"


@shared_task
def generate_summary_task(commit_diffs):
    text = "\n".join(commit_diffs)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a summary of the following changes:\n{text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary
