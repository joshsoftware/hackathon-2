import json
import re
from typing import Dict, List, Optional
import ollama

from prompt import EVENT_ANALYSIS_PROMPT

LLM = "llama3"
TEMPERATURE = 0.2

def create_prompt(
    frontend_events: List[Dict], 
    backend_events: List[Dict], 
    frontend_logs: List[Dict], 
    backend_logs: List[Dict]
) -> str:
    """
    Generates a prompt by replacing placeholders in `EVENT_ANALYSIS_PROMPT` with 
    JSON-formatted frontend and backend events and logs.

    Args:
        - frontend_events (List[Dict]): Frontend analytical events.
        - backend_events (List[Dict]): Backend analytical events.
        - frontend_logs (List[Dict]): Frontend error logs.
        - backend_logs (List[Dict]): Backend error logs.

    Returns:
        str: The formatted prompt with data in place of placeholders.

    Example:
        - Input:
            frontend_events = [{"id": 1}], backend_events = [{"id": 2}], 
            frontend_logs = [{"id": "log1"}], backend_logs = [{"id": "log2"}]
        - Output:
            A formatted string with the provided data in JSON format.

    Raises:
        - ValueError: If inputs are not lists of dictionaries.
    """
    
    # Serialize inputs to JSON strings
    fe_events_json = json.dumps(frontend_events, indent=2)
    be_events_json = json.dumps(backend_events, indent=2)
    fe_logs_json = json.dumps(frontend_logs, indent=2)
    be_logs_json = json.dumps(backend_logs, indent=2)
    
    # Replace placeholders in the prompt
    prompt = EVENT_ANALYSIS_PROMPT
    prompt = prompt.replace("<FE_EVENTS>", fe_events_json)
    prompt = prompt.replace("<BE_EVENTS>", be_events_json)
    prompt = prompt.replace("<FE_LOGS>", fe_logs_json)
    prompt = prompt.replace("<BE_LOGS>", be_logs_json)
    
    return prompt
    
def analyse_events_and_logs(
    frontend_events: List[Dict], 
    backend_events: List[Dict], 
    frontend_logs: List[Dict], 
    backend_logs: List[Dict]
) -> Optional[Dict]:
    """
    Analyzes frontend and backend events and logs using an LLM model and returns structured insights.

    Args:
        - frontend_events (List[Dict]): Frontend analytical events.
        - backend_events (List[Dict]): Backend analytical events.
        - frontend_logs (List[Dict]): Frontend error logs.
        - backend_logs (List[Dict]): Backend error logs.

    Returns:
        Optional[Dict]: Parsed JSON response from the LLM containing event analysis, or `None` if parsing fails.

    Steps:
        - 1. Generates a prompt using `create_prompt`.
        - 2. Sends the prompt to the LLM via `ollama.chat`.
        - 3. Extracts and parses the JSON content from the LLM response.
        - 4. Returns the parsed JSON or `None` if the response is invalid.

    Example:
        - Input:
            frontend_events = [{"id": 1}], backend_events = [{"id": 2}],
            frontend_logs = [{"id": "log1"}], backend_logs = [{"id": "log2"}]
        - Output:
            Parsed JSON structure with event insights, or `None` if invalid.

    Raises:
        None: Handles parsing errors gracefully by returning `None`.
    """
    
    prompt = create_prompt(
        frontend_events=frontend_events,
        backend_events=backend_events,
        frontend_logs=frontend_logs,
        backend_logs=backend_logs
    )
    
    response = ollama.chat(
        model=LLM,
        options={"temperature": TEMPERATURE},
        messages=[{"role": "user", "content": prompt}],
    )
    
    response_text = response.get("message", {}).get("content", "")
    response_text_json = re.search(r"\{.*\}", response_text, re.DOTALL)
    
    if response_text_json:
        try:
            response_text_json = json.loads(response_text_json.group())
        except json.JSONDecodeError as e:
            response_text_json = None
    else:
        response_text_json = None

    return response_text_json