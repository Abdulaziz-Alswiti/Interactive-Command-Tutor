#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          Interactive Command Tutor — Eta Team                    ║
║          Based on: Basic Command I & II (COSC-3411)              ║
║          Instructor: Ibrahim EL Didi                             ║
╚══════════════════════════════════════════════════════════════════╝

Modes:
  1. Learn Mode  — Study commands with explanations & examples
  2. Quiz Mode   — Answer questions and get scored
  3. Practice    — Type the correct command for a scenario
  4. Cheatsheet  — Quick reference for all commands
"""

import os
import sys
import random
import time
import json
import subprocess
import shutil
from datetime import datetime

# ─── ANSI Colors ────────────────────────────────────────────────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"
    BG_BLUE  = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"
    MAGENTA  = "\033[95m"

# ─── COMMAND DATABASE ────────────────────────────────────────────────────────
# Each entry: name, syntax, description, example, category, tip
COMMANDS = [
    # ── Basic I: Navigation & Files ──────────────────────────────────────────
    {
        "name": "whoami",
        "syntax": "whoami",
        "description": "Displays the username of the currently logged-in user. The superuser is called 'root'.",
        "example": "$ whoami\nkali",
        "category": "Basic I",
        "tip": "Useful to confirm whether you are root or a regular user.",
        "keywords": ["user", "login", "who", "identity"]
    },
    {
        "name": "cd",
        "syntax": "cd [directory]",
        "description": "Change the current working directory. Use 'cd ..' to go up one level, 'cd /' to go to root, 'cd ~' or just 'cd' for home.",
        "example": "$ cd /etc\n$ cd ..\n$ cd ~",
        "category": "Basic I",
        "tip": "Use Tab to auto-complete directory names.",
        "keywords": ["change", "directory", "navigate", "move"]
    },
    {
        "name": "ls",
        "syntax": "ls [options] [directory]",
        "description": "Lists files and directories. Common flags: -l (long format), -a (show hidden files), -la (both).",
        "example": "$ ls\n$ ls -l\n$ ls -la\n$ ls /etc",
        "category": "Basic I",
        "tip": "Hidden files start with a dot (.). Use -a to see them.",
        "keywords": ["list", "files", "directory", "contents"]
    },
    {
        "name": "pwd",
        "syntax": "pwd",
        "description": "Print Working Directory — shows the full path of the directory you are currently in.",
        "example": "$ pwd\n/home/kali",
        "category": "Basic I",
        "tip": "Always check pwd when you are unsure of your location in the filesystem.",
        "keywords": ["path", "current", "directory", "where"]
    },
    {
        "name": "clear",
        "syntax": "clear",
        "description": "Clears the terminal screen. You can also use Ctrl+L.",
        "example": "$ clear",
        "category": "Basic I",
        "tip": "Ctrl+L is faster than typing clear.",
        "keywords": ["clear", "screen", "terminal"]
    },
    {
        "name": "man",
        "syntax": "man [command]",
        "description": "Opens the manual page for any command. Press 'q' to quit the manual.",
        "example": "$ man ls\n$ man find",
        "category": "Basic I",
        "tip": "Use '/keyword' inside man to search, then 'n' for next match.",
        "keywords": ["manual", "help", "documentation"]
    },
    {
        "name": "locate",
        "syntax": "locate [filename]",
        "description": "Searches the entire filesystem for a file by name. Uses a pre-built database — run 'updatedb' to refresh it.",
        "example": "$ locate apache2\n$ locate passwd",
        "category": "Basic I",
        "tip": "locate is fast but the database may be outdated. Use 'find' for real-time search.",
        "keywords": ["search", "file", "locate", "find"]
    },
    {
        "name": "whereis",
        "syntax": "whereis [command]",
        "description": "Finds the binary, source, and manual page files for a command.",
        "example": "$ whereis python3\npython3: /usr/bin/python3 /usr/share/man/man1/python3.1.gz",
        "category": "Basic I",
        "tip": "Great for confirming where an installed tool lives.",
        "keywords": ["binary", "path", "command", "location"]
    },
    {
        "name": "echo",
        "syntax": "echo [string or $VARIABLE]",
        "description": "Prints text or variable values to the terminal. Like print() in Python.",
        "example": "$ echo Hello Kali\n$ echo $PATH\n$ echo $HOME",
        "category": "Basic I",
        "tip": "Use echo to debug shell scripts by printing variable values.",
        "keywords": ["print", "output", "variable", "text"]
    },
    {
        "name": "find",
        "syntax": "find [directory] [options] [expression]",
        "description": "Powerful search utility. Can search by name, type, size, modification time, and more.",
        "example": "$ find / -type f -name apache2\n$ find /home/kali -name '*.txt' -size +5M\n$ find / -mtime -1",
        "category": "Basic I",
        "tip": "Use -exec to run a command on each found file: find / -name '*.log' -exec rm {} \\;",
        "keywords": ["search", "file", "find", "size", "name"]
    },
    {
        "name": "cat",
        "syntax": "cat [file] or cat > [file]",
        "description": "Displays file contents. Also used to create files with 'cat > filename' (Ctrl+D to save).",
        "example": "$ cat /etc/passwd\n$ cat > newfile.txt\nHello World\n^D",
        "category": "Basic I",
        "tip": "cat stands for concatenate. Use it to combine files: cat file1 file2 > combined.txt",
        "keywords": ["display", "file", "read", "create", "concatenate"]
    },
    {
        "name": "touch",
        "syntax": "touch [filename]",
        "description": "Creates an empty file or updates the timestamp of an existing file.",
        "example": "$ touch notes.txt\n$ touch report.py",
        "category": "Basic I",
        "tip": "Useful for quickly creating placeholder files in scripts.",
        "keywords": ["create", "file", "empty", "timestamp"]
    },
    {
        "name": "mkdir",
        "syntax": "mkdir [directory] or mkdir -p [nested/path]",
        "description": "Makes a new directory. Use -p to create nested directories at once.",
        "example": "$ mkdir myfolder\n$ mkdir -p projects/web/html",
        "category": "Basic I",
        "tip": "mkdir -p will not error if the directory already exists.",
        "keywords": ["create", "directory", "folder", "make"]
    },
    {
        "name": "cp",
        "syntax": "cp [source] [destination]",
        "description": "Copies files or directories. Use -r to copy directories recursively.",
        "example": "$ cp file.txt /tmp/\n$ cp -r mydir/ /backup/",
        "category": "Basic I",
        "tip": "With find: find / -name '*.conf' -exec cp {} /Desktop \\;",
        "keywords": ["copy", "file", "duplicate"]
    },
    {
        "name": "mv",
        "syntax": "mv [source] [destination]",
        "description": "Moves or renames files and directories.",
        "example": "$ mv oldname.txt newname.txt\n$ mv file.txt /home/kali/",
        "category": "Basic I",
        "tip": "mv is also how you rename files in Linux — there is no separate rename command.",
        "keywords": ["move", "rename", "file"]
    },
    {
        "name": "rm",
        "syntax": "rm [file] or rm -r [directory]",
        "description": "Removes files or directories. -r for recursive (directories), -f to force without prompts.",
        "example": "$ rm oldfile.txt\n$ rm -r mydir/\n$ rm -rf /tmp/junk/",
        "category": "Basic I",
        "tip": "WARNING: There is no trash bin. Deleted files are gone permanently.",
        "keywords": ["delete", "remove", "file", "directory"]
    },
    {
        "name": "sudo",
        "syntax": "sudo [command]",
        "description": "Executes a command with root (superuser) privileges. Stands for 'Switch User Do'.",
        "example": "$ sudo apt update\n$ sudo -u root whoami",
        "category": "Basic I",
        "tip": "sudo -i gives you a full root shell session.",
        "keywords": ["root", "superuser", "admin", "privilege"]
    },
    {
        "name": "nl",
        "syntax": "nl [file]",
        "description": "Displays file contents with line numbers. Like cat but numbered.",
        "example": "$ nl /etc/passwd",
        "category": "Basic I",
        "tip": "Also try 'cat -n file' for a similar effect.",
        "keywords": ["line", "number", "file", "display"]
    },
    {
        "name": "wc",
        "syntax": "wc [options] [file]",
        "description": "Counts lines (-l), words (-w), and characters (-c) in a file.",
        "example": "$ wc /etc/passwd\n$ wc -l /etc/passwd\n$ wc -w notes.txt",
        "category": "Basic I",
        "tip": "wc -l is great for counting results: ls | wc -l",
        "keywords": ["count", "lines", "words", "characters"]
    },
    {
        "name": "ps",
        "syntax": "ps [options]",
        "description": "Shows running processes. Common flags: ps (current shell), ps -e or ps -A (all), ps aux (detailed all), ps -u [user], ps -p [PID].",
        "example": "$ ps\n$ ps aux\n$ ps -u kali\n$ ps -p 1234",
        "category": "Basic I",
        "tip": "top is an interactive real-time view of processes using most resources.",
        "keywords": ["process", "running", "PID", "status"]
    },
    # ── Basic II: User, Pipes, Text Processing ────────────────────────────────
    {
        "name": "adduser",
        "syntax": "sudo adduser [username]",
        "description": "Creates a new user account, home directory, and matching group.",
        "example": "$ sudo adduser bob",
        "category": "Basic II",
        "tip": "New home directory is created at /home/username. User info is in /etc/passwd.",
        "keywords": ["user", "create", "account", "add"]
    },
    {
        "name": "deluser",
        "syntax": "sudo deluser [username]",
        "description": "Deletes a user account from the system.",
        "example": "$ sudo deluser bob",
        "category": "Basic II",
        "tip": "Use --remove-home to also delete the user's home directory.",
        "keywords": ["user", "delete", "remove", "account"]
    },
    {
        "name": "su",
        "syntax": "su [username]",
        "description": "Switch User — changes to another user's session. 'su' alone or 'su root' switches to root.",
        "example": "$ su bob\n$ su root\n$ su -   # full root login shell",
        "category": "Basic II",
        "tip": "su - (with dash) loads the target user's full environment, including PATH.",
        "keywords": ["switch", "user", "login", "su"]
    },
    {
        "name": "history",
        "syntax": "history [n]",
        "description": "Shows the list of previously typed commands. Use !N to re-run command number N.",
        "example": "$ history\n$ history 20\n$ !100",
        "category": "Basic II",
        "tip": "The history limit is set by the HISTSIZE variable (default 1000). Press Up/Down arrows to scroll.",
        "keywords": ["history", "commands", "previous", "repeat"]
    },
    {
        "name": "pipe |",
        "syntax": "command1 | command2",
        "description": "Pipes send the output of one command as input to another. You can chain multiple pipes.",
        "example": "$ ls -la | grep '.txt'\n$ cat /etc/passwd | grep kali\n$ ps aux | grep ssh | wc -l",
        "category": "Basic II",
        "tip": "Pipes are one of the most powerful features of Linux. Master them!",
        "keywords": ["pipe", "redirect", "chain", "output", "input"]
    },
    {
        "name": "pgrep",
        "syntax": "pgrep [process_name]",
        "description": "Searches for a running process by name and returns its PID.",
        "example": "$ pgrep ssh\n$ pgrep apache2",
        "category": "Basic II",
        "tip": "Faster than 'ps aux | grep name' for just getting the PID.",
        "keywords": ["process", "search", "PID", "running"]
    },
    {
        "name": "sort",
        "syntax": "sort [options] [file]",
        "description": "Sorts lines of text. Flags: -r (reverse), -n (numeric), -u (remove duplicates), -k N (sort by column N).",
        "example": "$ sort file.txt\n$ sort -r file.txt\n$ sort -n numbers.txt\n$ sort -u file.txt\n$ sort -k 2 file.txt",
        "category": "Basic II",
        "tip": "Combine with uniq to remove duplicates: sort file.txt | uniq",
        "keywords": ["sort", "order", "alphabetical", "reverse", "numeric"]
    },
    {
        "name": "rev",
        "syntax": "rev [file]",
        "description": "Reverses the characters in each line (not the order of lines).",
        "example": "$ echo 'hello' | rev\nolleh",
        "category": "Basic II",
        "tip": "rev reverses characters per line, not the file itself.",
        "keywords": ["reverse", "characters", "line"]
    },
    {
        "name": "uniq",
        "syntax": "uniq [file]",
        "description": "Removes adjacent duplicate lines. Usually used after sort to remove all duplicates.",
        "example": "$ sort file.txt | uniq\n$ sort file.txt | uniq -c  # count occurrences",
        "category": "Basic II",
        "tip": "uniq only removes consecutive duplicates, so always sort first.",
        "keywords": ["unique", "duplicates", "remove", "filter"]
    },
    {
        "name": "grep",
        "syntax": "grep [pattern] [file]",
        "description": "Searches for lines matching a pattern. Supports regex. Flags: -i (ignore case), -r (recursive), -v (invert match), -n (line numbers).",
        "example": "$ grep 'hello' file.txt\n$ grep -i 'error' log.txt\n$ grep -r 'root' /etc/\n$ grep '^Hello' file.txt",
        "category": "Basic II",
        "tip": "Combine with pipes: ps aux | grep apache2",
        "keywords": ["search", "pattern", "filter", "text", "regex"]
    },
    {
        "name": "sed",
        "syntax": "sed 's/old/new/g' [file]",
        "description": "Stream Editor. Finds and replaces text. 's' = substitute, 'g' = global (all occurrences). Use -i to edit file in place.",
        "example": "$ sed 's/Hello/Hi/g' file.txt\n$ sed 's/bob/ibrahim/' old.txt > new.txt\n$ sed -i.bak 's/bob/ibrahim/' file.txt",
        "category": "Basic II",
        "tip": "sed -i.bak creates a backup before editing. Always good practice!",
        "keywords": ["replace", "substitute", "text", "edit", "stream"]
    },
    {
        "name": "awk",
        "syntax": "awk '{print $N}' [file]",
        "description": "A text processing language. $1 = first field, $2 = second, etc. NR = line number. -F sets field separator.",
        "example": "$ awk '{print $1, $3}' data.txt\n$ awk -F ':' '{print $1}' /etc/passwd\n$ awk 'NR==3' file.txt",
        "category": "Basic II",
        "tip": "awk -F ':' changes the field delimiter (default is space/tab).",
        "keywords": ["field", "column", "text", "extract", "process"]
    },
    {
        "name": "cut",
        "syntax": "cut -d [delimiter] -f [field] [file]",
        "description": "Extracts specific fields/columns from text. -d sets delimiter, -f selects the field number.",
        "example": "$ cut -d ':' -f 1 /etc/passwd\n$ cut -d ',' -f 2 data.csv",
        "category": "Basic II",
        "tip": "cut is simpler than awk for basic column extraction.",
        "keywords": ["cut", "field", "column", "extract", "delimiter"]
    },
    {
        "name": "chmod",
        "syntax": "chmod [permissions] [file]",
        "description": "Changes file permissions. Uses octal notation: 4=read, 2=write, 1=execute. Combine for each group: owner, group, others.",
        "example": "$ chmod 755 script.sh   # rwxr-xr-x\n$ chmod 644 file.txt   # rw-r--r--\n$ chmod +x script.sh",
        "category": "Basic II",
        "tip": "7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---. chmod 777 = everyone can do everything.",
        "keywords": ["permissions", "chmod", "read", "write", "execute"]
    },
    {
        "name": "vim / vi",
        "syntax": "vim [file] or vi [file]",
        "description": "Powerful text editor. Press 'i' to enter insert mode. Press ESC then ':wq' to save and quit. ':q!' to quit without saving.",
        "example": "$ vim notes.txt\n# Press i → type → ESC → :wq",
        "category": "Basic II",
        "tip": "In command mode: 'dd' deletes a line, 'yy' copies, 'p' pastes, ':wq' saves and exits.",
        "keywords": ["editor", "vim", "vi", "text", "edit"]
    },
    {
        "name": "nano",
        "syntax": "nano [file]",
        "description": "Beginner-friendly text editor. Shows keyboard shortcuts at the bottom. Ctrl+O saves, Ctrl+X exits.",
        "example": "$ nano notes.txt\n# Ctrl+O to save, Ctrl+X to exit",
        "category": "Basic II",
        "tip": "The ^ symbol in nano means Ctrl. Ctrl+Shift+V to paste.",
        "keywords": ["editor", "nano", "text", "beginner", "edit"]
    },
    {
        "name": "crontab",
        "syntax": "crontab -e",
        "description": "Schedules recurring tasks. Format: 'MIN HOUR DAY MON DOW command'. Use * for any.",
        "example": "$ crontab -e\n30 2 * * 1-5 /root/scan.sh  # 2:30AM Mon-Fri",
        "category": "Basic II",
        "tip": "cron.daily, cron.hourly, cron.weekly directories also exist in /etc/.",
        "keywords": ["schedule", "cron", "task", "automate", "time"]
    },
    {
        "name": "at",
        "syntax": "at [time]",
        "description": "Schedules a one-time task. Enter commands at the at> prompt, then Ctrl+D to save.",
        "example": "$ at 2:30 PM\nat> /root/scan.sh\nat> ^D",
        "category": "Basic II",
        "tip": "Use 'atq' to list scheduled at jobs and 'atrm N' to remove one.",
        "keywords": ["schedule", "one-time", "at", "task", "time"]
    },
    {
        "name": "sleep",
        "syntax": "sleep N[s|m|h|d]",
        "description": "Pauses script execution for a given time. Suffixes: s=seconds, m=minutes, h=hours, d=days.",
        "example": "$ sleep 5\n$ sleep 2m\n$ sleep 1h",
        "category": "Basic II",
        "tip": "Use with && to delay commands: sleep 5 && sudo poweroff",
        "keywords": ["sleep", "wait", "pause", "delay", "time"]
    },
    {
        "name": "apt-get",
        "syntax": "sudo apt-get [install|remove|purge|update|upgrade] [package]",
        "description": "Package manager for Debian-based systems (Kali, Ubuntu). install adds, remove uninstalls, purge removes with config files, update refreshes repo lists, upgrade installs updates.",
        "example": "$ sudo apt-get update\n$ sudo apt-get install gedit\n$ sudo apt-get remove gedit\n$ sudo apt-get purge gedit",
        "category": "Basic II",
        "tip": "Always run 'apt-get update' before installing to get the latest package list.",
        "keywords": ["package", "install", "remove", "apt", "software"]
    },
    {
        "name": "ifconfig",
        "syntax": "ifconfig",
        "description": "Displays network interface information including IP address, MAC address, and more.",
        "example": "$ ifconfig\n$ ifconfig eth0",
        "category": "Basic II",
        "tip": "Modern alternative: 'ip addr show' or 'ip a'",
        "keywords": ["network", "IP", "interface", "address", "ifconfig"]
    },
    {
        "name": "ping",
        "syntax": "ping [host or IP]",
        "description": "Tests network connectivity to a host. Sends ICMP echo requests.",
        "example": "$ ping 8.8.8.8\n$ ping google.com\n$ ping -c 4 192.168.1.1",
        "category": "Basic II",
        "tip": "Use Ctrl+C to stop. -c N sends only N packets.",
        "keywords": ["ping", "network", "connectivity", "reachable", "ICMP"]
    },
    {
        "name": "systemctl",
        "syntax": "sudo systemctl [start|stop|restart|status|enable] [service]",
        "description": "Controls system services (daemons). start/stop toggles a service, enable makes it start at boot.",
        "example": "$ sudo systemctl start apache2\n$ sudo systemctl status postgresql\n$ sudo systemctl enable apache2",
        "category": "Basic II",
        "tip": "systemd is the init system. Services are also called daemons.",
        "keywords": ["service", "daemon", "start", "stop", "systemd"]
    },
    {
        "name": "tar",
        "syntax": "tar [options] [archive.tar.gz] [files]",
        "description": "Creates or extracts compressed archives. -czvf = create, -xzvf = extract.",
        "example": "$ tar -czvf backup.tar.gz ~/Documents\n$ tar -xzvf backup.tar.gz -C /tmp/",
        "category": "Basic II",
        "tip": "Remember: c=create, x=extract, z=gzip, v=verbose, f=filename.",
        "keywords": ["archive", "compress", "tar", "backup", "extract"]
    },
    {
        "name": "mount",
        "syntax": "sudo mount [device] [mount_point]",
        "description": "Attaches a storage device (USB, disk) to the filesystem. Use 'umount' to detach.",
        "example": "$ sudo mount /dev/sdb1 /mnt/usb\n$ sudo umount /dev/sdb1",
        "category": "Basic II",
        "tip": "Use 'fdisk -l' to list available disks and partitions before mounting.",
        "keywords": ["mount", "USB", "disk", "filesystem", "storage"]
    },
    {
        "name": "chmod regex",
        "syntax": "grep with Regex patterns",
        "description": "Regex in grep: ^ = start of line, $ = end of line, * = zero or more, | = OR, [] = character class, () = grouping.",
        "example": "$ grep '^Hello' file.txt\n$ grep 'world$' file.txt\n$ grep -E 'cat|dog' file.txt\n$ grep -E '[^ap]' file.txt",
        "category": "Basic II",
        "tip": "Use -E for extended regex (ERE) to enable |, +, ?, ().",
        "keywords": ["regex", "pattern", "grep", "search", "regular expression"]
    },
    {
        "name": "ip route",
        "syntax": "ip route",
        "description": "Shows the routing table — how your machine decides where to send network traffic.",
        "example": "$ ip route\ndefault via 192.168.1.1 dev eth0",
        "category": "Basic II",
        "tip": "The 'default' route is your gateway to the internet.",
        "keywords": ["routing", "network", "gateway", "ip route"]
    },
    {
        "name": "shutdown / reboot",
        "syntax": "sudo shutdown [now|+N] or sudo reboot",
        "description": "Shuts down or reboots the system. 'shutdown now' = immediate, 'shutdown +5' = after 5 mins.",
        "example": "$ sudo shutdown now\n$ sudo shutdown +5\n$ sudo reboot\n$ sudo poweroff",
        "category": "Basic II",
        "tip": "You can schedule shutdowns and combine with sleep: sleep 5 && sudo poweroff",
        "keywords": ["shutdown", "reboot", "poweroff", "restart"]
    },
]

# ─── QUIZ QUESTIONS ──────────────────────────────────────────────────────────
QUIZ_QUESTIONS = [
    {
        "question": "Which command shows your current username?",
        "answer": "whoami",
        "options": ["whoami", "id", "hostname", "users"],
        "explanation": "'whoami' prints the username of the currently logged-in user."
    },
    {
        "question": "How do you list ALL files including hidden ones?",
        "answer": "ls -la",
        "options": ["ls -la", "ls -l", "dir -a", "ls --all"],
        "explanation": "ls -a shows hidden files (starting with dot). -l adds long format."
    },
    {
        "question": "Which command prints the current directory path?",
        "answer": "pwd",
        "options": ["pwd", "cwd", "dir", "path"],
        "explanation": "'pwd' = Print Working Directory."
    },
    {
        "question": "How do you search for the word 'root' in /etc/passwd?",
        "answer": "grep 'root' /etc/passwd",
        "options": ["grep 'root' /etc/passwd", "find 'root' /etc/passwd", "locate root /etc/passwd", "sed 'root' /etc/passwd"],
        "explanation": "grep searches for text patterns in files."
    },
    {
        "question": "Which flag makes ls show file permissions, size, and owner?",
        "answer": "-l",
        "options": ["-l", "-a", "-h", "-p"],
        "explanation": "-l stands for 'long format', showing detailed file info."
    },
    {
        "question": "What does 'sudo' stand for?",
        "answer": "Switch User Do",
        "options": ["Switch User Do", "Super User Domain", "System Update Do", "Secure User Directory"],
        "explanation": "sudo = Switch User Do. It runs commands with root privileges."
    },
    {
        "question": "How do you find a file named 'apache2' in the entire filesystem?",
        "answer": "find / -type f -name apache2",
        "options": ["find / -type f -name apache2", "locate -f apache2 /", "search / apache2", "whereis -f apache2 /"],
        "explanation": "find starts from /, -type f means files only, -name specifies the filename."
    },
    {
        "question": "Which command opens the manual page for 'ls'?",
        "answer": "man ls",
        "options": ["man ls", "help ls", "ls --manual", "info ls"],
        "explanation": "'man' opens the manual (man page) for any command."
    },
    {
        "question": "What does 'cat > file.txt' do?",
        "answer": "Creates a new file and waits for input",
        "options": ["Creates a new file and waits for input", "Displays file.txt contents", "Appends to file.txt", "Deletes file.txt"],
        "explanation": "'>' is a redirect. cat > file.txt creates the file and takes keyboard input until Ctrl+D."
    },
    {
        "question": "How do you create nested directories like a/b/c at once?",
        "answer": "mkdir -p a/b/c",
        "options": ["mkdir -p a/b/c", "mkdir a/b/c", "mkdir -r a/b/c", "makedir a b c"],
        "explanation": "mkdir -p creates parent directories as needed."
    },
    {
        "question": "Which command counts the number of lines in a file?",
        "answer": "wc -l",
        "options": ["wc -l", "count -l", "nl", "wc -c"],
        "explanation": "wc = word count. -l counts lines, -w counts words, -c counts characters."
    },
    {
        "question": "What does 'ps aux' show?",
        "answer": "All running processes with full details",
        "options": ["All running processes with full details", "Only your own processes", "System logs", "Network connections"],
        "explanation": "ps aux shows all processes (a=all users, u=user format, x=without terminal)."
    },
    {
        "question": "How do you add a new user called 'alice'?",
        "answer": "sudo adduser alice",
        "options": ["sudo adduser alice", "adduser alice", "sudo useradd alice", "sudo newuser alice"],
        "explanation": "sudo adduser creates the account, home directory, and group."
    },
    {
        "question": "What symbol is used for piping in Linux?",
        "answer": "|",
        "options": ["|", ">", ">>", "&"],
        "explanation": "The pipe | sends output of one command as input to the next."
    },
    {
        "question": "How do you sort a file in reverse order?",
        "answer": "sort -r file.txt",
        "options": ["sort -r file.txt", "sort -reverse file.txt", "rev file.txt", "sort -d file.txt"],
        "explanation": "sort -r reverses the sort order. -n for numeric sort."
    },
    {
        "question": "What does 'sed s/old/new/g' do?",
        "answer": "Replaces all occurrences of 'old' with 'new'",
        "options": ["Replaces all occurrences of 'old' with 'new'", "Deletes lines containing 'old'", "Shows lines with 'new'", "Searches for 'old' only"],
        "explanation": "sed s/old/new/g: s=substitute, g=globally on all occurrences."
    },
    {
        "question": "Which awk command prints only the first column of a file?",
        "answer": "awk '{print $1}' file.txt",
        "options": ["awk '{print $1}' file.txt", "awk '{print col1}' file.txt", "awk -c 1 file.txt", "cut file.txt $1"],
        "explanation": "In awk, $1 is the first field, $2 second, etc. $0 is the whole line."
    },
    {
        "question": "What permissions does 'chmod 755' set?",
        "answer": "rwxr-xr-x",
        "options": ["rwxr-xr-x", "rwxrwxrwx", "rw-rw-rw-", "rwx------"],
        "explanation": "7=rwx (owner), 5=r-x (group), 5=r-x (others). 4=r, 2=w, 1=x."
    },
    {
        "question": "How do you install a package called 'nmap' in Kali?",
        "answer": "sudo apt-get install nmap",
        "options": ["sudo apt-get install nmap", "install nmap", "sudo yum install nmap", "sudo pkg install nmap"],
        "explanation": "Kali/Debian uses apt-get. Always run apt-get update first."
    },
    {
        "question": "Which command tests if 8.8.8.8 is reachable?",
        "answer": "ping 8.8.8.8",
        "options": ["ping 8.8.8.8", "reach 8.8.8.8", "connect 8.8.8.8", "test 8.8.8.8"],
        "explanation": "ping sends ICMP echo requests to test connectivity."
    },
    {
        "question": "How do you start the apache2 service?",
        "answer": "sudo systemctl start apache2",
        "options": ["sudo systemctl start apache2", "sudo service start apache2", "sudo apache2 start", "systemctl apache2 run"],
        "explanation": "systemctl manages services (daemons) using systemd."
    },
    {
        "question": "What does 'crontab -e' do?",
        "answer": "Opens the cron schedule file for editing",
        "options": ["Opens the cron schedule file for editing", "Executes all cron jobs now", "Lists cron jobs", "Removes all cron jobs"],
        "explanation": "crontab -e opens the user's crontab for scheduling recurring tasks."
    },
    {
        "question": "How do you switch to user 'bob'?",
        "answer": "su bob",
        "options": ["su bob", "switch bob", "login bob", "cd /home/bob"],
        "explanation": "su = switch user. su bob switches to bob's session."
    },
    {
        "question": "What does grep '^Hello' do?",
        "answer": "Matches lines that START with 'Hello'",
        "options": ["Matches lines that START with 'Hello'", "Matches lines that end with 'Hello'", "Matches 'Hello' anywhere", "Ignores lines with 'Hello'"],
        "explanation": "In regex, ^ anchors the match to the START of a line."
    },
    {
        "question": "How do you create a compressed archive of a folder?",
        "answer": "tar -czvf archive.tar.gz folder/",
        "options": ["tar -czvf archive.tar.gz folder/", "zip archive.zip folder/", "tar -xzvf folder/ archive.tar.gz", "compress folder/ > archive.tar.gz"],
        "explanation": "tar: c=create, z=gzip compression, v=verbose, f=filename follows."
    },
    {
        "question": "How do you view command history and re-run command number 50?",
        "answer": "history → then !50",
        "options": ["history → then !50", "history 50", "show 50", "run 50"],
        "explanation": "history shows past commands. !N re-runs command number N."
    },
    {
        "question": "Which command finds the binary location of 'python3'?",
        "answer": "whereis python3",
        "options": ["whereis python3", "locate python3", "find python3", "which python3"],
        "explanation": "whereis returns binary, man page, and source locations."
    },
    {
        "question": "What does 'sleep 2m' do?",
        "answer": "Pauses for 2 minutes",
        "options": ["Pauses for 2 minutes", "Pauses for 2 seconds", "Runs a task every 2 minutes", "Schedules a 2-minute shutdown"],
        "explanation": "sleep N[suffix]. s=seconds, m=minutes, h=hours, d=days."
    },
    {
        "question": "How do you remove a directory and all its contents?",
        "answer": "rm -r dirname/",
        "options": ["rm -r dirname/", "rmdir dirname/", "delete dirname/", "rm dirname/"],
        "explanation": "rm -r = recursive remove. Add -f to force without prompts."
    },
    {
        "question": "Which command shows your IP address in Kali?",
        "answer": "ifconfig",
        "options": ["ifconfig", "ipaddr", "showip", "netstat"],
        "explanation": "ifconfig shows network interface info including your IP address."
    },
]

# ─── SCENARIO PRACTICE ───────────────────────────────────────────────────────
SCENARIOS = [
    {
        "scenario": "You need to see what user you are logged in as.",
        "correct": "whoami",
        "accept": ["whoami"],
        "hint": "This command prints only your username."
    },
    {
        "scenario": "Navigate to the /etc directory.",
        "correct": "cd /etc",
        "accept": ["cd /etc"],
        "hint": "Use the 'change directory' command followed by the path."
    },
    {
        "scenario": "Show all files (including hidden) in long format in the current directory.",
        "correct": "ls -la",
        "accept": ["ls -la", "ls -al", "ls -l -a", "ls -a -l"],
        "hint": "Combine the long format and show-all flags with ls."
    },
    {
        "scenario": "Find all .txt files larger than 5MB in /home/kali.",
        "correct": "find /home/kali -name '*.txt' -size +5M",
        "accept": ["find /home/kali -name '*.txt' -size +5M", "find /home/kali -name \"*.txt\" -size +5M"],
        "hint": "Use find with -name and -size flags."
    },
    {
        "scenario": "Search for the word 'kali' in /etc/passwd.",
        "correct": "grep 'kali' /etc/passwd",
        "accept": ["grep 'kali' /etc/passwd", 'grep "kali" /etc/passwd', "grep kali /etc/passwd"],
        "hint": "grep searches for patterns inside files."
    },
    {
        "scenario": "Create a new empty file called 'report.txt'.",
        "correct": "touch report.txt",
        "accept": ["touch report.txt"],
        "hint": "The 'touch' command creates empty files."
    },
    {
        "scenario": "Create nested directories: projects/web/css all at once.",
        "correct": "mkdir -p projects/web/css",
        "accept": ["mkdir -p projects/web/css"],
        "hint": "Use mkdir with the flag that creates parent directories."
    },
    {
        "scenario": "Replace ALL occurrences of 'hello' with 'hi' in greet.txt, save to new.txt.",
        "correct": "sed 's/hello/hi/g' greet.txt > new.txt",
        "accept": ["sed 's/hello/hi/g' greet.txt > new.txt", "sed 's/hello/hi/g' greet.txt >new.txt"],
        "hint": "Use sed with the substitute command and redirect output."
    },
    {
        "scenario": "Make script.sh executable by everyone.",
        "correct": "chmod 755 script.sh",
        "accept": ["chmod 755 script.sh", "chmod +x script.sh"],
        "hint": "chmod changes permissions. 755 = rwxr-xr-x."
    },
    {
        "scenario": "Show only the first field (username) from /etc/passwd (colon-separated).",
        "correct": "cut -d ':' -f 1 /etc/passwd",
        "accept": ["cut -d ':' -f 1 /etc/passwd", "cut -d: -f1 /etc/passwd", "awk -F ':' '{print $1}' /etc/passwd"],
        "hint": "Use cut with the delimiter and field flags, OR awk with -F."
    },
    {
        "scenario": "Sort the file words.txt and remove duplicate lines.",
        "correct": "sort words.txt | uniq",
        "accept": ["sort words.txt | uniq", "sort -u words.txt"],
        "hint": "Sort first so duplicates are adjacent, then filter with uniq."
    },
    {
        "scenario": "Start the apache2 web server service.",
        "correct": "sudo systemctl start apache2",
        "accept": ["sudo systemctl start apache2"],
        "hint": "Use systemctl to manage services. Remember sudo!"
    },
    {
        "scenario": "Schedule a task to run /root/backup.sh every day at 3:00 AM.",
        "correct": "crontab -e  →  0 3 * * * /root/backup.sh",
        "accept": ["crontab -e", "0 3 * * * /root/backup.sh"],
        "hint": "Edit the crontab file. Format: MIN HOUR DAY MON DOW command"
    },
    {
        "scenario": "Compress your home directory into backup.tar.gz",
        "correct": "tar -czvf backup.tar.gz ~",
        "accept": ["tar -czvf backup.tar.gz ~", "tar -czvf backup.tar.gz ~/"],
        "hint": "tar with c=create, z=gzip, v=verbose, f=filename. ~ = home."
    },
    {
        "scenario": "Count how many lines are in /etc/passwd.",
        "correct": "wc -l /etc/passwd",
        "accept": ["wc -l /etc/passwd", "cat /etc/passwd | wc -l"],
        "hint": "wc counts things. -l = lines."
    },
]

# ─── SCORE FILE ──────────────────────────────────────────────────────────────
SCORE_FILE = os.path.expanduser("~/.command_tutor_scores.json")

def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"sessions": [], "total_correct": 0, "total_attempts": 0}

def save_scores(scores):
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except Exception:
        pass

# ─── UI HELPERS ──────────────────────────────────────────────────────────────
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    clear()
    w = shutil.get_terminal_size((80, 24)).columns
    print(C.CYAN + C.BOLD + "═" * w + C.RESET)
    title = "🐧  Interactive Command Tutor  🐧"
    sub   = "COSC-3411 — Basic Command I & II"
    print(C.CYAN + C.BOLD + title.center(w) + C.RESET)
    print(C.DIM + sub.center(w) + C.RESET)
    print(C.CYAN + C.BOLD + "═" * w + C.RESET)

def section(title):
    w = shutil.get_terminal_size((80, 24)).columns
    print()
    print(C.YELLOW + C.BOLD + f"  ── {title} " + "─" * max(0, w - len(title) - 7) + C.RESET)

def input_prompt(prompt=""):
    try:
        return input(C.GREEN + "  ❯ " + prompt + C.RESET).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return "q"

def wait():
    input(C.DIM + "\n  Press Enter to continue..." + C.RESET)

def print_cmd(cmd):
    """Pretty print a command entry."""
    print()
    cat_color = C.CYAN if cmd["category"] == "Basic I" else C.MAGENTA
    print(f"  {cat_color}[{cmd['category']}]{C.RESET}  {C.BOLD}{C.YELLOW}{cmd['name'].upper()}{C.RESET}")
    print(f"  {C.DIM}Syntax:{C.RESET}  {C.GREEN}{cmd['syntax']}{C.RESET}")
    print()
    # wrap description
    desc = cmd["description"]
    words = desc.split()
    line = "  "
    for w in words:
        if len(line) + len(w) + 1 > 76:
            print(line)
            line = "    " + w + " "
        else:
            line += w + " "
    if line.strip():
        print(line)
    print()
    print(f"  {C.BOLD}Example:{C.RESET}")
    for ex_line in cmd["example"].split("\n"):
        print(f"    {C.CYAN}{ex_line}{C.RESET}")
    print()
    print(f"  {C.YELLOW}💡 Tip:{C.RESET} {cmd['tip']}")

# ─── MODE 1: LEARN ───────────────────────────────────────────────────────────
def learn_mode():
    while True:
        banner()
        section("LEARN MODE")
        cats = ["Basic I", "Basic II", "All", "Search by keyword", "Back"]
        for i, c in enumerate(cats, 1):
            print(f"    {C.BOLD}{i}.{C.RESET} {c}")
        choice = input_prompt("Select category: ")
        if choice in ("q", "5"):
            return
        if choice == "1":
            pool = [c for c in COMMANDS if c["category"] == "Basic I"]
        elif choice == "2":
            pool = [c for c in COMMANDS if c["category"] == "Basic II"]
        elif choice == "3":
            pool = list(COMMANDS)
        elif choice == "4":
            kw = input_prompt("Enter keyword: ").lower()
            pool = [c for c in COMMANDS if
                    kw in c["name"].lower() or
                    kw in c["description"].lower() or
                    any(kw in k for k in c["keywords"])]
            if not pool:
                print(C.RED + "\n  No commands found for that keyword." + C.RESET)
                wait()
                continue
        else:
            continue

        idx = 0
        while True:
            banner()
            cmd = pool[idx]
            section(f"Command {idx+1} of {len(pool)}")
            print_cmd(cmd)
            print()
            nav = f"  [N]ext  [P]rev  [Q]uit  ({idx+1}/{len(pool)})"
            print(C.DIM + nav + C.RESET)
            key = input_prompt().lower()
            if key in ("n", ""):
                idx = (idx + 1) % len(pool)
            elif key == "p":
                idx = (idx - 1) % len(pool)
            elif key == "q":
                break

# ─── MODE 2: QUIZ ────────────────────────────────────────────────────────────
def quiz_mode():
    banner()
    section("QUIZ MODE")
    print("  How many questions?")
    n_str = input_prompt("(5-30, default 10): ")
    try:
        n = max(1, min(30, int(n_str)))
    except Exception:
        n = 10

    questions = random.sample(QUIZ_QUESTIONS, min(n, len(QUIZ_QUESTIONS)))
    correct = 0
    wrong_list = []

    for i, q in enumerate(questions, 1):
        banner()
        section(f"Question {i} / {len(questions)}")
        print(f"\n  {C.BOLD}{q['question']}{C.RESET}\n")
        opts = q["options"][:]
        random.shuffle(opts)
        for j, opt in enumerate(opts, 1):
            print(f"    {C.BOLD}{j}.{C.RESET} {opt}")
        print()
        ans = input_prompt("Your answer (number or text): ")

        # check by number or text
        chosen = None
        if ans.isdigit() and 1 <= int(ans) <= len(opts):
            chosen = opts[int(ans) - 1]
        else:
            chosen = ans

        if chosen.lower().strip() == q["answer"].lower().strip():
            print(C.GREEN + C.BOLD + "\n  ✅  Correct!" + C.RESET)
            correct += 1
        else:
            print(C.RED + C.BOLD + f"\n  ❌  Wrong! Correct answer: {C.RESET}{C.YELLOW}{q['answer']}{C.RESET}")
            wrong_list.append(q)

        print(C.DIM + f"\n  💡 {q['explanation']}" + C.RESET)
        time.sleep(0.5)
        wait()

    # Score
    banner()
    section("QUIZ RESULTS")
    pct = int(correct / len(questions) * 100)
    bar_len = 40
    filled = int(bar_len * correct / len(questions))
    bar = C.GREEN + "█" * filled + C.RED + "░" * (bar_len - filled) + C.RESET
    print(f"\n  Score: {bar} {C.BOLD}{correct}/{len(questions)} ({pct}%){C.RESET}\n")
    if pct >= 90:
        print(C.GREEN + "  🏆  Excellent! You mastered these commands!" + C.RESET)
    elif pct >= 70:
        print(C.YELLOW + "  👍  Good job! Review the ones you missed." + C.RESET)
    elif pct >= 50:
        print(C.YELLOW + "  📚  Keep studying — use Learn Mode to review." + C.RESET)
    else:
        print(C.RED + "  💪  Don't give up! Practice makes perfect." + C.RESET)

    if wrong_list:
        print(f"\n  {C.BOLD}Review these:{C.RESET}")
        for wq in wrong_list:
            print(f"    • {wq['question']}")
            print(f"      → {C.YELLOW}{wq['answer']}{C.RESET}")

    # Save score
    scores = load_scores()
    scores["total_correct"] += correct
    scores["total_attempts"] += len(questions)
    scores["sessions"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "correct": correct,
        "total": len(questions),
        "pct": pct
    })
    save_scores(scores)

    wait()

# ─── MODE 3: PRACTICE ────────────────────────────────────────────────────────
def practice_mode():
    banner()
    section("PRACTICE MODE — Type the Command")
    print("  A scenario is shown. Type the correct command.\n")
    print(f"  {C.DIM}Type 'hint' for a clue. Type 'skip' to move on. Type 'q' to quit.{C.RESET}\n")
    wait()

    pool = random.sample(SCENARIOS, len(SCENARIOS))
    correct = 0
    total = 0

    for sc in pool:
        banner()
        section("Scenario")
        print(f"\n  {C.BOLD}{sc['scenario']}{C.RESET}\n")
        attempts = 0
        solved = False
        while attempts < 3:
            ans = input_prompt("$ ")
            if ans.lower() == "q":
                return
            if ans.lower() == "hint":
                print(C.YELLOW + f"  💡 Hint: {sc['hint']}" + C.RESET)
                continue
            if ans.lower() == "skip":
                print(C.DIM + f"  ⏭  Answer: {sc['correct']}" + C.RESET)
                break
            # Check
            accepted = [a.lower().strip() for a in sc["accept"]]
            if ans.lower().strip() in accepted:
                print(C.GREEN + C.BOLD + "  ✅  Correct!" + C.RESET)
                correct += 1
                solved = True
                break
            else:
                attempts += 1
                remaining = 3 - attempts
                if remaining > 0:
                    print(C.RED + f"  ❌  Not quite. {remaining} attempt(s) left. Try again." + C.RESET)
                else:
                    print(C.RED + f"  ❌  Answer: {C.RESET}{C.YELLOW}{sc['correct']}{C.RESET}")
        total += 1
        time.sleep(0.3)
        wait()

    banner()
    section("PRACTICE RESULTS")
    pct = int(correct / total * 100) if total else 0
    print(f"\n  Score: {C.BOLD}{correct}/{total} ({pct}%){C.RESET}\n")
    wait()

# ─── MODE 4: CHEATSHEET ──────────────────────────────────────────────────────
def cheatsheet_mode():
    banner()
    section("CHEATSHEET — Quick Reference")
    print(f"  {C.DIM}Filter by: [1] Basic I  [2] Basic II  [3] All  [Q] Back{C.RESET}\n")
    choice = input_prompt("Filter: ")
    if choice == "1":
        pool = [c for c in COMMANDS if c["category"] == "Basic I"]
    elif choice == "2":
        pool = [c for c in COMMANDS if c["category"] == "Basic II"]
    elif choice.lower() == "q":
        return
    else:
        pool = COMMANDS

    banner()
    section("CHEATSHEET")
    cur_cat = ""
    for cmd in pool:
        if cmd["category"] != cur_cat:
            cur_cat = cmd["category"]
            cat_color = C.CYAN if cur_cat == "Basic I" else C.MAGENTA
            print(f"\n  {cat_color}{C.BOLD}── {cur_cat} ──────────────────────────────────{C.RESET}")
        name_col  = C.YELLOW + C.BOLD + f"{cmd['name']:<20}" + C.RESET
        syn_col   = C.GREEN  + f"{cmd['syntax']:<35}" + C.RESET
        # short desc
        short_desc = cmd["description"].split(".")[0][:50]
        print(f"    {name_col}  {syn_col}  {C.DIM}{short_desc}{C.RESET}")
    print()
    wait()

# ─── MODE 5: SCORES ──────────────────────────────────────────────────────────
def scores_mode():
    banner()
    section("YOUR SCORES")
    scores = load_scores()
    total_a = scores["total_attempts"]
    total_c = scores["total_correct"]
    sessions = scores["sessions"]
    if total_a == 0:
        print(C.DIM + "\n  No quiz history yet. Take a quiz first!" + C.RESET)
    else:
        pct = int(total_c / total_a * 100)
        print(f"\n  Overall: {C.BOLD}{total_c}/{total_a} ({pct}%){C.RESET}")
        print(f"  Sessions played: {len(sessions)}\n")
        print(f"  {C.BOLD}Last 5 sessions:{C.RESET}")
        for s in sessions[-5:][::-1]:
            bar = "█" * (s["pct"] // 10) + "░" * (10 - s["pct"] // 10)
            color = C.GREEN if s["pct"] >= 70 else C.YELLOW if s["pct"] >= 50 else C.RED
            print(f"    {s['date']}  {color}{bar}{C.RESET}  {s['correct']}/{s['total']} ({s['pct']}%)")
    wait()

# ─── MAIN MENU ───────────────────────────────────────────────────────────────
def main():
    # Check for --help flag
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    while True:
        banner()
        scores = load_scores()
        if scores["total_attempts"] > 0:
            pct = int(scores["total_correct"] / scores["total_attempts"] * 100)
            print(C.DIM + f"  Your score: {scores['total_correct']}/{scores['total_attempts']} ({pct}%)" + C.RESET)
        print()
        print(f"  {C.BOLD}1.{C.RESET} 📖  Learn Mode   — Study commands with explanations")
        print(f"  {C.BOLD}2.{C.RESET} 🧠  Quiz Mode    — Multiple choice questions")
        print(f"  {C.BOLD}3.{C.RESET} ⌨️   Practice     — Type the correct command for a scenario")
        print(f"  {C.BOLD}4.{C.RESET} 📋  Cheatsheet   — Quick reference for all commands")
        print(f"  {C.BOLD}5.{C.RESET} 📊  My Scores    — View your quiz history")
        print(f"  {C.BOLD}6.{C.RESET} ❌  Exit")
        print()
        choice = input_prompt("Select option: ")
        if choice == "1":
            learn_mode()
        elif choice == "2":
            quiz_mode()
        elif choice == "3":
            practice_mode()
        elif choice == "4":
            cheatsheet_mode()
        elif choice == "5":
            scores_mode()
        elif choice in ("6", "q", "exit", "quit"):
            banner()
            print(C.GREEN + C.BOLD + "\n  Happy hacking! 🐧\n" + C.RESET)
            sys.exit(0)

if __name__ == "__main__":
    main()
