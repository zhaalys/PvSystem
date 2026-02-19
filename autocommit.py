import random
import time
import subprocess
import sys
import argparse
import os
from datetime import datetime

# List of professional developer-style commit messages
COMMIT_MESSAGES = [
    "refactor: optimize internal log structure",
    "docs: update maintenance logs",
    "fix: minor tweak in logging format",
    "chore: daily system health check",
    "style: format daily_log.txt",
    "refactor: improve log readability",
    "docs: update documentation for internal processes",
    "feat: add entry to daily_log",
    "fix: resolve minor inconsistency in logs",
    "chore: routine maintenance",
    "docs: sync activity logs",
    "refactor: clean up log entries"
]

def run_git_command(command):
    try:
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"STDOUT: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {' '.join(command)}:")
        print(f"Exit code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def auto_commit(test_mode=False):
    is_github_action = os.getenv("GITHUB_ACTIONS") == "true"
    
    if is_github_action:
        print("--- CI DEBUG INFO ---")
        run_git_command(["git", "--version"])
        run_git_command(["git", "config", "--list"])
        print(f"Current Directory: {os.getcwd()}")
        print("---------------------")

    if not test_mode:
        # 1. Random Delay before starting
        start_delay = random.randint(0, 30)
        print(f"Waiting for {start_delay} minutes before starting batch...")
        if not is_github_action:
            time.sleep(start_delay * 60)
        else:
            print("Detected GitHub Actions. Using shorter delay (1-2 min) to avoid timeout/idle.")
            time.sleep(random.randint(30, 120))
    else:
        print("Running in TEST MODE. Skipping initial delay.")

    # Deciding number of commits for this session
    num_commits = 1 if test_mode else 100
    print(f"Planned commits for this session: {num_commits}")

    for i in range(num_commits):
        # 2. Update the log file
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("daily_log.txt", "a") as f:
            f.write(f"Log entry {i+1}/{num_commits} at: {now}\n")
        
        # 3. Choose a random commit message
        message = random.choice(COMMIT_MESSAGES)
        if test_mode:
            message = f"test: {message}"
        
        # 4. Git Add and Commit
        print(f"Executing commit {i+1}/{num_commits}: {message}")
        run_git_command(["git", "add", "daily_log.txt"])
            
        # Using --allow-empty to prevent failure if git thinks nothing changed
        if not run_git_command(["git", "commit", "--allow-empty", "-m", message]):
            print("Git commit failed. Exiting.")
            sys.exit(1)
        
        print(f"Commit {i+1} successful.")
        
        # Short random delay between commits
        if i < num_commits - 1 and not test_mode:
            # Very short delays for CI to handle 100 commits quickly
            wait_time = random.randint(5, 15) if is_github_action else random.randint(30, 90)
            print(f"Waiting for {wait_time} seconds before next commit...")
            time.sleep(wait_time)

    # 5. Push all at once at the end
    print("Pushing all commits to remote...")
    push_command = ["git", "push"]
    if is_github_action:
        # Explicit push to current branch
        push_command = ["git", "push", "origin", "HEAD"]
        
    if run_git_command(push_command):
        print("Successfully pushed all commits to repository.")
    else:
        print("Failed to push. Possible permission issue (Check Workflow Permissions in Settings).")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-commit script.")
    parser.add_argument("--test", action="store_true", help="Run in test mode (1 commit, no delays)")
    args = parser.parse_args()
    
    auto_commit(test_mode=args.test)
