# src/python/analysis/study_analyzer.py

import json
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging

class StudyAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Set up OpenAI client
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load schema
        self.schema = self._load_schema()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)

    def _load_schema(self) -> Dict:
        """Load the analysis schema from file"""
        try:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema', 'study_analysis_schema.json')
            with open(schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading schema: {str(e)}")
            raise

    def _create_analysis_prompt(self, study_data: Dict) -> str:
        """Create the prompt for the LLM"""
        return f"""You are a research analysis assistant specializing in analyzing scientific studies about nutrition and diet.
        Analyze the following study and create a structured summary following the exact JSON schema provided.

        STUDY DATA:
        Title: {study_data.get('title', '')}
        Authors: {', '.join(study_data.get('authors', []))}
        Journal: {study_data.get('journal', '')}
        Date: {study_data.get('date', '')}
        Type: {study_data.get('type', '')}
        DOI: {study_data.get('doi', '')}
        Abstract: {study_data.get('abstract', '')}

        REQUIRED ANALYSIS STRUCTURE:
        Your response must be a valid JSON object following this exact schema:
        {json.dumps(self.schema, indent=2)}

        ANALYSIS REQUIREMENTS:
        1. Be objective and evidence-based in your assessments
        2. Clearly distinguish between proven and suggested outcomes
        3. Note all limitations and necessary context
        4. Use appropriate evidence_level categorization:
           - Strong: Well-designed RCTs with adequate sample size
           - Moderate: RCTs with limitations or high-quality observational studies
           - Preliminary: Pilot studies, small trials, or initial findings
        5. Consider population characteristics and study design
        6. Be specific about who findings apply to
        7. List both supported and unsupported claims clearly

        RESPONSE:
        Provide your analysis as a single JSON object that exactly matches the schema provided."""

    async def analyze_study(self, study_data: Dict) -> Optional[Dict]:
        """
        Analyze a study using OpenAI's API
        
        Args:
            study_data: Dictionary containing study information
            
        Returns:
            Dictionary containing the structured analysis or None if failed
        """
        try:
            # Create the prompt
            prompt = self._create_analysis_prompt(study_data)
            
            # Get analysis from OpenAI
            response = await self.client.chat.completions.create(
                model="gpt-4",  # or whichever model you prefer
                messages=[
                    {"role": "system", "content": "You are a research analysis assistant that creates structured JSON analysis of scientific studies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2  # Lower temperature for more consistent output
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            analysis = json.loads(analysis_text)
            
            # TODO: Add schema validation here
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing study: {str(e)}")
            return None

# Example usage:
async def main():
    # Example study data
    study_data = {
        "title": "Low-Dose Ketone Monoester Administration in Adults with Cystic Fibrosis: A Pilot and Feasibility Study.",
        "authors": ["Plaisance EP", "Bergeron JM", "Bolyard ML"],
        "journal": "Nutrients",
        "date": "2024 Nov 19",
        "type": "Journal Article, Randomized Controlled Trial",
        "doi": "10.3390/nu16223957",
        "abstract": "Your abstract text here..."
    }
    
    analyzer = StudyAnalyzer()
    analysis = await analyzer.analyze_study(study_data)
    
    if analysis:
        print(json.dumps(analysis, indent=2))
    else:
        print("Analysis failed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())