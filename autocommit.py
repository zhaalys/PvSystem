import random
import time
import subprocess
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
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {' '.join(command)}: {e.stderr}")
        return False
    return True

def auto_commit():
    # 1. Random Delay before starting (0 to 30 minutes)
    start_delay = random.randint(0, 30)
    print(f"Waiting for {start_delay} minutes before starting batch...")
    time.sleep(start_delay * 60)

    # Deciding number of commits for this session (Fixed 5 as requested)
    num_commits = 5
    print(f"Planned commits for this session: {num_commits}")

    for i in range(num_commits):
        # 2. Update the log file
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("daily_log.txt", "a") as f:
            f.write(f"Log entry {i+1}/{num_commits} at: {now}\n")
        
        # 3. Choose a random commit message
        message = random.choice(COMMIT_MESSAGES)
        
        # 4. Git Add and Commit
        print(f"Executing commit {i+1}/{num_commits}: {message}")
        if run_git_command(["git", "add", "daily_log.txt"]):
            if run_git_command(["git", "commit", "-m", message]):
                print("Commit successful.")
            else:
                print("Commit failed.")
        
        # Short random delay between commits (1 to 5 minutes) so timestamps vary
        if i < num_commits - 1:
            wait_time = random.randint(60, 300)
            time.sleep(wait_time)

    # 5. Push all at once at the end
    if run_git_command(["git", "push"]):
        print("Successfully pushed all commits to repository.")
    else:
        print("Failed to push.")

if __name__ == "__main__":
    auto_commit()
