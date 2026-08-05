# ShipFlow Evaluation Framework

This directory contains the automated evaluation framework used to compare different architectural approaches in ShipFlow (e.g., multi-agent vs. mono-agent).

## Components

1. **`eval_harness.py`**: Uses `pexpect` to drive the `claude` CLI, initiating sessions, sending commands, and capturing outputs.
2. **`user_simulator.py`**: A lightweight LLM-based user simulator. It uses either an OpenAI-compatible API (like DeepSeek) or a local Ollama instance to dynamically answer questions posed by the ShipFlow agents during the Discover phase.
3. **`metrics_collector.py`**: Gathers evaluation metrics. It performs deterministic checks (format validation, read budget analysis, multi-agent blocks) and uses the LLM to judge subjective quality (spec completeness, story breakdown quality, edge cases caught).
4. **`run_eval.py`**: The main entry point. It orchestrates the process, creating a test environment, running the Discover and Spec phases, collecting metrics, and outputting a JSON report.

## Usage

You can run the evaluation framework by specifying the target directory, user persona, and branch name.

```bash
# Export the required API keys for the User Simulator and Judge
export SIMULATOR_API_BASE="https://api.deepseek.com"
export SIMULATOR_API_KEY="your-deepseek-api-key"
export SIMULATOR_MODEL="deepseek-chat"

# Run the evaluation
python eval/run_eval.py --dir ./eval_target --persona "I want to build a simple habit tracker app..." --branch main
```

## Comparing Branches

To compare the multi-agent approach with the mono-agent approach:

1. Checkout `main`.
2. Run the evaluation: `python eval/run_eval.py --dir ./eval_main --branch main`
3. Checkout the mono-agent branch (`experiment/mono-agent`).
4. Run the evaluation: `python eval/run_eval.py --dir ./eval_mono --branch mono-agent`
5. Compare the output JSON files: `eval_report_main.json` vs `eval_report_mono-agent.json`.
