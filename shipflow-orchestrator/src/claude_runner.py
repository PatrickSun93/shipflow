import subprocess
import json
import os
import shlex
import logging

logger = logging.getLogger(__name__)

class ClaudeRunner:
    """
    A wrapper around the Claude Code CLI to spawn agents and orchestrate tasks.
    """
    def __init__(self, plugin_dir: str = None, cwd: str = None):
        """
        :param plugin_dir: Optional path to the shipflow plugin directory.
                           If provided, adds `--plugin-dir` to the command.
        :param cwd: Optional working directory where Claude should be executed.
        """
        self.plugin_dir = plugin_dir
        self.cwd = cwd or os.getcwd()

    def run_command(self, prompt: str, system_prompt_file: str = None) -> str:
        """
        Executes a prompt using the claude CLI.

        :param prompt: The input prompt to send to claude.
        :param system_prompt_file: Path to a markdown file containing the agent's instructions.
        :return: The stdout output from the claude CLI.
        """
        cmd = ["claude"]

        if self.plugin_dir:
            cmd.extend(["--plugin-dir", self.plugin_dir])

        cmd.extend(["-p", prompt])

        # If we need to pass a specific system prompt (agent persona)
        # Note: Depending on claude cli implementation, we might pass it via a specific flag
        # or append it to the prompt. We'll append it for now or use a hypothetical --system flag.
        # Assuming claude CLI doesn't have --system, we will prefix the prompt with the file content.
        if system_prompt_file and os.path.exists(system_prompt_file):
            with open(system_prompt_file, "r", encoding="utf-8") as f:
                system_content = f.read()
            prompt = f"{system_content}\n\nUser Task:\n{prompt}"
            # Rebuild cmd with the updated prompt
            cmd[-1] = prompt

        logger.debug(f"Executing: {' '.join(shlex.quote(c) for c in cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Claude CLI failed with exit code {e.returncode}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise RuntimeError(f"Claude CLI failed: {e.stderr}") from e

    def spawn_subagent(self, agent_file_path: str, task_prompt: str) -> str:
        """
        Spawns a specific subagent with a task prompt.

        :param agent_file_path: Path to the agent's markdown definition (e.g., shipflow/agents/discovery-moderator.md)
        :param task_prompt: The specific task for the agent.
        :return: The output from the agent.
        """
        return self.run_command(prompt=task_prompt, system_prompt_file=agent_file_path)
