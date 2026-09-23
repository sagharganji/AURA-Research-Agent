from typing import List

from pydantic import BaseModel, Field

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


class ResearchTask(BaseModel):
    id: int
    task_type: str
    query: str
    purpose: str


class ResearchPlan(BaseModel):
    goal: str
    domain: str
    constraints: List[str] = Field(default_factory=list)
    tasks: List[ResearchTask]


PLANNER_PROMPT = """
You are the Task Planner Agent of AURA,
an AI Research & Decision Agent.

Your responsibility is to convert a scientific or technical
question into a structured research plan.

You must:

1. Understand the user's goal.
2. Identify the scientific or technical domain.
3. Identify relevant constraints.
4. Break the goal into research tasks.
5. Generate useful search queries.

Possible task types include:

- paper_search
- dataset_search
- code_search
- documentation_search
- method_comparison
- limitation_analysis
- implementation_planning

Do not answer the research question itself.
Only create the research plan.
"""


def create_research_plan(
    user_question: str
) -> ResearchPlan:

    prompt = f"""
{PLANNER_PROMPT}

USER QUESTION:

{user_question}

Return ONLY valid JSON in this format:

{{
    "goal": "main goal",
    "domain": "research domain",
    "constraints": [],
    "tasks": [
        {{
            "id": 1,
            "task_type": "paper_search",
            "query": "search query",
            "purpose": "purpose of task"
        }}
    ]
}}
"""

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    data = clean_json_response(
        response.text
    )

    return ResearchPlan(**data)
