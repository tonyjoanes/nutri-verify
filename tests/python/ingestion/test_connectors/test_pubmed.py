# tests/python/ingestion/test_connectors/test_pubmed.py
import sys
import os
from pathlib import Path
import asyncio

# Add the src directory to Python path
root_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from src.python.ingestion.connectors.pubmed import PubMedConnector

async def test_pubmed_search():
    # Initialize the connector with your email
    connector = PubMedConnector(email="your.email@example.com")
    
    try:
        # Search for some nutrition-related articles
        articles = await connector.search_articles(
            query="ketogenic diet diabetes",
            max_results=5,
            date_from="2023/01/01"
        )
        
        # Print results
        print(f"\nFound {len(articles)} articles:")
        for article in articles:
            print("\n-------------------")
            print(f"Title: {article.title}")
            print(f"Authors: {', '.join(article.authors)}")
            print(f"Journal: {article.journal}")
            print(f"Date: {article.publication_date}")
            if article.abstract:
                print(f"Abstract: {article.abstract[:200]}...")
            print(f"PMID: {article.pmid}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(test_pubmed_search())