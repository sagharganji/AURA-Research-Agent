from app.main import run_aura


QUESTION = """
I want to build a solar flare prediction
system using machine learning.

Find relevant papers, datasets and code,
compare existing approaches, identify
limitations, and propose an implementation
roadmap.
"""


result = run_aura(
    QUESTION,
    max_papers=2,
    max_datasets=2,
    max_repositories=2,
    save_output=True,
)

required = [
    "research_plan",
    "evidence",
    "verification",
    "analysis",
    "decision",
    "roadmap",
    "report",
]

for key in required:
    assert key in result


assert len(
    result["report"]
) > 100


print(
    f"✅ Papers: {len(result['papers'])}"
)

print(
    f"✅ Datasets: {len(result['datasets'])}"
)

print(
    f"✅ Repositories: "
    f"{len(result['repositories'])}"
)

print(
    f"✅ Evidence: {len(result['evidence'])}"
)

print(
    f"✅ Claims: "
    f"{len(result['verification'].get('claims', []))}"
)

print(
    f"✅ Roadmap phases: "
    f"{len(result['roadmap'].get('phases', []))}"
)

print(
    "🎉 AURA FINAL MVP TEST PASSED."
)
