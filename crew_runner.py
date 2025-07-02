from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, verification, nutrition_analysis, exercise_planning

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    print("RUN_CREW CALLED", query, file_path)
    medical_crew = Crew(
        agents=[verifier, doctor, nutritionist, exercise_specialist],
        tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
        process=Process.sequential,
        verbose=True
    )
    result = medical_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result 