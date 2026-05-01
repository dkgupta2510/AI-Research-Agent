import json
import os
import time
from datetime import datetime
from agent.searcher import search_web, read_url
from agent.llm import generate_react_step
from agent.prompt import build_react_prompt
from config import LOG_DIR

def save_log(query: str, result: dict) -> str:
    """Saves the result to a JSON log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(LOG_DIR, f"query_{timestamp}.json")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "result": result
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
        
    return filename

def run_agent(query: str) -> dict:
    """
    Autonomous ReAct Loop:
    The agent dynamically decides to search, read URLs, or provide a final answer.
    """
    print(f"\nInitializing Agent for query: '{query}'")
    
    history_text = build_react_prompt(query) + "\n\n--- BEGIN EXECUTION ---\n"
    
    max_steps = 6
    for step in range(1, max_steps + 1):
        print(f"Step {step}/{max_steps}: Thinking...")
        
        start_time = time.time()
        step_result = generate_react_step(history_text)
        
        if "error" in step_result:
            return step_result
            
        thought = step_result.get("thought", "")
        action = step_result.get("action", "")
        action_input = step_result.get("action_input", "")
        
        print(f"Thought: {thought}")
        print(f"Action: {action}({action_input}) ({(time.time() - start_time):.2f}s)")
        
        history_text += f"\nAgent Thought: {thought}\nAgent Action: {action}\nAction Input: {action_input}\n"
        
        if action == "final_answer":
            print("Agent has formulated a final answer.")
            final_data = action_input if isinstance(action_input, dict) else {}
            log_file = save_log(query, final_data)
            final_data["_log_file"] = log_file
            return final_data
            
        elif action == "search_web":
            print(f"Searching: {action_input}")
            results = search_web(str(action_input))
            observation = json.dumps(results, indent=2)
            print(f"Observation: Found {len(results)} URLs")
            
        elif action == "read_url":
            print(f"Reading: {action_input}")
            text = read_url(str(action_input))
            observation = f"Content from {action_input}:\n{text}"
            print(f"Observation: Extracted {len(text)} characters")
            
        else:
            observation = f"Error: Unknown action '{action}'"
            print(f"Warning: {observation}")
            
        history_text += f"Observation: {observation}\n"

    # If we run out of steps without a final answer
    print("Warning: Agent reached maximum steps.")
    fallback = {
        "question": query,
        "plan": [],
        "short_answer": "Agent reached maximum execution steps without formulating a final answer.",
        "key_findings": [],
        "sources": [],
        "confidence": "Low",
        "limitations": ["Reached max iterations", "Incomplete research"],
        "next_steps": ["Try a more specific query"]
    }
    log_file = save_log(query, fallback)
    fallback["_log_file"] = log_file
    return fallback
