import pexpect
import sys
import time
import os
import json

class ClaudeCodeEvaluator:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.child = None

    def start_session(self):
        print(f"Starting Claude Code in {self.target_dir}...")
        os.makedirs(self.target_dir, exist_ok=True)
        # Using unbuffer to avoid buffering issues with pexpect
        # We run the command via shell to ensure nvm/node paths are picked up if needed
        # Or just call claude directly
        cmd = f"cd {self.target_dir} && claude"
        self.child = pexpect.spawn('/bin/bash', ['-c', cmd], encoding='utf-8', timeout=120)

        # Log output to stdout for debugging
        self.child.logfile_read = sys.stdout

        # Wait for the initial prompt (this might need adjustment depending on Claude's CLI output)
        try:
            self.child.expect([r'>\s*', pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        except pexpect.TIMEOUT:
            print("Timeout waiting for Claude Code to start.")

    def run_command(self, command, wait_for_prompt=True):
        print(f"\n[Evaluator] Running command: {command}")
        self.child.sendline(command)
        if wait_for_prompt:
            self.wait_for_turn()

    def wait_for_turn(self):
        # We need to detect when Claude is done generating and waiting for user input.
        # This usually looks like a prompt "> " or similar.
        # Sometimes Claude might ask a question.
        try:
            # We look for the common prompt indicator
            index = self.child.expect([r'>\s*', pexpect.EOF, pexpect.TIMEOUT], timeout=300)
            if index == 1:
                print("Claude session ended unexpectedly.")
            elif index == 2:
                print("Timeout waiting for Claude response.")
            return self.child.before
        except pexpect.TIMEOUT:
            print("Timeout waiting for Claude turn.")
            return ""

    def close(self):
        if self.child and self.child.isalive():
            self.child.sendline('/exit')
            self.child.close()

if __name__ == "__main__":
    # Simple test to verify the harness can start
    evaluator = ClaudeCodeEvaluator(target_dir="./test_env")
    evaluator.start_session()
    # Let's see if we can get basic version info or help
    evaluator.run_command("/help")
    time.sleep(2)
    evaluator.close()
    print("Harness setup test complete.")
