#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          Interactive Command Tutor — Eta Team                    ║
║          Course  : COSC-3411  Basic Command I & II               ║
║          Instructor: Ibrahim EL Didi                             ║
║          Repo    : ITAP/COSC-3411/Eta                            ║
╚══════════════════════════════════════════════════════════════════╝

Module layout
─────────────
  1.  Constants      — ANSI colors, file paths
  2.  Question Bank  — All 70 quiz questions
  3.  Score Helpers  — Persist / load JSON score history
  4.  UI Helpers     — Terminal drawing utilities
  5.  Quiz Engine    — run_quiz()  core loop
  6.  Score Screen   — show_scores()
  7.  Main Menu      — main()  entry point
"""

import os
import sys
import random
import time
import json
import shutil
from datetime import datetime


# ══════════════════════════════════════════════════════════════════
# 1.  CONSTANTS
# ══════════════════════════════════════════════════════════════════

class C:
    """ANSI escape codes for terminal colour and style."""
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


# Path where quiz history is saved between sessions
SCORE_FILE = os.path.expanduser("~/.command_tutor_scores.json")


# ══════════════════════════════════════════════════════════════════
# 2.  QUESTION BANK
# ══════════════════════════════════════════════════════════════════
# Each entry is a dict with:
#   q    – question text
#   a    – exact correct answer string
#   opts – list of 4 answer choices (correct + 3 distractors)
#   exp  – short explanation shown after answering
#   cat  – category label: "Basic I" or "Basic II"

QUESTIONS = [

    # ── Basic Command I ──────────────────────────────────────────
    {
        "q":    "Which command shows your current username?",
        "a":    "whoami",
        "opts": ["whoami", "id", "hostname", "users"],
        "exp":  "'whoami' prints the username of the currently logged-in user.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command prints the full path of your current directory?",
        "a":    "pwd",
        "opts": ["pwd", "cwd", "path", "dir"],
        "exp":  "'pwd' = Print Working Directory.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you list ALL files including hidden ones in long format?",
        "a":    "ls -la",
        "opts": ["ls -la", "ls -l", "ls -a", "dir -all"],
        "exp":  "ls -a shows hidden files (dot files). -l adds long format with permissions, size, owner.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which flag makes 'ls' show permissions, size, and owner?",
        "a":    "-l",
        "opts": ["-l", "-a", "-h", "-p"],
        "exp":  "-l = long format. Shows permissions, links, owner, size, timestamp.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you navigate to the /etc directory?",
        "a":    "cd /etc",
        "opts": ["cd /etc", "go /etc", "nav /etc", "open /etc"],
        "exp":  "'cd' = Change Directory. Use it with any absolute or relative path.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command opens the manual page for 'ls'?",
        "a":    "man ls",
        "opts": ["man ls", "help ls", "ls --manual", "info ls"],
        "exp":  "'man' opens the manual page for any command. Press 'q' to quit.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command finds the binary and man page location of a command?",
        "a":    "whereis",
        "opts": ["whereis", "locate", "which", "find"],
        "exp":  "'whereis' returns the binary path, man page, and source code location.",
        "cat":  "Basic I",
    },
    {
        "q":    "What does 'echo $PATH' do?",
        "a":    "Prints the value of the PATH variable",
        "opts": [
            "Prints the value of the PATH variable",
            "Sets the PATH variable",
            "Clears the terminal",
            "Shows running processes",
        ],
        "exp":  "echo prints text or variable values. $VAR retrieves a variable's value.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you find all .txt files larger than 5 MB in /home/kali?",
        "a":    "find /home/kali -name '*.txt' -size +5M",
        "opts": [
            "find /home/kali -name '*.txt' -size +5M",
            "locate *.txt -size +5M",
            "ls /home/kali *.txt +5M",
            "search /home/kali -txt -size 5M",
        ],
        "exp":  "find: directory first, then options. -name for filename, -size +5M = bigger than 5 MB.",
        "cat":  "Basic I",
    },
    {
        "q":    "What does 'cat > file.txt' do?",
        "a":    "Creates a new file and waits for keyboard input",
        "opts": [
            "Creates a new file and waits for keyboard input",
            "Displays file.txt",
            "Appends to file.txt",
            "Deletes file.txt",
        ],
        "exp":  "'>' is a redirect. cat > file.txt creates the file. Type content, then Ctrl+D to save.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command creates an empty file called 'notes.txt'?",
        "a":    "touch notes.txt",
        "opts": ["touch notes.txt", "create notes.txt", "new notes.txt", "mkfile notes.txt"],
        "exp":  "'touch' creates an empty file, or updates the timestamp if the file exists.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you create nested directories projects/web/css all at once?",
        "a":    "mkdir -p projects/web/css",
        "opts": [
            "mkdir -p projects/web/css",
            "mkdir projects/web/css",
            "mkdir -r projects/web/css",
            "makedir -all projects/web/css",
        ],
        "exp":  "mkdir -p creates all parent directories as needed.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you copy 'file.txt' to /tmp/?",
        "a":    "cp file.txt /tmp/",
        "opts": ["cp file.txt /tmp/", "mv file.txt /tmp/", "copy file.txt /tmp/", "put file.txt /tmp/"],
        "exp":  "'cp' copies files. 'mv' moves or renames them.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you rename 'old.txt' to 'new.txt'?",
        "a":    "mv old.txt new.txt",
        "opts": ["mv old.txt new.txt", "rename old.txt new.txt", "cp old.txt new.txt", "rn old.txt new.txt"],
        "exp":  "There is no separate 'rename' command. 'mv' handles both moving and renaming.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you remove a directory and ALL its contents?",
        "a":    "rm -r dirname/",
        "opts": ["rm -r dirname/", "rmdir dirname/", "del dirname/", "rm dirname/"],
        "exp":  "rm -r = recursive remove. Add -f to force. Warning: no trash bin — it is permanent!",
        "cat":  "Basic I",
    },
    {
        "q":    "What does 'sudo' stand for?",
        "a":    "Switch User Do",
        "opts": ["Switch User Do", "Super User Domain", "System Update Do", "Secure User Directory"],
        "exp":  "sudo = Switch User Do. By default it runs the command as root.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command displays a file with line numbers?",
        "a":    "nl",
        "opts": ["nl", "cat", "head", "tail"],
        "exp":  "'nl' = number lines. 'cat -n' also works.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you count the number of lines in /etc/passwd?",
        "a":    "wc -l /etc/passwd",
        "opts": ["wc -l /etc/passwd", "count -l /etc/passwd", "nl /etc/passwd | tail", "lines /etc/passwd"],
        "exp":  "wc = word count. Flags: -l (lines), -w (words), -c (characters).",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command shows all running processes with full details?",
        "a":    "ps aux",
        "opts": ["ps aux", "ps", "ps -f", "ps -u"],
        "exp":  "ps aux: a=all users, u=user format, x=processes without terminal. Like Task Manager.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which tool shows which process uses the most CPU/memory in real time?",
        "a":    "top",
        "opts": ["top", "ps aux", "jobs", "monitor"],
        "exp":  "'top' is an interactive real-time process viewer. Press 'q' to quit.",
        "cat":  "Basic I",
    },
    {
        "q":    "The Linux filesystem starts at which directory?",
        "a":    "/",
        "opts": ["/", "C:\\\\", "/root", "/home"],
        "exp":  "'/' is the root of the Linux filesystem — everything branches from here.",
        "cat":  "Basic I",
    },
    {
        "q":    "What does '..' refer to in a file path?",
        "a":    "The parent directory",
        "opts": ["The parent directory", "The current directory", "The home directory", "The root directory"],
        "exp":  ".. = parent directory. . = current directory. cd .. goes up one level.",
        "cat":  "Basic I",
    },
    {
        "q":    "What does 'locate' use internally to find files?",
        "a":    "A pre-built database",
        "opts": ["A pre-built database", "Real-time filesystem scan", "The /etc/files index", "RAM cache"],
        "exp":  "locate is fast because it uses a database. Run 'updatedb' to refresh it.",
        "cat":  "Basic I",
    },
    {
        "q":    "Which command clears the terminal screen?",
        "a":    "clear",
        "opts": ["clear", "cls", "reset", "wipe"],
        "exp":  "'clear' or Ctrl+L both clear the terminal.",
        "cat":  "Basic I",
    },
    {
        "q":    "How do you search for PID of processes with 'ps' for a specific user?",
        "a":    "ps -u username",
        "opts": ["ps -u username", "ps --user username", "ps -name username", "ps -p username"],
        "exp":  "ps -u filters processes for a specific user. ps -p PID shows a specific process.",
        "cat":  "Basic I",
    },

    # ── Basic Command II ─────────────────────────────────────────
    {
        "q":    "How do you create a new user called 'bob'?",
        "a":    "sudo adduser bob",
        "opts": ["sudo adduser bob", "adduser bob", "sudo useradd bob", "sudo newuser bob"],
        "exp":  "sudo adduser creates the account, home directory at /home/bob, and a matching group.",
        "cat":  "Basic II",
    },
    {
        "q":    "Where is user account information stored in Linux?",
        "a":    "/etc/passwd",
        "opts": ["/etc/passwd", "/etc/users", "/home/users.db", "/var/accounts"],
        "exp":  "/etc/passwd holds essential info about all user accounts on the system.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you delete a user called 'bob'?",
        "a":    "sudo deluser bob",
        "opts": ["sudo deluser bob", "sudo rmuser bob", "sudo userdel bob", "del user bob"],
        "exp":  "sudo deluser removes the user account. Add --remove-home to also delete /home/bob.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you switch to user 'alice' in the terminal?",
        "a":    "su alice",
        "opts": ["su alice", "switch alice", "login alice", "cd /home/alice"],
        "exp":  "'su' = Switch User. 'su -' with a dash loads the target user's full environment.",
        "cat":  "Basic II",
    },
    {
        "q":    "What file controls who can use sudo?",
        "a":    "/etc/sudoers",
        "opts": ["/etc/sudoers", "/etc/sudo.conf", "/root/sudoers", "/home/sudoers"],
        "exp":  "The /etc/sudoers file controls sudo privileges. Edit it safely with 'visudo'.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you view your command history?",
        "a":    "history",
        "opts": ["history", "log", "cmds", "past"],
        "exp":  "'history' lists previously typed commands. !N re-runs command number N.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you re-run command number 42 from history?",
        "a":    "!42",
        "opts": ["!42", "run 42", "history 42", "exec 42"],
        "exp":  "!N executes the Nth command from history.",
        "cat":  "Basic II",
    },
    {
        "q":    "What is the default limit of commands stored in history?",
        "a":    "1000",
        "opts": ["1000", "500", "100", "Unlimited"],
        "exp":  "HISTSIZE=1000 is the default. You can change it in ~/.bashrc.",
        "cat":  "Basic II",
    },
    {
        "q":    "What symbol pipes output of one command into another?",
        "a":    "|",
        "opts": ["|", ">", ">>", "&"],
        "exp":  "The pipe | sends stdout of command1 as stdin to command2.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'ps aux | grep ssh' do?",
        "a":    "Filters output to show only ssh-related processes",
        "opts": [
            "Filters output to show only ssh-related processes",
            "Kills all ssh processes",
            "Starts ssh",
            "Lists ssh config files",
        ],
        "exp":  "Piping ps aux into grep filters the output to lines matching 'ssh'.",
        "cat":  "Basic II",
    },
    {
        "q":    "Which command searches for a running process by name and returns its PID?",
        "a":    "pgrep",
        "opts": ["pgrep", "pfind", "ps -name", "pidof"],
        "exp":  "pgrep is faster than 'ps aux | grep name' when you only need the PID.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you sort 'file.txt' in reverse alphabetical order?",
        "a":    "sort -r file.txt",
        "opts": ["sort -r file.txt", "sort -reverse file.txt", "rev file.txt", "sort -z file.txt"],
        "exp":  "sort -r = reverse. -n = numeric, -u = remove duplicates, -k N = sort by column N.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'uniq' do?",
        "a":    "Removes adjacent duplicate lines",
        "opts": [
            "Removes adjacent duplicate lines",
            "Removes all duplicate lines",
            "Sorts unique lines",
            "Counts unique words",
        ],
        "exp":  "uniq removes consecutive duplicates. Always sort first to group all duplicates together.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'rev' do to each line of a file?",
        "a":    "Reverses the characters within each line",
        "opts": [
            "Reverses the characters within each line",
            "Reverses the order of lines",
            "Rotates text 180 degrees",
            "Reverses the entire file",
        ],
        "exp":  "rev reverses characters per line — 'hello' becomes 'olleh'. It does NOT reverse line order.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you search for 'error' in log.txt, case-insensitive?",
        "a":    "grep -i 'error' log.txt",
        "opts": [
            "grep -i 'error' log.txt",
            "grep 'error' log.txt",
            "grep -c 'error' log.txt",
            "grep -v 'error' log.txt",
        ],
        "exp":  "grep -i = case-insensitive. -v = invert (non-matching). -n = show line numbers.",
        "cat":  "Basic II",
    },
    {
        "q":    "In grep regex, what does '^' mean?",
        "a":    "Matches the start of a line",
        "opts": [
            "Matches the start of a line",
            "Matches the end of a line",
            "Matches any character",
            "Negates the pattern",
        ],
        "exp":  "In regex: ^ = start of line, $ = end of line.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'grep \"world$\" file.txt' match?",
        "a":    "Lines that END with 'world'",
        "opts": [
            "Lines that END with 'world'",
            "Lines that START with 'world'",
            "Lines containing 'world'",
            "Lines NOT containing 'world'",
        ],
        "exp":  "$ in regex anchors the match to the END of the line.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you grep for lines with 'cat' OR 'dog'?",
        "a":    "grep -E 'cat|dog' file.txt",
        "opts": [
            "grep -E 'cat|dog' file.txt",
            "grep 'cat|dog' file.txt",
            "grep 'cat or dog' file.txt",
            "grep -o 'cat,dog' file.txt",
        ],
        "exp":  "-E enables extended regex (ERE). The | character means OR.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'sed s/hello/hi/g' do?",
        "a":    "Replaces ALL occurrences of 'hello' with 'hi'",
        "opts": [
            "Replaces ALL occurrences of 'hello' with 'hi'",
            "Replaces only the first 'hello'",
            "Deletes lines with 'hello'",
            "Searches for 'hi'",
        ],
        "exp":  "sed: s=substitute, g=globally on all occurrences. Without 'g' only the first per line is replaced.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you use sed to edit a file in-place and create a backup?",
        "a":    "sed -i.bak 's/old/new/' file.txt",
        "opts": [
            "sed -i.bak 's/old/new/' file.txt",
            "sed -b 's/old/new/' file.txt",
            "sed --backup 's/old/new/' file.txt",
            "sed -e 's/old/new/' file.txt",
        ],
        "exp":  "sed -i.bak modifies the original file and saves a backup as file.txt.bak.",
        "cat":  "Basic II",
    },
    {
        "q":    "Which awk command prints the 1st and 3rd columns?",
        "a":    "awk '{print $1, $3}' file.txt",
        "opts": [
            "awk '{print $1, $3}' file.txt",
            "awk '{col 1,3}' file.txt",
            "awk -c 1,3 file.txt",
            "awk print(1,3) file.txt",
        ],
        "exp":  "In awk: $1=first field, $2=second, $0=whole line. Fields split by whitespace by default.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you change awk's field separator to a colon?",
        "a":    "awk -F ':' '{print $1}' file.txt",
        "opts": [
            "awk -F ':' '{print $1}' file.txt",
            "awk -d ':' '{print $1}' file.txt",
            "awk --sep ':' '{print $1}' file.txt",
            "awk -s ':' '{print $1}' file.txt",
        ],
        "exp":  "awk -F sets the Field Separator. Very useful with /etc/passwd which uses ':'.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you extract field 1 from /etc/passwd using cut (colon-delimited)?",
        "a":    "cut -d ':' -f 1 /etc/passwd",
        "opts": [
            "cut -d ':' -f 1 /etc/passwd",
            "cut -s ':' -c 1 /etc/passwd",
            "cut ':' 1 /etc/passwd",
            "cut -col 1 /etc/passwd",
        ],
        "exp":  "cut: -d sets delimiter, -f selects the field number.",
        "cat":  "Basic II",
    },
    {
        "q":    "What permissions does 'chmod 755' set?",
        "a":    "rwxr-xr-x",
        "opts": ["rwxr-xr-x", "rwxrwxrwx", "rw-rw-rw-", "rwx------"],
        "exp":  "7=rwx (owner), 5=r-x (group), 5=r-x (others). r=4, w=2, x=1.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'chmod 644 file.txt' set?",
        "a":    "rw-r--r--",
        "opts": ["rw-r--r--", "rwxr--r--", "rw-rw-rw-", "r--r--r--"],
        "exp":  "6=rw- (owner), 4=r-- (group), 4=r-- (others). Typical for regular files.",
        "cat":  "Basic II",
    },
    {
        "q":    "In 'ls -l' output, what does a leading 'd' in permissions mean?",
        "a":    "It is a directory",
        "opts": [
            "It is a directory",
            "It is a device file",
            "It is a deleted file",
            "It is a daemon",
        ],
        "exp":  "First character: d=directory, -=regular file, l=symlink, c=char device.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you enter insert mode in vim?",
        "a":    "Press i",
        "opts": ["Press i", "Press e", "Press a", "Press Ctrl+I"],
        "exp":  "In vim: 'i' enters insert mode. ESC returns to command mode. ':wq' saves and quits.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you save and quit vim?",
        "a":    ":wq",
        "opts": [":wq", ":save", ":exit", "Ctrl+S"],
        "exp":  "In vim command mode: :wq (write+quit), :q! (quit without saving), Shift+ZZ also saves.",
        "cat":  "Basic II",
    },
    {
        "q":    "In nano, which shortcut saves the file?",
        "a":    "Ctrl+O",
        "opts": ["Ctrl+O", "Ctrl+S", "Ctrl+W", "Ctrl+X"],
        "exp":  "Nano shows shortcuts at the bottom. ^ = Ctrl. Ctrl+O saves, Ctrl+X exits.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'crontab -e' open?",
        "a":    "The cron schedule file for editing",
        "opts": [
            "The cron schedule file for editing",
            "Executes all cron jobs now",
            "Lists scheduled jobs",
            "Removes all cron jobs",
        ],
        "exp":  "crontab -e opens the user's crontab. Format: MIN HOUR DAY MON DOW command.",
        "cat":  "Basic II",
    },
    {
        "q":    "What cron expression runs a script at 2:30 AM every Mon-Fri?",
        "a":    "30 2 * * 1-5 /root/script.sh",
        "opts": [
            "30 2 * * 1-5 /root/script.sh",
            "2 30 * * 1-5 /root/script.sh",
            "30 2 1-5 * * /root/script.sh",
            "* * 2 30 1-5 /root/script.sh",
        ],
        "exp":  "Cron format: MIN HOUR DAY MON DOW. 1-5 = Monday to Friday.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you pause a script for 2 minutes?",
        "a":    "sleep 2m",
        "opts": ["sleep 2m", "sleep 2", "wait 2m", "pause 120"],
        "exp":  "sleep suffixes: s=seconds (default), m=minutes, h=hours, d=days.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you install 'nmap' in Kali Linux?",
        "a":    "sudo apt-get install nmap",
        "opts": ["sudo apt-get install nmap", "sudo yum install nmap", "sudo pkg install nmap", "install nmap"],
        "exp":  "Kali/Debian uses apt-get. Always run 'apt-get update' first.",
        "cat":  "Basic II",
    },
    {
        "q":    "What is the difference between apt-get update and upgrade?",
        "a":    "update refreshes the package list; upgrade installs newer versions",
        "opts": [
            "update refreshes the package list; upgrade installs newer versions",
            "They do the same thing",
            "update installs; upgrade removes old packages",
            "upgrade refreshes; update installs",
        ],
        "exp":  "update = gets new version list from repos. upgrade = actually installs those updates.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you remove a package AND its config files?",
        "a":    "sudo apt-get purge packagename",
        "opts": [
            "sudo apt-get purge packagename",
            "sudo apt-get remove packagename",
            "sudo apt-get delete packagename",
            "sudo apt-get clean packagename",
        ],
        "exp":  "remove keeps config files. purge removes the package AND all its configuration files.",
        "cat":  "Basic II",
    },
    {
        "q":    "Which command shows your IP address in Kali?",
        "a":    "ifconfig",
        "opts": ["ifconfig", "ipaddr", "showip", "netstat -i"],
        "exp":  "ifconfig shows network interfaces and their IP/MAC addresses. Modern alternative: 'ip a'.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you test if 8.8.8.8 is reachable?",
        "a":    "ping 8.8.8.8",
        "opts": ["ping 8.8.8.8", "reach 8.8.8.8", "connect 8.8.8.8", "test 8.8.8.8"],
        "exp":  "ping sends ICMP echo requests. 'Destination Unreachable' means no connection.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does 'ip route' show?",
        "a":    "How traffic is routed to reach the internet",
        "opts": [
            "How traffic is routed to reach the internet",
            "Current IP address",
            "Open ports",
            "Active connections",
        ],
        "exp":  "'ip route' shows the routing table. The 'default' entry is your gateway to the internet.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you start the apache2 web server?",
        "a":    "sudo systemctl start apache2",
        "opts": [
            "sudo systemctl start apache2",
            "sudo service start apache2",
            "sudo apache2 --start",
            "systemctl run apache2",
        ],
        "exp":  "systemctl manages services (daemons) via systemd: start/stop/restart/status/enable.",
        "cat":  "Basic II",
    },
    {
        "q":    "Which systemctl command makes apache2 start automatically at boot?",
        "a":    "sudo systemctl enable apache2",
        "opts": [
            "sudo systemctl enable apache2",
            "sudo systemctl start apache2",
            "sudo systemctl autostart apache2",
            "sudo systemctl boot apache2",
        ],
        "exp":  "'enable' configures the service to start at boot. 'start' only starts it right now.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you create a compressed archive of ~/Documents?",
        "a":    "tar -czvf backup.tar.gz ~/Documents",
        "opts": [
            "tar -czvf backup.tar.gz ~/Documents",
            "tar -xzvf backup.tar.gz ~/Documents",
            "zip backup.tar.gz ~/Documents",
            "tar -czf ~/Documents backup.tar.gz",
        ],
        "exp":  "tar flags: c=create, z=gzip compress, v=verbose, f=filename follows.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you extract backup.tar.gz into /tmp/?",
        "a":    "tar -xzvf backup.tar.gz -C /tmp/",
        "opts": [
            "tar -xzvf backup.tar.gz -C /tmp/",
            "tar -czvf backup.tar.gz -C /tmp/",
            "unzip backup.tar.gz /tmp/",
            "tar -extract backup.tar.gz /tmp/",
        ],
        "exp":  "tar: x=extract, z=gzip, v=verbose, f=filename, -C=destination directory.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you mount /dev/sdb1 to /mnt/usb?",
        "a":    "sudo mount /dev/sdb1 /mnt/usb",
        "opts": [
            "sudo mount /dev/sdb1 /mnt/usb",
            "sudo attach /dev/sdb1 /mnt/usb",
            "mount --usb /dev/sdb1",
            "sudo link /dev/sdb1 /mnt/usb",
        ],
        "exp":  "mount attaches a device's filesystem to a directory (mount point).",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you list all available disks and partitions?",
        "a":    "fdisk -l",
        "opts": ["fdisk -l", "ls /dev/disk", "df -h", "lsblk"],
        "exp":  "fdisk -l (Fixed Disk) lists all disks and partitions. Needs sudo.",
        "cat":  "Basic II",
    },
    {
        "q":    "How do you allow TCP port 80 through the UFW firewall?",
        "a":    "sudo ufw allow 80/tcp",
        "opts": ["sudo ufw allow 80/tcp", "sudo ufw open 80", "sudo ufw permit 80/tcp", "sudo firewall allow 80"],
        "exp":  "UFW = Uncomplicated Firewall. 'ufw allow 80/tcp' opens TCP port 80 for HTTP.",
        "cat":  "Basic II",
    },
    {
        "q":    "Which command shuts down the system immediately?",
        "a":    "sudo shutdown now",
        "opts": ["sudo shutdown now", "sudo halt", "sudo poweroff -f", "sudo shutdown 0"],
        "exp":  "shutdown now = immediate. shutdown +5 = after 5 minutes. 'sudo reboot' restarts.",
        "cat":  "Basic II",
    },
    {
        "q":    "What does the '&' symbol do at the end of a command?",
        "a":    "Runs the command in the background",
        "opts": [
            "Runs the command in the background",
            "Combines two commands",
            "Redirects output",
            "Runs as root",
        ],
        "exp":  "& sends the process to the background so you can continue using the terminal.",
        "cat":  "Basic II",
    },
    {
        "q":    "What port does Apache2 listen on by default (HTTP)?",
        "a":    "80",
        "opts": ["80", "443", "8080", "22"],
        "exp":  "HTTP = port 80. HTTPS = port 443. SSH = port 22.",
        "cat":  "Basic II",
    },
    {
        "q":    "Apache2's default web directory in Linux is?",
        "a":    "/var/www/html/",
        "opts": ["/var/www/html/", "/etc/apache2/html/", "/home/www/", "/srv/http/"],
        "exp":  "Place your HTML files in /var/www/html/ to serve them with Apache2.",
        "cat":  "Basic II",
    },
]


# ══════════════════════════════════════════════════════════════════
# 3.  SCORE HELPERS
# ══════════════════════════════════════════════════════════════════

def load_scores() -> dict:
    """Load quiz history from the JSON score file.

    Returns a dict with keys:
        sessions       – list of past session records
        total_correct  – cumulative correct answers across all sessions
        total_attempts – cumulative questions attempted
    If the file is missing or corrupted, returns fresh empty stats.
    """
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass  # Fall through to return defaults
    return {"sessions": [], "total_correct": 0, "total_attempts": 0}


def save_scores(scores: dict) -> None:
    """Persist the updated scores dict to SCORE_FILE as formatted JSON."""
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except IOError:
        pass  # Non-fatal; the session still proceeds normally


# ══════════════════════════════════════════════════════════════════
# 4.  UI HELPERS
# ══════════════════════════════════════════════════════════════════

def clear_screen() -> None:
    """Clear the terminal on both POSIX (Linux/macOS) and Windows."""
    os.system("clear" if os.name == "posix" else "cls")


def terminal_width() -> int:
    """Return the current terminal width, defaulting to 80 columns."""
    return shutil.get_terminal_size((80, 24)).columns


def banner() -> None:
    """Draw the application header banner."""
    clear_screen()
    w = terminal_width()
    print(C.CYAN + C.BOLD + "═" * w + C.RESET)
    print(C.CYAN + C.BOLD + "🐧  Interactive Command Tutor — COSC-3411".center(w) + C.RESET)
    print(C.CYAN + C.BOLD + "═" * w + C.RESET)


def prompt(message: str = "") -> str:
    """Show a styled input prompt and return the stripped input.

    Returns "q" if the user presses Ctrl+C or Ctrl+D.
    """
    try:
        return input(C.GREEN + "  ❯ " + message + C.RESET).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return "q"


def wait_for_enter() -> None:
    """Pause execution until the user presses Enter."""
    input(C.DIM + "\n  Press Enter to continue..." + C.RESET)


def progress_bar(correct: int, total: int, bar_length: int = 40) -> str:
    """Build a coloured text progress bar string.

    Args:
        correct    – number of correct answers so far
        total      – total questions in this session
        bar_length – character width of the bar (default 40)

    Returns a formatted string like:  ████░░░░  7/10  (70%)
    """
    filled = int(bar_length * correct / total) if total else 0
    bar = (
        C.GREEN + "█" * filled
        + C.DIM + "░" * (bar_length - filled)
        + C.RESET
    )
    pct = int(correct / total * 100) if total else 0
    return f"{bar}  {C.BOLD}{correct}/{total}  ({pct}%){C.RESET}"


# ══════════════════════════════════════════════════════════════════
# 5.  QUIZ ENGINE
# ══════════════════════════════════════════════════════════════════

def run_quiz(pool: list, label: str = "") -> None:
    """Run an interactive multiple-choice quiz over the given question pool.

    Args:
        pool  – list of question dicts to present
        label – short name for this quiz session (e.g. "Basic I", "Full Quiz")

    Flow per question:
      1. Display question with shuffled answer choices
      2. Accept a number (1-4) or typed text answer
      3. Evaluate and show feedback + explanation
      4. After all questions, show results and update score history
    """
    correct    = 0
    wrong_list = []           # Questions the user got wrong — shown in review
    total      = len(pool)

    for i, question in enumerate(pool, 1):
        banner()

        # Category badge — cyan for Basic I, magenta for Basic II
        cat_color = C.CYAN if question["cat"] == "Basic I" else C.MAGENTA
        print(
            f"  {cat_color}[{question['cat']}]{C.RESET}"
            f"   Q {C.BOLD}{i}{C.RESET}/{total}"
            f"   {progress_bar(correct, i - 1)}"
        )
        print()
        print(f"  {C.BOLD}{question['q']}{C.RESET}\n")

        # Shuffle options so the correct answer isn't always in the same slot
        shuffled_opts = question["opts"][:]
        random.shuffle(shuffled_opts)
        for j, option in enumerate(shuffled_opts, 1):
            print(f"    {C.BOLD}{j}.{C.RESET}  {option}")
        print()

        # Accept either a number or typed text
        raw_answer = prompt("Your answer (1-4 or text): ")
        if raw_answer.isdigit() and 1 <= int(raw_answer) <= len(shuffled_opts):
            chosen = shuffled_opts[int(raw_answer) - 1]
        else:
            chosen = raw_answer

        # Evaluate
        if chosen.lower().strip() == question["a"].lower().strip():
            print(C.GREEN + C.BOLD + "\n  ✅  Correct!" + C.RESET)
            correct += 1
        else:
            print(
                C.RED + C.BOLD + "\n  ❌  Wrong!" + C.RESET
                + f"  Correct answer: {C.YELLOW}{question['a']}{C.RESET}"
            )
            wrong_list.append(question)

        # Always show the explanation
        print(C.DIM + f"\n  💡  {question['exp']}" + C.RESET)
        time.sleep(0.3)
        wait_for_enter()

    # ── Results screen ────────────────────────────────────────────
    banner()
    pct = int(correct / total * 100)
    print()
    print(f"  {C.BOLD}── RESULTS {'─' * (terminal_width() - 13)}{C.RESET}")
    print(f"\n  {label}  {progress_bar(correct, total)}\n")

    # Performance message
    if pct >= 90:
        print(C.GREEN  + "  🏆  Excellent! You have mastered these commands!" + C.RESET)
    elif pct >= 70:
        print(C.YELLOW + "  👍  Good job! Review the ones you missed." + C.RESET)
    elif pct >= 50:
        print(C.YELLOW + "  📚  Keep studying — you are getting there." + C.RESET)
    else:
        print(C.RED    + "  💪  Don't give up! Go over the commands and try again." + C.RESET)

    # Show missed questions for quick review
    if wrong_list:
        print(f"\n  {C.BOLD}Review these:{C.RESET}")
        for wq in wrong_list:
            print(f"    {C.DIM}Q:{C.RESET} {wq['q']}")
            print(f"    {C.YELLOW}A: {wq['a']}{C.RESET}\n")

    # Persist this session to disk
    scores = load_scores()
    scores["total_correct"]  += correct
    scores["total_attempts"] += total
    scores["sessions"].append({
        "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
        "label":   label,
        "correct": correct,
        "total":   total,
        "pct":     pct,
    })
    save_scores(scores)
    wait_for_enter()


# ══════════════════════════════════════════════════════════════════
# 6.  SCORE SCREEN
# ══════════════════════════════════════════════════════════════════

def show_scores() -> None:
    """Display cumulative stats and the last 10 session results."""
    banner()
    scores = load_scores()
    total_attempts = scores["total_attempts"]
    total_correct  = scores["total_correct"]
    print()

    if total_attempts == 0:
        print(C.DIM + "  No quiz history yet. Take a quiz first!\n" + C.RESET)
    else:
        print(f"  Overall: {progress_bar(total_correct, total_attempts)}")
        print(f"  Sessions played: {len(scores['sessions'])}\n")
        print(f"  {C.BOLD}Last 10 sessions:{C.RESET}\n")

        for session in scores["sessions"][-10:][::-1]:
            pct   = session["pct"]
            color = C.GREEN if pct >= 70 else C.YELLOW if pct >= 50 else C.RED
            # Mini 10-block bar using block / light-shade characters
            bar   = "█" * (pct // 10) + "░" * (10 - pct // 10)
            print(
                f"    {C.DIM}{session['date']}{C.RESET}  "
                f"{color}{bar}{C.RESET}  "
                f"{session['correct']}/{session['total']} ({pct}%)  "
                f"{C.DIM}{session.get('label', '')}{C.RESET}"
            )
    print()
    wait_for_enter()


# ══════════════════════════════════════════════════════════════════
# 7.  MAIN MENU
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    """Entry point: display the main menu and dispatch to quiz modes."""

    # Pre-split questions into category buckets for quick access
    basic1 = [q for q in QUESTIONS if q["cat"] == "Basic I"]
    basic2 = [q for q in QUESTIONS if q["cat"] == "Basic II"]

    while True:
        banner()

        # Show a quick overall score if the user has history
        scores = load_scores()
        if scores["total_attempts"] > 0:
            tc = scores["total_correct"]
            ta = scores["total_attempts"]
            print(C.DIM + f"  Overall score: {tc}/{ta} ({int(tc / ta * 100)}%)" + C.RESET)

        print()
        print(f"  {C.BOLD}Choose a quiz:{C.RESET}\n")
        print(f"  {C.BOLD}1.{C.RESET} {C.CYAN}Basic Command I{C.RESET}"
              f"   — Navigation, files, find, ps  ({len(basic1)} questions)")
        print(f"  {C.BOLD}2.{C.RESET} {C.MAGENTA}Basic Command II{C.RESET}"
              f"  — Users, pipes, text tools, services  ({len(basic2)} questions)")
        print(f"  {C.BOLD}3.{C.RESET} 🎲  Full Quiz"
              f"         — All commands, random order  ({len(QUESTIONS)} questions)")
        print(f"  {C.BOLD}4.{C.RESET} 🔢  Custom Quiz       — Pick how many questions")
        print(f"  {C.BOLD}5.{C.RESET} 📊  My Scores")
        print(f"  {C.BOLD}6.{C.RESET} ❌  Exit\n")

        choice = prompt("Select: ")

        if choice == "1":
            run_quiz(random.sample(basic1, len(basic1)), label="Basic I")

        elif choice == "2":
            run_quiz(random.sample(basic2, len(basic2)), label="Basic II")

        elif choice == "3":
            run_quiz(random.sample(QUESTIONS, len(QUESTIONS)), label="Full Quiz")

        elif choice == "4":
            # Let the user narrow the source and pick a question count
            banner()
            print(f"\n  {C.BOLD}Custom Quiz{C.RESET}  ({len(QUESTIONS)} questions available)\n")
            print(f"  {C.BOLD}1.{C.RESET} Basic I only")
            print(f"  {C.BOLD}2.{C.RESET} Basic II only")
            print(f"  {C.BOLD}3.{C.RESET} Mixed (all)\n")

            source_map = {"1": basic1, "2": basic2}
            source = source_map.get(prompt("Source (1-3): "), QUESTIONS)

            n_str = prompt(f"How many questions? (1-{len(source)}): ")
            try:
                n = max(1, min(len(source), int(n_str)))
            except ValueError:
                n = min(10, len(source))      # Sensible fallback

            run_quiz(random.sample(source, n), label=f"Custom ({n}q)")

        elif choice == "5":
            show_scores()

        elif choice in ("6", "q", "exit", "quit"):
            banner()
            print(C.GREEN + C.BOLD + "\n  Good luck! 🐧\n" + C.RESET)
            sys.exit(0)


# ── Script entry point ────────────────────────────────────────────
if __name__ == "__main__":
    main()
