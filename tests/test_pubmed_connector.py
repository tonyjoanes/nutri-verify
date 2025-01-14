# tests/test.py

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.python.pubmed_connector import PubMedConnector
from src.python.analysis.study_analyzer import StudyAnalyzer

async def main():
    # Create connector and analyzer
    connector = PubMedConnector(email="your.email@example.com")  # Replace with your email
    analyzer = StudyAnalyzer()
    
    try:
        # Get one article
        articles = await connector.search_articles("ketogenic diet clinical trial", max_results=1)
        
        if not articles:
            print("No articles found")
            return
            
        # Get the first article
        study = articles[0]
        
        # Print raw study data
        print("\nRaw Study Data:")
        print("=" * 80)
        print(f"Title: {study['title']}")
        print(f"Authors: {', '.join(study['authors'])}")
        print(f"Journal: {study['journal']}")
        print(f"Date: {study['date']}")
        print(f"Type: {', '.join(study['publication_types'])}")
        if study['doi']:
            print(f"DOI: {study['doi']}")
        if study['keywords']:
            print(f"Keywords: {', '.join(study['keywords'])}")
        print("\nAbstract:")
        print(study['abstract'])
        print("=" * 80)
        
        # Analyze the study
        print("\nAnalyzing study...")
        analysis = await analyzer.analyze_study(study)
        
        if analysis:
            print("\nStructured Analysis:")
            print("=" * 80)
            # Print analysis in a nice format
            print(json.dumps(analysis, indent=2))
            
            # Save the analysis to a file
            output_file = "study_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"\nAnalysis saved to {output_file}")
        else:
            print("Analysis failed")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())