import random
import subprocess
import sys
import os
from datetime import datetime

# Commit messages yang profesional
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

TOTAL_COMMITS = 50

def run_git(command):
    print(f"  > {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        return False
    return True

def main():
    print("=" * 50)
    print("  AUTO COMMIT - 50 Commits Per Day")
    print("=" * 50)
    print()

    # Cek apakah di dalam git repo
    if not os.path.exists(".git"):
        print("ERROR: Bukan git repository! Jalankan di folder project.")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)

    # Pull dulu biar sync
    print("Syncing dengan GitHub...")
    run_git(["git", "pull", "--rebase", "origin", "main"])
    print()

    print(f"Memulai {TOTAL_COMMITS} commits...\n")

    for i in range(TOTAL_COMMITS):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("daily_log.txt", "a") as f:
            f.write(f"Commit {i+1}/{TOTAL_COMMITS} at: {now}\n")

        message = random.choice(COMMIT_MESSAGES)
        run_git(["git", "add", "daily_log.txt"])

        if not run_git(["git", "commit", "--allow-empty", "-m", message]):
            print(f"\nGAGAL di commit {i+1}!")
            input("\nTekan Enter untuk keluar...")
            sys.exit(1)

        progress = int((i + 1) / TOTAL_COMMITS * 100)
        bar = "█" * (progress // 2) + "░" * (50 - progress // 2)
        print(f"  [{bar}] {progress}% ({i+1}/{TOTAL_COMMITS})")

    print(f"\n{'=' * 50}")
    print("  Pushing ke GitHub...")
    print("=" * 50)

    if run_git(["git", "push", "origin", "HEAD"]):
        print("\n✅ SELESAI! 50 commits berhasil di-push ke GitHub.")
    else:
        print("\n❌ Push gagal! Cek koneksi atau credential GitHub.")

    input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    main()
