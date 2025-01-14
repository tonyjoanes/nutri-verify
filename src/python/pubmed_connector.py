# src/pubmed_connector.py

import httpx
from typing import List, Dict
from datetime import datetime

class PubMedConnector:
    """Simple PubMed connector"""
    
    def __init__(self, email: str):
        self.email = email
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search_articles(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search PubMed articles"""
        
        # Search parameters
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': str(max_results),
            'retmode': 'json',
            'tool': 'nutriverify',
            'email': self.email
        }
        
        async with httpx.AsyncClient() as client:
            # Get article IDs
            search_response = await client.get(
                f"{self.base_url}/esearch.fcgi",
                params=params
            )
            
            data = search_response.json()
            ids = data['esearchresult']['idlist']
            
            # Get article details
            details_params = {
                'db': 'pubmed',
                'id': ','.join(ids),
                'retmode': 'json',
                'tool': 'nutriverify',
                'email': self.email
            }
            
            details_response = await client.get(
                f"{self.base_url}/esummary.fcgi",
                params=details_params
            )
            
            articles = []
            details_data = details_response.json()
            
            for pmid in ids:
                article_data = details_data['result'][pmid]
                
                article = {
                    'pmid': pmid,
                    'title': article_data.get('title', ''),
                    'authors': [a.get('name', '') for a in article_data.get('authors', [])],
                    'journal': article_data.get('source', ''),
                    'date': article_data.get('pubdate', ''),
                }
                
                articles.append(article)
            
            return articles