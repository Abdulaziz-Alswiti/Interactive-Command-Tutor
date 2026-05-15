🐧 Interactive Command Tutor
COSC-3411 System Programming — Eta Team Project  
Based on Basic Command I & II by Instructor Ibrahim EL Didi (PMU)
---
Overview
An interactive Python CLI tool that teaches and quizzes students on Linux/Kali shell commands covered in class. Four modes let you learn at your own pace, test yourself, and get a quick reference.
Mode	What it does
Learn	Browse all commands with syntax, description, examples & tips
Quiz	Multiple-choice questions with instant feedback and scoring
Practice	Read a scenario — type the correct command
Cheatsheet	Compact one-line reference for every command
Covers 40+ commands from Basic Command I & II including: `ls`, `cd`, `find`, `grep`, `sed`, `awk`, `chmod`, `crontab`, `tar`, `systemctl`, and more.
---
Requirements
Python 3.6+
Linux / Kali Linux (runs in any terminal)
No external libraries needed (stdlib only)
---
Installation
```bash
# Clone the repository
git clone https://github.com/ITAP/COSC-3411/Eta.git
cd Eta

# Make the script executable
chmod +x tutor.py

# Run it
python3 tutor.py
# or
./tutor.py
```
---
Usage
Launch the tool:
```bash
python3 tutor.py
```
You'll see the main menu:
```
══════════════════════════════════════════════════════════════
         🐧  Interactive Command Tutor  🐧
         COSC-3411 — Basic Command I \& II
══════════════════════════════════════════════════════════════

  1. 📖  Learn Mode   — Study commands with explanations
  2. 🧠  Quiz Mode    — Multiple choice questions
  3. ⌨️   Practice     — Type the correct command for a scenario
  4. 📋  Cheatsheet   — Quick reference for all commands
  5. 📊  My Scores    — View your quiz history
  6. ❌  Exit
```
Learn Mode
Filter by Basic I, Basic II, All, or search by keyword
Navigate with `N` (next), `P` (previous), `Q` (quit)
Each command shows: syntax, full description, example, and a pro tip
Quiz Mode
Choose 5–30 questions
Multiple-choice with shuffled options
Instant explanation after each answer
Score shown at the end with a progress bar
Results saved to `\~/.command\_tutor\_scores.json`
Practice Mode
A real-world scenario is shown (e.g. "Find all .txt files larger than 5MB in /home/kali")
Type the exact command
Type `hint` for a clue, `skip` to move on
3 attempts per question
Cheatsheet
Fast one-line reference for all 40+ commands
Filter by Basic I, Basic II, or show all
---
Example Session
```
Scenario: Search for the word 'root' in /etc/passwd.

  ❯ $ grep 'root' /etc/passwd
  ✅  Correct!
```
```
Question 3 / 10
  What does 'ps aux' show?

    1. All running processes with full details
    2. Only your own processes
    3. System logs
    4. Network connections

  ❯ Your answer: 1
  ✅  Correct!
  💡 ps aux shows all processes (a=all users, u=user format, x=without terminal)
```
---
File Structure
```
Eta/
├── tutor.py          # Main script
└── README.md         # This file
```
Scores are stored locally in `\~/.command\_tutor\_scores.json`.
---
Commands Covered
Basic Command I
`whoami` · `cd` · `ls` · `pwd` · `clear` · `man` · `locate` · `whereis` · `echo` · `find` · `cat` · `touch` · `mkdir` · `cp` · `mv` · `rm` · `sudo` · `nl` · `wc` · `ps`
Basic Command II
`adduser` · `deluser` · `su` · `history` · `pipe |` · `pgrep` · `sort` · `rev` · `uniq` · `grep` · `sed` · `awk` · `cut` · `chmod` · `vim/vi` · `nano` · `crontab` · `at` · `sleep` · `apt-get` · `ifconfig` · `ping` · `systemctl` · `tar` · `mount` · `ip route` · `shutdown/reboot` · Regex patterns
---
Credits
Project: COSC-3411 System Programming, Eta Team
Instructor: Ibrahim EL Didi, PMU
Inspired by: Abdullah's project from a previous semester
Submission Deadline: Sunday, 17 May 2026 — 23:59
