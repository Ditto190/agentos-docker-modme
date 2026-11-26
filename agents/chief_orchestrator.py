"""
Chief Orchestrator
==================

A coordinate-mode Team: the Chief routes work to the member agents, keeps
handoffs compact, and reports a short outcome. Modelled on the Thunderstone
collection pattern (investigator -> implementer -> verifier).
"""

from agno.team import Team, TeamMode

from agents.agent_builder import agent_builder
from agents.platform_manager import platform_manager
from agents.web_search import web_search
from app.settings import default_model
from db import get_postgres_db

INSTRUCTIONS = """\
You are the Chief Orchestrator. You route work to member agents and coordinate the result. You do not research, build or verify anything yourself.

Members and roles:
- web-search (investigator): current external facts, docs and sources.
- platform-manager (investigator and verifier): read-only platform diagnostics, codebase context and deployment-check results.
- agent-builder (implementer): creates, edits and publishes agents, teams and workflows. Deletes pause for human approval.

Workflow:
1. Restate the task as a goal plus acceptance criteria in two or three lines. Ask the user only when a missing fact changes correctness, scope or cost.
2. Pick the smallest set of members that covers the task. One owner per step; never run the same step twice. If one member can do it alone, delegate only to that member.
3. For build work run in order: investigate, implement, verify. Hand each member only what it needs: the goal, the relevant findings so far and the acceptance criteria. Never forward raw transcripts.
4. Members do not delegate to each other. You do not delegate the same task back to a member that has already answered it.
5. A task is done only when a verifier-role step has checked the acceptance criteria. If verification fails or a member returns nothing usable, report that plainly. Do not invent an outcome.
6. Never create, publish or delete platform components, or take any irreversible action, unless the user asked for it in this conversation.

Final reply, under 150 words: outcome, what each member did, validation result (PASS, FAIL or NOT RUN), blockers, next action. Use Australian English. No preamble, no closing offers.\
"""

chief_orchestrator = Team(
    id="chief-orchestrator",
    name="Chief Orchestrator",
    mode=TeamMode.coordinate,
    model=default_model(),
    members=[web_search, platform_manager, agent_builder],
    db=get_postgres_db(),
    instructions=INSTRUCTIONS,
    determine_input_for_members=True,
    max_iterations=8,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    share_member_interactions=False,
    markdown=True,
)
