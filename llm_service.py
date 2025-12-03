import os
from dotenv import load_dotenv
from google import genai
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GenAI client once
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def auto_categorize(note: str) -> tuple[str, str]:
    """
    Categorize an expense note and predict if it's Income or Expense.
    
    Args:
        note (str): The transaction note/description.
    
    Returns:
        tuple: (category, entry_type) e.g. ("Food", "Expense")
    """
    prompt = f"""
    Categorize this note into one of these categories: Food, Transportation, Entertainment, Other.
    Also predict if it is an Income or Expense.
    
    Note: {note}
    
    Output format: Category | Type
    Example: Food | Expense
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(temperature=0.0)
        )
        # Expecting format: "Food | Expense"
        result = response.text.strip()
        if "|" in result:
            category, entry_type = map(str.strip, result.split("|"))
        else:
            # fallback if output is not in expected format
            category, entry_type = result, "Expense"
        return category, entry_type
    except Exception as e:
        logger.error(f"LLM categorization failed for note: '{note}'. Error: {e}")
        return "Other", "Expense"

# Example usage
if __name__ == "__main__":
    note = "Uber ride to office"
    category, entry_type = auto_categorize(note)
    print(f"Note: {note} | Category: {category} | Type: {entry_type}")
