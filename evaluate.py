import sys
import json
from agent.orchestrator import run_agent

TEST_QUERIES = [
    "What is the capital of France?", # Simple, likely uses general knowledge or 1 quick search
    "Compare the features of modern electric vehicles in 2026.", # Complex, requires searching and synthesizing
    "This is gibberish: asdfqwerzxvc", # Should handle failure/missing data gracefully
]

def run_evaluation():
    print("Starting Automated Evaluation of AI Research Agent")
    print("="*60)
    
    score = 0
    total = len(TEST_QUERIES)
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{total}] Evaluating Query: '{query}'")
        try:
            result = run_agent(query)
            
            # Validation checks
            if "error" in result:
                print(f"FAILED: Agent threw an error: {result['error']}")
                continue
                
            if not result.get("question") or not result.get("confidence"):
                print("FAILED: Missing essential structured JSON fields.")
                continue
                
            print(f"PASSED: Answer length: {len(result.get('short_answer', ''))} | Confidence: {result.get('confidence')}")
            score += 1
            
        except Exception as e:
            print(f"CRITICAL FAILURE on query '{query}': {e}")
            
    print("\n" + "="*60)
    print(f"Evaluation Complete. Score: {score}/{total} ({score/total*100:.1f}%)")
    
if __name__ == "__main__":
    run_evaluation()
