from google import genai

# Initialize the client
client = genai.Client()

# Generate content
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)
