"""CrewAI multi-agent orchestrator for code analysis workflows."""

from crewai import Agent, Task, Crew


def create_analyst_agent() -> Agent:
    """Create a code analyst agent."""
    return Agent(
        role="Code Security Analyst",
        goal="Identify security vulnerabilities and code quality issues",
        backstory="Expert in static analysis and secure coding practices.",
        verbose=True,
    )


def create_reviewer_agent() -> Agent:
    """Create a code reviewer agent."""
    return Agent(
        role="Senior Code Reviewer",
        goal="Provide actionable improvement suggestions",
        backstory="Seasoned engineer with deep experience in code reviews.",
        verbose=True,
    )


def run_analysis_crew(code_snippet: str) -> str:
    """Run a Crew of agents to analyze code."""
    analyst = create_analyst_agent()
    reviewer = create_reviewer_agent()

    task_analyze = Task(
        description=f"Analyze this code for security issues:\n{code_snippet}",
        agent=analyst,
        expected_output="List of security findings",
    )
    task_review = Task(
        description="Review the analysis and suggest improvements",
        agent=reviewer,
        expected_output="Prioritized recommendations",
        context=[task_analyze],
    )

    crew = Crew(agents=[analyst, reviewer], tasks=[task_analyze, task_review])
    result = crew.kickoff()
    return str(result)
