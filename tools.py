# ddgs_agent.py

from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from ddgs import DDGS

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("openApiKey")
OPENAI_BASE_URL = os.getenv("openApiBaseUrl")  # optional

if OPENAI_API_KEY is None:
    raise ValueError("Please set 'openApiKey' in your .env file")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -----------------------------
# Define DuckDuckGo search tool
# -----------------------------
def search_web(query: str, num_res: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return the top results.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_res))

        if not results:
            return f"No results found for '{query}'"

        formatted_results = [f"Top {num_res} results for '{query}':\n"]

        for i, result in enumerate(results, start=1):
            title = result.get("title", "No Title")
            url = result.get("href", "No URL")
            snippet = result.get("body", "No Snippet")
            # Trim snippet to 300 chars
            if len(snippet) > 300:
                snippet = snippet[:300] + "..."
            formatted_results.append(
                f"{i}. {title}\nURL: {url}\nSnippet: {snippet}\n"
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"An error occurred while searching the web: {str(e)}"