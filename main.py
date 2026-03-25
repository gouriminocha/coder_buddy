import argparse
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()
from agent.graph import agent


def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")

    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ")
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )
        print("\n==== MEMORY LOGS ====")

        if "coder_state" in result:
            for log in result["coder_state"].logs:
                print(log)
        else:
            print("No memory logs found ❌")
        print("Final State:", result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()