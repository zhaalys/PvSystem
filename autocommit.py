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
    # 1. Random Delay (0 to 60 minutes) to make it look natural
    # Note: For GitHub Actions, we don't want to wait *too* long as there's a timeout,
    # but 0-1 hour is usually fine and adds good jitter.
    delay_minutes = random.randint(0, 60)
    print(f"Waiting for {delay_minutes} minutes before committing...")
    time.sleep(delay_minutes * 60)

    # 2. Update the log file
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("daily_log.txt", "a") as f:
        f.write(f"Log entry at: {now}\n")
    
    # 3. Choose a random commit message
    message = random.choice(COMMIT_MESSAGES)
    
    # 4. Git Push process
    print(f"Executing commit: {message}")
    if run_git_command(["git", "add", "daily_log.txt"]):
        if run_git_command(["git", "commit", "-m", message]):
            if run_git_command(["git", "push"]):
                print("Successfully pushed to repository.")
            else:
                print("Failed to push.")
        else:
            print("Nothing to commit or commit failed.")
    else:
        print("Failed to add file.")

if __name__ == "__main__":
    auto_commit()
