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
        print(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {' '.join(command)}")
        print(f"Error: {e.stderr.strip()}")
        return False

def auto_commit(test_mode=False):
    is_github_action = os.getenv("GITHUB_ACTIONS") == "true"
    
    # 1. Identity Setup (Crucial for CI)
    if is_github_action:
        username = "winterc0ldsye" if "Github-Auto" in os.getcwd() else "DacterMonster"
        email = "winterc0ldsye@gmail.com" if "Github-Auto" in os.getcwd() else "fcfaisal51@gmail.com"
        run_git_command(["git", "config", "user.name", username])
        run_git_command(["git", "config", "user.email", email])

    # 2. Delay Strategy
    if not test_mode:
        delay = random.randint(10, 60) if is_github_action else random.randint(300, 1800)
        print(f"Initial delay: {delay} seconds")
        time.sleep(delay)

    num_commits = 1 if test_mode else 100
    print(f"Batch size: {num_commits}")

    for i in range(num_commits):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("daily_log.txt", "a") as f:
            f.write(f"Commit {i+1}/{num_commits} at {now}\n")
        
        message = random.choice(COMMIT_MESSAGES)
        if test_mode: message = f"test: {message}"
        
        run_git_command(["git", "add", "daily_log.txt"])
        # We use --allow-empty just in case, though file always changes
        if not run_git_command(["git", "commit", "--allow-empty", "-m", message]):
            print("Abort: Commit failed.")
            sys.exit(1)
        
        if i < num_commits - 1 and not test_mode:
            wait = random.randint(2, 10) if is_github_action else random.randint(30, 60)
            time.sleep(wait)

    # 3. Pull-Rebase-Push Strategy (The Final Boss of Reliability)
    print("Finalizing updates...")
    if is_github_action:
        # Pull latest changes just in case something happened while we were committing
        run_git_command(["git", "pull", "--rebase", "origin", "main"])
        
    if run_git_command(["git", "push", "origin", "HEAD"]):
        print("DONE: All changes pushed successfully.")
    else:
        print("FAILED: Push blocked. Check 'Workflow permissions' in GitHub Settings.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    auto_commit(test_mode=args.test)
