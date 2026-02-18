import os
from groq import Groq, GroqError, InternalServerError, AuthenticationError
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def paraphrase_text(text: str) -> str:
    """
    Sends text to Groq API (Llama 3) for high-speed paraphrasing.
    """
    if not text.strip():
        raise ValueError("No text provided for paraphrasing.")

    try:
        response = client.chat.completions.create(
            # Using Llama 3.3 70B for high quality, or 8B for extreme speed
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a text simplification assistant. Rewrite the following text to make it clearer and easier to understand, while preserving all the original meaning. Return only the rewritten text, nothing else.",
                },
                {"role": "user", "content": f"Text: {text}"},
            ],
            max_tokens=1024,
            temperature=0.5,  # Lower temperature = more focused/consistent results
        )
        return response.choices[0].message.content.strip()

    except AuthenticationError:
        raise RuntimeError("Invalid Groq API key, check your .env file.")
    except InternalServerError:
        raise RuntimeError("Groq server is currently busy, try again later.")
    except GroqError as e:
        raise RuntimeError(f"Groq API error: {str(e)}")
