import json

from ai.brain import Brain

planner_brain = Brain()


class Planner:

    def __init__(self):
        pass

    def plan(self, user_message):

        prompt = f"""
You are an AI planner.

Your job is NOT to answer the user.

Your job is ONLY to decide what action should happen.

Possible actions:

answer
remember
ticket
knowledge
emergency

Return ONLY valid JSON.

Examples

User:
Hello

Output:
{{
    "action":"answer"
}}

User:
My name is Sumith

Output:
{{
    "action":"remember"
}}

User:
My lift is stuck.

Output:
{{
    "action":"ticket"
}}

User:
Someone is trapped inside the lift.

Output:
{{
    "action":"emergency"
}}

User:
How often should lifts be serviced?

Output:
{{
    "action":"knowledge"
}}

User:

{user_message}
"""

        reply = planner_brain.ask(prompt)

        try:

            return json.loads(reply)

        except:

            return {
                "action": "answer"
            }