import json
import os

from config import MEMORY_FILE


class MemoryManager:

    def __init__(self):
        self.memory = self.load()

    def load(self):

        if os.path.exists(MEMORY_FILE):

            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        return {
            "user": {},
            "preferences": {},
            "company": {},
            "tickets": [],
            "conversation": []
        }

    def save(self):

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:

            json.dump(
                self.memory,
                f,
                indent=4
            )

    # -------------------------
    # USER MEMORY
    # -------------------------

    def set_user(self, key, value):

        self.memory["user"][key] = value

        self.save()

    def get_user(self, key):

        return self.memory["user"].get(key)

    # -------------------------
    # PREFERENCES
    # -------------------------

    def set_preference(self, key, value):

        self.memory["preferences"][key] = value

        self.save()

    def get_preference(self, key):

        return self.memory["preferences"].get(key)

    # -------------------------
    # COMPANY
    # -------------------------

    def set_company(self, key, value):

        self.memory["company"][key] = value

        self.save()

    def get_company(self, key):

        return self.memory["company"].get(key)

    # -------------------------
    # CONVERSATION
    # -------------------------

    def add_message(self, role, message):

        self.memory["conversation"].append({

            "role": role,
            "message": message

        })

        self.save()

    def get_conversation(self):

        return self.memory["conversation"]

    # -------------------------
    # TICKETS
    # -------------------------

    def add_ticket(self, ticket):

        self.memory["tickets"].append(ticket)

        self.save()

    def get_tickets(self):

        return self.memory["tickets"]

    # -------------------------
    # DEBUG
    # -------------------------

    def print_memory(self):

        print(json.dumps(
            self.memory,
            indent=4
        ))