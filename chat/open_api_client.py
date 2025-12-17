import google.generativeai as genai
genai.configure(api_key="AIzaSyBhJuWfpO8GDE2YvCRkWBG3KO7Gv3yOyvg")

class GeminiClient:
    def __init__(self):
        pass

    def chat_client(self, message: str):
        response = genai.chat.create(
            model="gemini-2.0-flash", 
            messages=[
                {"author": "system", "content": "You are a helpful assistant."},
                {"author": "user", "content": message},
            ],
            max_output_tokens=50
        )
        return response["candidates"][0]["content"]
