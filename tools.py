# ddgs_agent.py
from dotenv import load_dotenv
import os
from ddgs import DDGS
from langchain_core.tools import tool
import ast
import math

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("open_api_key")
OPENAI_BASE_URL = os.getenv("openApiBaseUrl")  # optional

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -----------------------------
# DuckDuckGo search tool
# -----------------------------
@tool
def search_web(query: str, num_res: int = 5) -> str:
    """Search the web using DuckDuckGo and return the top results."""
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
            if len(snippet) > 300:
                snippet = snippet[:300] + "..."
            formatted_results.append(f"{i}. {title}\nURL: {url}\nSnippet: {snippet}\n")
        return "\n".join(formatted_results)
    except Exception as e:
        return f"An error occurred while searching the web: {str(e)}"

# -----------------------------
# Safe calculation tool
# -----------------------------
@tool
def Calculate(expression: str) -> str:
    """Calculate a mathematical expression safely."""
    try:
        node = ast.parse(expression, mode='eval')

        allowed_nodes = {
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Load,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
            ast.USub, ast.UAdd, ast.Call, ast.Name, ast.Constant
        }

        allowed_functions = {
            'sqrt': math.sqrt,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }

        for n in ast.walk(node):
            if type(n) not in allowed_nodes:
                raise ValueError(f"Disallowed expression: {type(n).__name__}")
            if isinstance(n, ast.Call):
                if not isinstance(n.func, ast.Name) or n.func.id not in allowed_functions:
                    raise ValueError(f"Disallowed function: {n.func.id}")

        code = compile(node, '<string>', 'eval')
        result = str(eval(code, {"__builtins__": None}, allowed_functions))
        return result
    except Exception as e:
        return f"Error in calculation: {str(e)}"
