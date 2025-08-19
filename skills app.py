import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
db = sqlite3.connect("app.db")
cursor = db.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    progress INTEGER,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

def commit_and_continue():
    db.commit()
    print("\n✅ Operation completed successfully.\n")

# === Functions ===
def show_skills():
    cursor.execute("SELECT users.name, skills.name, skills.progress FROM skills JOIN users ON users.user_id = skills.user_id")
    rows = cursor.fetchall()
    if not rows:
        print("⚠️ No skills found.")
    else:
        for row in rows:
            print(f"User: {row[0]}, Skill: {row[1]}, Progress: {row[2]}")
    commit_and_continue()


def add_skills():
    user_name = input("Write your name: ").strip().capitalize()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
    user_id = cursor.lastrowid

    while True:   # ✅ handling wrong input
        try:
            num_of_skills = int(input("How many skills do you want to add? ").strip())
            break
        except ValueError:
            print("⚠️ Please enter a valid number.")

    for i in range(num_of_skills):
        skill_name = input(f"Enter your skill {i+1} name: ").strip().capitalize()
        while True:
            try:
                progress = int(input(f"Enter progress for {skill_name}: ").strip())
                break
            except ValueError:
                print("⚠️ Progress must be a number.")
        cursor.execute("INSERT INTO skills (name, progress, user_id) VALUES (?, ?, ?)", 
                       (skill_name, progress, user_id))

    commit_and_continue()


def delete_skill():
    cursor.execute("SELECT user_id, name FROM users")
    users = cursor.fetchall()
    if not users:
        print("⚠️ No users found.")
        return

    print("\n---- Users ----")
    for u in users:
        print(f"User ID: {u[0]}, Name: {u[1]}")

    user_id = input("\nEnter the User ID to manage skills: ").strip()

    cursor.execute("SELECT skill_id, name, progress FROM skills WHERE user_id=?", (user_id,))
    skills = cursor.fetchall()
    if not skills:
        print("⚠️ This user has no skills.")
        return

    print(f"\n--- Skills for User {user_id} ---")
    for s in skills:
        print(f"Skill ID: {s[0]}, Name: {s[1]}, Progress: {s[2]}")

    skill_id = input("\nEnter the Skill ID to delete: ").strip()

    cursor.execute("DELETE FROM skills WHERE skill_id=? AND user_id=?", (skill_id, user_id))
    if cursor.rowcount == 0:
        print("⚠️ No skill found with that ID for this user.")
    else:
        print("✅ Skill deleted successfully.")
    commit_and_continue()


def update_skill():
    cursor.execute("SELECT user_id, name FROM users")
    users = cursor.fetchall()
    if not users:
        print("⚠️ No users found.")
        return

    print("\n---- Users ----")
    for u in users:
        print(f"User ID: {u[0]}, Name: {u[1]}")

    user_id = input("\nEnter the User ID to manage skills: ").strip()

    cursor.execute("SELECT skill_id, name, progress FROM skills WHERE user_id=?", (user_id,))
    skills = cursor.fetchall()
    if not skills:
        print("⚠️ This user has no skills.")
        return

    print(f"\n--- Skills for User {user_id} ---")
    for s in skills:
        print(f"Skill ID: {s[0]}, Name: {s[1]}, Progress: {s[2]}")

    skill_id = input("\nEnter the Skill ID to update: ").strip()
    choice = input("Do you want to update (n)ame, (p)rogress, or (b)oth? ").strip().lower()

    new_name, new_progress = None, None
    if choice in ("n", "b"):
        new_name = input("Enter new skill name: ").strip().capitalize()
    if choice in ("p", "b"):
        while True:
            try:
                new_progress = int(input("Enter new progress: ").strip())
                break
            except ValueError:
                print("⚠️ Progress must be a number.")

    if new_name and new_progress:
        cursor.execute("UPDATE skills SET name=?, progress=? WHERE skill_id=? AND user_id=?", 
                       (new_name, new_progress, skill_id, user_id))
    elif new_name:
        cursor.execute("UPDATE skills SET name=? WHERE skill_id=? AND user_id=?", 
                       (new_name, skill_id, user_id))
    elif new_progress:
        cursor.execute("UPDATE skills SET progress=? WHERE skill_id=? AND user_id=?", 
                       (new_progress, skill_id, user_id))
    else:
        print("⚠️ Nothing to update.")
        return

    if cursor.rowcount == 0:
        print("⚠️ No skill found with that ID for this user.")
    else:
        print("✅ Skill updated successfully.")
    commit_and_continue()

# === MAIN LOOP ===
def main():
    while True:
        input_message = """
What Do You Want To Do ?
"s" => Show All Skills
"a" => Add New Skill
"d" => Delete A Skill
"u" => Update Skill Progress
"q" => Quit The App
Choose Option: 
"""
        user_input = input(input_message).strip().lower()

        if user_input == "s":
            show_skills()
        elif user_input == "a":
            add_skills()
        elif user_input == "d":
            delete_skill()
        elif user_input == "u":
            update_skill()
        elif user_input == "q":
            print("👋 App is closed")
            break
        else:
            print("⚠️ Sorry, command not found.")

        # ✅ Ask to continue or exit
        again = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
        if again != "y":
            print("👋 App is closed")
            break

main()
