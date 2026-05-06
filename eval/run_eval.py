import os
import json
import time
import argparse
from eval_harness import ClaudeCodeEvaluator
from user_simulator import UserSimulator
from metrics_collector import MetricsCollector

def run_evaluation(target_dir, persona_description, branch_name):
    print(f"\n{'='*50}")
    print(f"Starting Evaluation on branch: {branch_name}")
    print(f"Target Directory: {target_dir}")
    print(f"Persona: {persona_description}")
    print(f"{'='*50}\n")

    evaluator = ClaudeCodeEvaluator(target_dir)
    simulator = UserSimulator(persona_description)
    collector = MetricsCollector(target_dir)

    # Note: We assume the target_dir is already a git repo with the plugin installed,
    # or that `claude` will work there. For a real run, we would copy the plugin files
    # or initialize a fresh git repo and install the plugin.

    # Initialize the project if not already done
    if not os.path.exists(os.path.join(target_dir, "docs", "shipflow")):
        print("Initializing ShipFlow...")
        evaluator.start_session()
        evaluator.run_command("/sf-init")
        time.sleep(2)
        evaluator.close()

    evaluator.start_session()

    # Run Discovery Phase
    print("\n--- Running Discovery Phase ---")
    evaluator.run_command(f'/sf-discover "{persona_description}"', wait_for_prompt=False)

    # Interactive Loop
    # We will loop for a maximum number of turns to prevent infinite loops
    max_turns = 10
    turns = 0

    while turns < max_turns:
        output = evaluator.wait_for_turn()
        print(f"\n[Claude]:\n{output}\n")

        if not output:
            break

        # Check if Claude is asking a question or waiting for input
        # If it seems like a question or prompt for user input, generate an answer
        if "?" in output[-500:] or ">" in output[-10:]:
            answer = simulator.answer_question(output)
            print(f"\n[Simulator User]: {answer}\n")
            evaluator.run_command(answer, wait_for_prompt=False)
            turns += 1
        else:
            # If it's just processing or we shouldn't answer, wait more or break
            # In a real scenario, we might need a more robust way to know when Discover is done.
            # For this script, we'll assume if it's not asking a question, it might be done or
            # we can force the next phase.
            break

    # Run Spec Phase
    print("\n--- Running Spec Phase ---")
    evaluator.run_command("/sf-spec", wait_for_prompt=True)

    evaluator.close()

    # Collect Metrics
    print("\n--- Collecting Metrics ---")
    metrics = collector.collect_all(simulator)

    # Calculate basic cost (mocked here, in reality would parse Claude logs)
    # This gives us a placeholder to compare against mono-agent
    metrics["token_cost_estimate"] = turns * 1000 # Rough estimate
    metrics["turn_count"] = turns

    # Save Report
    report = {
        "branch": branch_name,
        "persona": persona_description,
        "metrics": metrics
    }

    report_path = f"eval_report_{branch_name.replace('/', '_')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nEvaluation complete. Report saved to {report_path}")
    print(json.dumps(metrics, indent=2))

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShipFlow Evaluation Runner")
    parser.add_argument("--dir", default="./eval_target", help="Directory to run evaluation in")
    parser.add_argument("--persona", default="I want to build a simple habit tracker app. It should have a calendar view and streaks.", help="User persona/goal")
    parser.add_argument("--branch", default="current", help="Name of the branch being evaluated")

    args = parser.parse_args()

    # Ensure target directory exists and is empty-ish
    os.makedirs(args.dir, exist_ok=True)

    run_evaluation(args.dir, args.persona, args.branch)
