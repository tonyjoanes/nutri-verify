# src/python/pubmed_connector.py

import httpx
from typing import List, Dict
import xml.etree.ElementTree as ET

class PubMedConnector:
    """PubMed connector that fetches detailed study information"""
    
    def __init__(self, email: str):
        self.email = email
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search_articles(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search PubMed articles with full details"""
        
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
            
            # Get basic article details
            summary_params = {
                'db': 'pubmed',
                'id': ','.join(ids),
                'retmode': 'json',
                'tool': 'nutriverify',
                'email': self.email
            }
            
            summary_response = await client.get(
                f"{self.base_url}/esummary.fcgi",
                params=summary_params
            )
            
            # Get full article details including abstract
            efetch_params = {
                'db': 'pubmed',
                'id': ','.join(ids),
                'retmode': 'xml',
                'rettype': 'abstract',
                'tool': 'nutriverify',
                'email': self.email
            }
            
            efetch_response = await client.get(
                f"{self.base_url}/efetch.fcgi",
                params=efetch_params
            )
            
            # Parse the XML for abstracts
            abstracts = {}
            try:
                root = ET.fromstring(efetch_response.text)
                for article in root.findall(".//PubmedArticle"):
                    pmid = article.find(".//PMID").text
                    abstract_element = article.find(".//Abstract")
                    if abstract_element is not None:
                        abstract_text = []
                        for section in abstract_element.findall(".//AbstractText"):
                            label = section.get('Label', '')
                            text = section.text or ''
                            if label:
                                abstract_text.append(f"{label}: {text}")
                            else:
                                abstract_text.append(text)
                        abstracts[pmid] = "\n".join(abstract_text)
                    else:
                        abstracts[pmid] = "No abstract available"
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
            
            # Combine all information
            articles = []
            details_data = summary_response.json()
            
            for pmid in ids:
                article_data = details_data['result'][pmid]
                
                # Get publication types
                pub_types = article_data.get('pubtype', [])
                
                # Get DOI if available
                doi = None
                if 'articleids' in article_data:
                    for id_obj in article_data['articleids']:
                        if id_obj.get('idtype') == 'doi':
                            doi = id_obj.get('value')
                
                article = {
                    'pmid': pmid,
                    'title': article_data.get('title', ''),
                    'authors': [a.get('name', '') for a in article_data.get('authors', [])],
                    'journal': article_data.get('source', ''),
                    'date': article_data.get('pubdate', ''),
                    'abstract': abstracts.get(pmid, 'No abstract available'),
                    'publication_types': pub_types,
                    'doi': doi,
                    'keywords': article_data.get('keywords', []),
                }
                
                articles.append(article)
            
            return articles