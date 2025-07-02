## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.tools import Tool
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "A tool to read a blood test report from a PDF file path and return the content as a string."

    def _run(self, file_path: str) -> str:
        """Internal function to read data from a pdf file from a path"""
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        full_report = ""
        for data in docs:
            content = data.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
            
        return full_report

read_data_tool = BloodTestReportTool()

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(blood_report_data):        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"

# --- Redis connection test (for debugging) ---
if __name__ == "__main__":
    import redis
    r = redis.Redis(
        host='redis-10036.c267.us-east-1-4.ec2.redns.redis-cloud.com',
        port=10036,
        decode_responses=True,
        username="default",
        password="PQOF9aW386wTkiZHM1JnJAfA4QVqUMDK",
    )
    success = r.set('foo', 'bar')
    print('Set success:', success)
    result = r.get('foo')
    print('Get result:', result)