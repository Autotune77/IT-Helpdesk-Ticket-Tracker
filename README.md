IT Helpdesk Ticket Tracker

A command-line IT helpdesk ticket management system built in Python, simulating realworld
service desk workflows used in enterprise IT environments.

Built by Junior Graham — IT Support Specialist | CS Graduate | CompTIA Tech+

Overview

This project replicates the core functionality of professional ticketing systems like
ServiceNow and Jira Service Management. It allows technicians to create, track, update,
search, and resolve support tickets all persisted to a local JSON file so data survives
between sessions.
Features
Feature Description
Create Tickets
Log new issues with title, description, category, priority, and
assignee
View Tickets List all tickets with optional filtering by status
Search Search by ticket ID, keyword, or assigned technician
Update Change status, priority, reassign, or add timestamped notes
Delete Remove tickets with confirmation prompt
Dashboard Visual summary of tickets by status, priority, and category
Persistent
Storage
All data saved to tickets.json survives between sessions

Tech Stack

Language: Python 3

Storage: JSON (flat-file database)

Libraries: json , os , datetime (all standard library no installs needed)

Getting Started

Prerequisites

Python 3.x installed (download here)

Run the app

# Clone the repo
git clone https://github.com/Junior-Graham/helpdesk-ticket-tracker.git
# Navigate into the folder
cd helpdesk-ticket-tracker
# Run the program
python3 ticket_tracker.py
Demo

════════════════════════════════════════════════════════════

IT HELPDESK TICKET TRACKER

By Junior Graham

════════════════════════════════════════════════════════════

MAIN MENU

────────────────────────────────────────────────────────────

1. Create New Ticket
2. View All Tickets
3. Search Tickets
4. Update Ticket
5. Delete Ticket
6. Summary Dashboard
7. Exit
   
────────────────────────────────────────────────────────────

Summary Dashboard output:

Total Tickets : 4

By Status:

Open 2 ██

In Progress 1 █

Resolved 1 █

By Priority:

Medium 1 █

High 2 ██

Critical 1 █

By Category:

Network 1 █

Email 1 █

Printer 1 █

Account Access 1 █

Project Structure

helpdesk-ticket-tracker/
│
├── ticket_tracker.py # Main application

├── tickets.json # Auto-generated data file (created on first run)

└── README.md # Project documentation

Why I Built This

In my roles as a System Administrator and IT Support Intern at Womack Army Medical Center, I worked daily with ServiceNow to manage hundreds of Tier 1 and Tier 2 support tickets. This project was built to demonstrate a deep understanding of that workflow in code showing how ticketing systems track state, persist data, support search and filtering, andprovide summary analytics for IT managers.

Future Improvements:

1.Export reports to CSV for data analysis

2.Add SLA tracking (flag tickets open > 24 hours)

3.Web interface using Flask

4.Email notification simulation

5.Multi-user login system

Author: Junior Graham

LinkedIn: linkedin.com/in/junior-graham

Email: juniorgraham118@gmail.com
