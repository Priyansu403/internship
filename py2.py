import json
import os

VAULT_FILE = "vault.json"


# Load data
def load_vault():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}


# Save data
def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)


# Add entry
def add_entry(vault):
    website = input("Enter Website: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    vault[website] = {
        "username": username,
        "password": password
    }

    save_vault(vault)
    print("Entry Added Successfully!")


# Get entry
def get_entry(vault):
    website = input("Enter Website: ")

    if website in vault:
        print("\nWebsite :", website)
        print("Username:", vault[website]["username"])
        print("Password:", vault[website]["password"])
    else:
        print("Website Not Found!")


# List websites
def list_entries(vault):
    if not vault:
        print("No Entries Found!")
        return

    print("\nStored Websites:")
    print("----------------")
    for website in vault:
        print(website)


# Delete entry
def delete_entry(vault):
    website = input("Enter Website To Delete: ")

    if website in vault:
        del vault[website]
        save_vault(vault)
        print("Entry Deleted Successfully!")
    else:
        print("Website Not Found!")


# Main Menu
def main():

    vault = load_vault()

    while True:

        print("\n==========================")
        print(" CLI PASSWORD MANAGER ")
        print("==========================")
        print("1. Add Entry")
        print("2. Get Entry")
        print("3. List Websites")
        print("4. Delete Entry")
        print("5. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_entry(vault)

        elif choice == "2":
            get_entry(vault)

        elif choice == "3":
            list_entries(vault)

        elif choice == "4":
            delete_entry(vault)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()