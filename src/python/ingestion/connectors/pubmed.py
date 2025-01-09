from typing import List, Dict, Optional
from datetime import datetime
import logging
import httpx
from pydantic import BaseModel, Field

class PubMedArticle(BaseModel):
    pmid: str
    title: str
    abstract: Optional[str]
    authors: List[str]
    publication_date: datetime
    journal: str
    keywords: List[str] = Field(default_factory=list)
    doi: Optional[str] = None

class PubMedConnector:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize PubMed connector
        
        Args:
            email: Required email for NCBI E-utilities
            api_key: Optional NCBI API key for higher rate limits
        """
        self.logger = logging.getLogger(__name__)
        self.email = email
        self.api_key = api_key

    async def search_articles(
        self, 
        query: str, 
        max_results: int = 100,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[PubMedArticle]:
        """
        Search PubMed articles based on query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            date_from: Start date in format YYYY/MM/DD
            date_to: End date in format YYYY/MM/DD
        """
        try:
            # Construct date range if provided
            date_range = ""
            if date_from or date_to:
                date_range = f" AND ({date_from or '1900/01/01'}:{date_to or '3000'}[Date - Publication])"
            
            # Build search parameters
            search_params = {
                'db': 'pubmed',
                'term': query + date_range,
                'retmax': str(max_results),
                'sort': 'relevance',
                'retmode': 'json',
                'tool': 'nutriverify',
                'email': self.email
            }
            
            if self.api_key:
                search_params['api_key'] = self.api_key

            # Search for articles
            async with httpx.AsyncClient() as client:
                # First get the PMIDs
                search_response = await client.get(
                    f"{self.BASE_URL}/esearch.fcgi",
                    params=search_params
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                
                if not search_data.get('esearchresult', {}).get('idlist', []):
                    return []

                # Then fetch details for each article
                fetch_params = {
                    'db': 'pubmed',
                    'id': ','.join(search_data['esearchresult']['idlist']),
                    'retmode': 'json',
                    'tool': 'nutriverify',
                    'email': self.email
                }
                
                if self.api_key:
                    fetch_params['api_key'] = self.api_key

                fetch_response = await client.get(
                    f"{self.BASE_URL}/esummary.fcgi",
                    params=fetch_params
                )
                fetch_response.raise_for_status()
                articles_data = fetch_response.json()

                # Process articles
                articles = []
                for pmid, article_data in articles_data.get('result', {}).items():
                    if pmid == 'uids':  # Skip the uids list
                        continue
                        
                    try:
                        article = PubMedArticle(
                            pmid=pmid,
                            title=article_data.get('title', ''),
                            abstract=article_data.get('abstract', ''),
                            authors=[author['name'] for author in article_data.get('authors', [])],
                            publication_date=datetime.strptime(
                                article_data.get('pubdate', ''), 
                                '%Y %b %d'
                            ),
                            journal=article_data.get('source', ''),
                            keywords=article_data.get('keywords', [])
                        )
                        articles.append(article)
                    except Exception as e:
                        self.logger.error(f"Error processing article {pmid}: {str(e)}")
                        continue

                return articles

        except Exception as e:
            self.logger.error(f"Error searching PubMed: {str(e)}")
            raise