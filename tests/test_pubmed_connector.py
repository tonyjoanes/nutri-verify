# tests/test.py

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.python.pubmed_connector import PubMedConnector

async def main():
    # Create connector
    connector = PubMedConnector(email="tonyjoanes@outlook.com")
    
    try:
        # Search for articles
        articles = await connector.search_articles("ketogenic diet", max_results=5)
        
        # Print results
        print(f"\nFound {len(articles)} articles:")
        for article in articles:
            print("\n" + "=" * 50)
            print(f"Title: {article['title']}")
            print(f"Authors: {', '.join(article['authors'])}")
            print(f"Journal: {article['journal']}")
            print(f"Date: {article['date']}")
            print("=" * 50)
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())