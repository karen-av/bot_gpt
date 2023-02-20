import openai

def respotnse_gpt(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        max_tokens=1000
    )
    return response

def check_user(user_id, USERS_ID):
    if str(user_id) in USERS_ID:
        return True
    return False


