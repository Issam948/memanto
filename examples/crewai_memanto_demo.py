"""
Official Solution for Memanto Issue #37:
[BOUNTY $100] Best-in-Class Integration: CrewAI + Memanto Agentic Memory
Repository: https://github.com/moorcheh-ai/memanto/issues/37
Package: crewai-memanto
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_memanto import MemantoSetup

def main():
    print("=== Initializing Memanto Long-Term Agentic Memory for CrewAI ===")

    # 1. Initialize Memanto Memory Layer
    # Memanto automatically exposes three native tools: 'remember', 'recall', and 'answer'
    memanto_api_key = os.getenv("MEMANTO_API_KEY", "demo_memanto_key")
    memanto = MemantoSetup(api_key=memanto_api_key)
    memory_tools = memanto.get_tools()

    # 2. Agent 1: Research Analyst (Captures and permanently stores user preferences)
    analyst = Agent(
        role="Capital Strategy Analyst",
        goal="Extract critical financial constraints and store them permanently into Memanto.",
        backstory="Expert in identifying client mandates and recording them using the 'remember' tool.",
        tools=memory_tools,
        verbose=True
    )

    # 3. Agent 2: Executive Strategist (Cross-Session Agent with no direct input)
    strategist = Agent(
        role="Portfolio Execution Strategist",
        goal="Recall previous facts from Memanto to draft an execution plan without re-asking.",
        backstory="Never asks the client twice. Queries Memanto memory using 'recall' and 'answer'.",
        tools=memory_tools,
        verbose=True
    )

    # 4. Task 1: Store information into Memanto persistence
    task_record = Task(
        description=(
            "The user established: 'Our personal savings are strictly $100.00, "
            "we mandate non-custodial crypto settlement with zero human sales calls.' "
            "Use the 'remember' tool to store this preference with confidence score 1.0."
        ),
        expected_output="Confirmation that preference is stored in Memanto.",
        agent=analyst
    )

    # 5. Task 2: Recall information and formulate output
    task_synthesize = Task(
        description=(
            "Use the 'recall' tool to search Memanto for 'savings' and 'mandate'. "
            "Synthesize a strict operational directive based ONLY on the recalled memory."
        ),
        expected_output="An execution plan strictly grounded in recalled Memanto memory.",
        agent=strategist
    )

    # 6. Crew Orchestration (Crucial: memory=False prevents CrewAI LanceDB conflict)
    crew = Crew(
        agents=[analyst, strategist],
        tasks=[task_record, task_synthesize],
        process=Process.sequential,
        memory=False,  # Enforces Memanto as the primary authoritative memory layer
        verbose=True
    )

    print("\n=== Executing Cross-Agent Memory Test ===")
    result = crew.kickoff()
    print("\n=== FINAL RESULT SYNTHESIZED FROM MEMANTO ===")
    print(result)

if __name__ == "__main__":
    main()
  
