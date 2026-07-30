from ai.planner import Planner

planner = Planner()

plan = planner.plan(
    "My name is Sumith"
)

print("\nFINAL PLAN:\n")
print(plan)