import json

from ai.brain import Brain

planner_brain = Brain()


class Planner:

    def __init__(self):
        pass

    def plan(self, user_message):

        prompt = """
You are the planning engine of LiftGuard AI.

Your job is NOT to answer the user.

Your job is ONLY to create an execution plan.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Never use markdown.
3. Never wrap the JSON inside ``` or ```json.
4. Never explain your answer.
5. Never add text before or after the JSON.
6. The response must be directly parsable by json.loads().
7. Always return both "thought" and "steps".
8. If a tool should be executed, include it in the "steps" array.
9. Never leave "steps" empty if an action can be performed.

The JSON format is:

{
    "thought":"why you chose these actions",

    "steps":[

        {

            "tool":"memory",

            "arguments":{

                "name":"Sumith"

            }

        }

    ]

}

Available tools:

1. memory
2. ticket
3. emergency
4. knowledge
5. email
6. whatsapp

You MUST ONLY use these tools.

Never invent tools.

If none of these tools apply, return:

{
    "thought":"No tool required.",
    "steps":[]
}

Examples

User:
My name is Sumith

Output:

{
    "thought":"The user introduced himself.",

    "steps":[

        {

            "tool":"memory",

            "arguments":{

                "name":"Sumith"

            }

        }

    ]

}

User:
Hello

Output:

{
    "thought":"The user is greeting.",

    "steps":[]
}

User:
Help I am trapped!

Output:

{
    "thought":"Emergency reported but no address provided. We must wait and ask the user for the address.",

    "steps":[]
}

User:
Someone is trapped in the lift at Building A!

Output:

{
    "thought":"Emergency reported with address.",

    "steps":[

        {

            "tool":"emergency",

            "arguments":{

                "priority":"high",
                "address":"Building A"

            }

        }

    ]

}

User:
"""
        prompt += f"\n{user_message}\n"

        reply = planner_brain.ask(prompt, is_json=True)

        # Remove markdown if the model returns it
        reply = reply.replace("```json", "")
        reply = reply.replace("```", "")
        reply = reply.strip()

        try:

            return json.loads(reply)

        except Exception:

            print("\nPlanner returned invalid JSON.")

            return {

                "thought": "Fallback",

                "steps": []

            }