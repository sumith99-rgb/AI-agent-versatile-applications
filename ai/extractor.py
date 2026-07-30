import re


class Extractor:

    def __init__(self):
        pass

    def extract(self, tool, text):

        text_lower = text.lower()

        # ----------------------------
        # MEMORY
        # ----------------------------

        if tool == "memory":

            if "my name is" in text_lower:

                name = re.split(
                    r"my name is",
                    text,
                    flags=re.IGNORECASE
                )[1].strip()

                return {

                    "name": name

                }

            return {}

        # ----------------------------
        # TICKET
        # ----------------------------

        elif tool == "ticket":

            return {

                "description": text

            }

        # ----------------------------
        # EMERGENCY
        # ----------------------------

        elif tool == "emergency":

            return {

                "description": text,

                "priority": "high"

            }

        return {}