# ============================================================
# IT Helpdesk Ticket Tracker
# Author: Junior Graham
# Description: A command-line IT helpdesk ticket management
# system that simulates real-world service desk
# workflows including ticket creation, assignment,
# status updates, priority management, and logging.
# ============================================================
import json
import os
import datetime
# ── File where all tickets are saved ──────────────────────────
DATA_FILE = "tickets.json"
# ── Allowed values ─────────────────────────────────────────────
VALID_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
VALID_CATEGORIES = [
"Hardware", "Software", "Network", "Account Access",
"Email", "Printer", "Other"
]
# ══════════════════════════════════════════════════════════════
# DATA HELPERS
# ══════════════════════════════════════════════════════════════
def load_tickets():
"""Load tickets from the JSON file. Return empty list if none exist."""
if not os.path.exists(DATA_FILE):
return []
with open(DATA_FILE, "r") as f:
return json.load(f)
def save_tickets(tickets):
"""Save the current ticket list to the JSON file."""
with open(DATA_FILE, "w") as f:
json.dump(tickets, f, indent=4)
def generate_ticket_id(tickets):
"""Generate the next ticket ID in the format TKT-0001."""
if not tickets:
return "TKT-0001"
last_id = tickets[-1]["id"] # e.g. "TKT-0042"
number = int(last_id.split("-")[1]) # → 42
return f"TKT-{number + 1:04d}" # → "TKT-0043"
def get_timestamp():
"""Return the current date and time as a readable string."""
return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# ══════════════════════════════════════════════════════════════
# DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════
def print_divider(char="═", width=60):
print(char * width)
def print_header(title):
print_divider()
print(f" {title}")
print_divider()
def print_ticket(ticket):
"""Print a single ticket in a clean, readable format."""
print_divider("─")
print(f" ID : {ticket['id']}")
print(f" Title : {ticket['title']}")
print(f" Category : {ticket['category']}")
print(f" Priority : {ticket['priority']}")
print(f" Status : {ticket['status']}")
print(f" Assigned : {ticket['assigned_to']}")
print(f" Created : {ticket['created_at']}")
print(f" Updated : {ticket['updated_at']}")
print(f" Description:")
print(f" {ticket['description']}")
if ticket.get("notes"):
print(f" Notes:")
for note in ticket["notes"]:
print(f" [{note['timestamp']}] {note['text']}")
print_divider("─")
def choose_from_list(prompt, options):
"""
Display a numbered menu and return the user's chosen option.
Keeps asking until a valid number is entered.
"""
print(f"\n{prompt}")
for i, option in enumerate(options, 1):
print(f" {i}. {option}")
while True:
choice = input(" Enter number: ").strip()
if choice.isdigit() and 1 <= int(choice) <= len(options):
return options[int(choice) - 1]
print(" ⚠ Invalid choice. Please enter a number from the list.")
# ══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════
def create_ticket(tickets):
"""Collect details from the user and create a new ticket."""
print_header("CREATE NEW TICKET")
title = input("\n Ticket title (brief summary): ").strip()
if not title:
print(" ⚠ Title cannot be empty.")
return
description = input(" Description (full details): ").strip()
if not description:
print(" ⚠ Description cannot be empty.")
return
category = choose_from_list("Select category:", VALID_CATEGORIES)
priority = choose_from_list("Select priority:", VALID_PRIORITIES)
assigned_to = input("\n Assign to (technician name or 'Unassigned'): ").strip()
if not assigned_to:
assigned_to = "Unassigned"
now = get_timestamp()
ticket = {
"id" : generate_ticket_id(tickets),
"title" : title,
"description" : description,
"category" : category,
"priority" : priority,
"status" : "Open",
"assigned_to" : assigned_to,
"created_at" : now,
"updated_at" : now,
"notes" : []
}
tickets.append(ticket)
save_tickets(tickets)
print(f"\n ✔ Ticket {ticket['id']} created successfully.")
def view_all_tickets(tickets):
"""Display all tickets, with optional filtering by status."""
print_header("ALL TICKETS")
if not tickets:
print("\n No tickets found.")
return
filter_choice = input("\n Filter by status? (press Enter to show all, or type: Open / In filtered = tickets
if filter_choice:
filtered = [t for t in tickets if t["status"].lower() == filter_choice.lower()]
if not filtered:
print(f"\n No tickets found with status '{filter_choice}'.")
return
print(f"\n Showing {len(filtered)} ticket(s):\n")
for ticket in filtered:
print_ticket(ticket)
def search_tickets(tickets):
"""Search tickets by ID, keyword in title, or assigned technician."""
print_header("SEARCH TICKETS")
if not tickets:
print("\n No tickets to search.")
return
query = input("\n Enter ticket ID, keyword, or technician name: ").strip().lower()
if not query:
print(" ⚠ Search query cannot be empty.")
return
results = [
t for t in tickets
if query in t["id"].lower()
or query in t["title"].lower()
or query in t["description"].lower()
or query in t["assigned_to"].lower()
]
if not results:
print(f"\n No tickets matched '{query}'.")
return
print(f"\n Found {len(results)} result(s):\n")
for ticket in results:
print_ticket(ticket)
def update_ticket(tickets):
"""Update the status, priority, assignment, or add a note to a ticket."""
print_header("UPDATE TICKET")
if not tickets:
print("\n No tickets available to update.")
return
ticket_id = input("\n Enter ticket ID to update (e.g. TKT-0001): ").strip().upper()
ticket = next((t for t in tickets if t["id"] == ticket_id), None)
if not ticket:
print(f" ⚠ Ticket '{ticket_id}' not found.")
return
print("\n Current ticket:")
print_ticket(ticket)
action = choose_from_list(
"What would you like to update?",
["Status", "Priority", "Assigned To", "Add Note", "Cancel"]
)
if action == "Cancel":
return
if action == "Status":
ticket["status"] = choose_from_list("Select new status:", VALID_STATUSES)
elif action == "Priority":
ticket["priority"] = choose_from_list("Select new priority:", VALID_PRIORITIES)
elif action == "Assigned To":
new_assignee = input("\n New assignee name: ").strip()
if new_assignee:
ticket["assigned_to"] = new_assignee
elif action == "Add Note":
note_text = input("\n Enter note: ").strip()
if note_text:
ticket["notes"].append({
"timestamp" : get_timestamp(),
"text" : note_text
})
ticket["updated_at"] = get_timestamp()
save_tickets(tickets)
print(f"\n ✔ Ticket {ticket_id} updated successfully.")
def delete_ticket(tickets):
"""Permanently delete a ticket after confirmation."""
print_header("DELETE TICKET")
if not tickets:
print("\n No tickets to delete.")
return
ticket_id = input("\n Enter ticket ID to delete (e.g. TKT-0001): ").strip().upper()
ticket = next((t for t in tickets if t["id"] == ticket_id), None)
if not ticket:
print(f" ⚠ Ticket '{ticket_id}' not found.")
return
print("\n Ticket to delete:")
print_ticket(ticket)
confirm = input(" Are you sure you want to delete this ticket? (yes/no): ").strip().lower()
if confirm == "yes":
tickets.remove(ticket)
save_tickets(tickets)
print(f"\n ✔ Ticket {ticket_id} deleted.")
else:
print(" Deletion cancelled.")
def show_summary(tickets):
"""Print a summary dashboard of ticket counts by status and priority."""
print_header("TICKET SUMMARY DASHBOARD")
if not tickets:
print("\n No tickets in the system.")
return
total = len(tickets)
# Count by status
status_counts = {s: 0 for s in VALID_STATUSES}
for t in tickets:
if t["status"] in status_counts:
status_counts[t["status"]] += 1
# Count by priority
priority_counts = {p: 0 for p in VALID_PRIORITIES}
for t in tickets:
if t["priority"] in priority_counts:
priority_counts[t["priority"]] += 1
# Count by category
category_counts = {}
for t in tickets:
category_counts[t["category"]] = category_counts.get(t["category"], 0) + 1
print(f"\n Total Tickets : {total}\n")
print(" By Status:")
for status, count in status_counts.items():
bar = "█" * count
print(f" {status:<14} {count:>3} {bar}")
print("\n By Priority:")
for priority, count in priority_counts.items():
bar = "█" * count
print(f" {priority:<14} {count:>3} {bar}")
print("\n By Category:")
for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
bar = "█" * count
print(f" {category:<14} {count:>3} {bar}")
# ══════════════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════════════
def main():
print("\n" + "═" * 60)
print(" IT HELPDESK TICKET TRACKER")
print(" By Junior Graham")
print("═" * 60)
while True:
tickets = load_tickets() # reload each loop so data is always fresh
print("\n MAIN MENU")
print_divider("─")
print(" 1. Create New Ticket")
print(" 2. View All Tickets")
print(" 3. Search Tickets")
print(" 4. Update Ticket")
print(" 5. Delete Ticket")
print(" 6. Summary Dashboard")
print(" 7. Exit")
print_divider("─")
choice = input(" Select an option (1-7): ").strip()
if choice == "1": create_ticket(tickets)
elif choice == "2": view_all_tickets(tickets)
elif choice == "3": search_tickets(tickets)
elif choice == "4": update_ticket(tickets)
elif choice == "5": delete_ticket(tickets)
elif choice == "6": show_summary(tickets)
elif choice == "7":
print("\n Goodbye!\n")
break
else:
print(" ⚠ Invalid option. Please enter a number between 1 and 7.")
if __name__ == "__main__":
main()
