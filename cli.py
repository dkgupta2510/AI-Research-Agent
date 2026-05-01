import argparse
import sys
import json
from agent.orchestrator import run_agent

def print_result(result: dict):
    """Pretty prints the JSON result to the terminal."""
    if "error" in result:
        print(f"\nError: {result['error']}")
        return

    print("\n" + "="*60)
    print(f"Question   : {result.get('question', 'N/A')}")
    print(f"Confidence : {result.get('confidence', 'N/A')}")
    print("="*60)
    
    plan = result.get('plan', [])
    if plan:
        print("\nPlan:")
        for idx, pt in enumerate(plan, 1):
            print(f"  {idx}. {pt}")
            
    print(f"\nAnswer:\n{result.get('short_answer', result.get('answer', 'No answer provided.'))}")
    
    points = result.get('key_findings', result.get('points', []))
    if points:
        print("\nKey Findings:")
        for pt in points:
            print(f"  * {pt}")
            
    limitations = result.get('limitations', [])
    if limitations:
        print("\nLimitations:")
        for pt in limitations:
            print(f"  - {pt}")
            
    next_steps = result.get('next_steps', [])
    if next_steps:
        print("\nNext Steps:")
        for pt in next_steps:
            print(f"  > {pt}")
            
    sources = result.get('sources', [])
    if sources:
        print("\nSources used:")
        for src in sources:
            print(f"  - {src}")
            
    log_file = result.get('_log_file')
    if log_file:
        print(f"\nSaved to : {log_file}")
    
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="AI Research Agent CLI")
    parser.add_argument("--query", "-q", type=str, help="Single query to ask the agent")
    args = parser.parse_args()

    if args.query:
        # Single shot mode
        result = run_agent(args.query)
        print_result(result)
    else:
        # Interactive mode
        print("Welcome to the AI Research Agent! (Type 'exit' or 'quit' to stop)")
        while True:
            try:
                query = input("\n> Ask a question: ").strip()
                if query.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                if not query:
                    continue
                
                result = run_agent(query)
                print_result(result)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
