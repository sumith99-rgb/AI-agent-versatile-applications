import traceback
import os
os.environ['PYTHONPATH'] = '.'
from core.agent import Agent

try:
    agent = Agent()
    plan = agent.create_plan('Hello')
    print('PLAN:', plan)
except Exception:
    traceback.print_exc()
