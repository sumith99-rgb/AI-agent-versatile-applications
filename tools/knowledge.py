"""
Knowledge tool - simple search over the `knowledge/` folder
"""
import os
import json
import glob

from tools.base_tool import BaseTool


class KnowledgeTool(BaseTool):

    @property
    def name(self):
        return "knowledge"

    def execute(self, arguments):

        query = (arguments.get("query") or "").strip().lower()

        if not query:
            return {"status": "error", "message": "no query provided"}

        matches = []

        base = "knowledge"

        if not os.path.exists(base):
            return {"status": "ok", "matches": []}

        for path in glob.glob(os.path.join(base, "**", "*.*"), recursive=True):
            try:
                if path.lower().endswith(".json"):
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        text = json.dumps(data).lower()
                else:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read().lower()

                if query in text:
                    matches.append(path)

            except Exception:
                # ignore invalid files
                continue

        return {"status": "ok", "matches": matches}
