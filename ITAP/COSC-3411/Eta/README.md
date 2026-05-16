# 🐧 Interactive Command Tutor

> **COSC-3411 | Eta Team | Instructor: Ibrahim EL Didi**  
> A terminal-based quiz tool that teaches and tests Linux command-line proficiency.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Tool](#running-the-tool)
- [Usage Example](#usage-example)
- [Project Structure](#project-structure)
- [Quiz Categories](#quiz-categories)
- [Score Tracking](#score-tracking)
- [Team](#team)

---

## Overview

**Interactive Command Tutor** is a command-line quiz application written in Python 3. It covers two sets of Linux commands taught in COSC-3411:

- **Basic Command I** — filesystem navigation, file operations, process management
- **Basic Command II** — user management, text processing, services, networking, and more

Each question comes with multiple-choice options, instant feedback, and an explanation so you learn from every answer — right or wrong.

---

## Features

| Feature | Description |
|---|---|
| 🎯 Multiple quiz modes | Basic I, Basic II, Full (all 70 questions), or Custom |
| 🔀 Randomized order | Questions and answer options are shuffled every session |
| 💡 Explanations | Every question shows a detailed tip after you answer |
| 📊 Score history | Persistent score tracking saved between sessions |
| 📈 Progress bar | Visual progress indicator during each quiz |
| 🎨 Color output | ANSI-colored terminal UI for readability |

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.6 or higher |
| Operating System | Linux / macOS / WSL on Windows |
| Terminal | Any terminal supporting ANSI color codes |

No external libraries are required — the tool uses only Python standard library modules (`os`, `sys`, `random`, `time`, `json`, `shutil`, `datetime`).

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/ITAP/COSC-3411/Eta.git
cd Eta
```

**2. Confirm Python 3 is installed:**

```bash
python3 --version
```

**3. Make the script executable (Linux/macOS):**

```bash
chmod +x tutor.py
```

That's it — no `pip install` needed.

---

## Configuration

The tool works out of the box with no configuration file required.

**Score storage:**  
Quiz history is automatically saved to `~/.command_tutor_scores.json` in your home directory. This file is created on first run and updated after every session.

To reset your score history, simply delete that file:

```bash
rm ~/.command_tutor_scores.json
```

---

## Running the Tool

```bash
python3 tutor.py
```

Or, if you made it executable:

```bash
./tutor.py
```

You will be presented with the main menu immediately.

---

## Usage Example

```
════════════════════════════════════════════════════════
🐧  Interactive Command Tutor — COSC-3411
════════════════════════════════════════════════════════
  Overall score: 18/25 (72%)

  Choose a quiz:

  1. Basic Command I   — Navigation, files, find, ps  (25 questions)
  2. Basic Command II  — Users, pipes, text tools, services  (45 questions)
  3. 🎲  Full Quiz     — All commands, random order  (70 questions)
  4. 🔢  Custom Quiz   — Pick how many questions
  5. 📊  My Scores
  6. ❌  Exit

  ❯ 4
```

**Selecting Custom Quiz (option 4):**

```
  Custom Quiz  (70 questions available)

  1. Basic I only
  2. Basic II only
  3. Mixed (all)

  ❯ Source (1-3): 3
  ❯ How many questions? (1-70): 10
```

**During a question:**

```
  [Basic II]   Q 3/10   ████████████░░░░░░░░░░░░░░  2/2  (100%)

  How do you search for 'error' in log.txt, case-insensitive?

    1.  grep -i 'error' log.txt
    2.  grep 'error' log.txt
    3.  grep -c 'error' log.txt
    4.  grep -v 'error' log.txt

  ❯ Your answer (1-4 or text): 1

  ✅  Correct!

  💡  grep -i = case-insensitive. -v = invert (non-matching). -n = show line numbers.
```

**End-of-quiz results:**

```
  ── RESULTS ─────────────────────────────────────────

  Custom (10q)  ████████████████████░░░░░░░░░░  8/10  (80%)

  👍  Good job! Review the ones you missed.

  Review these:
    Q: What does 'uniq' do?
    A: Removes adjacent duplicate lines
```

---

## Project Structure

```
Eta/
├── tutor.py          # Main application entry point
├── README.md         # This file
└── .command_tutor_scores.json   # Auto-generated score history (in ~/)
```

**Inside `tutor.py`, the code is organized into these sections:**

```
tutor.py
├── C                  # ANSI color constants
├── QUESTIONS          # Question bank (70 questions)
├── Score helpers      # load_scores() / save_scores()
├── UI helpers         # clr(), banner(), inp(), wait(), pbar()
├── run_quiz()         # Core quiz loop
├── show_scores()      # Score history screen
└── main()             # Menu and navigation
```

---

## Quiz Categories

### Basic Command I (25 questions)
Covers: `whoami`, `pwd`, `ls`, `cd`, `man`, `whereis`, `echo`, `find`, `cat`, `touch`, `mkdir`, `cp`, `mv`, `rm`, `sudo`, `nl`, `wc`, `ps`, `top`, filesystem concepts, `locate`, `clear`

### Basic Command II (45 questions)
Covers: `adduser`, `deluser`, `su`, `/etc/sudoers`, `history`, pipes (`|`), `pgrep`, `sort`, `uniq`, `rev`, `grep`, regex, `sed`, `awk`, `cut`, `chmod`, `vim`, `nano`, `crontab`, `sleep`, `apt-get`, `ifconfig`, `ping`, `ip route`, `systemctl`, `tar`, `mount`, `fdisk`, `ufw`, `shutdown`, Apache2

---

## Score Tracking

After every session the tool records:

- Date and time of the session
- Quiz label (Basic I, Basic II, Full, or Custom)
- Number of correct answers
- Total questions attempted
- Percentage score

The **My Scores** screen (option 5) shows your cumulative score across all sessions and a mini bar chart of your last 10 sessions.

---

## Team

**Eta Team — COSC-3411**  
King Fahd University of Petroleum and Minerals (KFUPM) | ITAP Program  
Instructor: Ibrahim EL Didi  
Submission deadline: 17 May 2026
