# src/python/pubmed_connector.py

import httpx
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

class PubMedConnector:
    """PubMed connector that properly extracts abstracts"""
    
    def __init__(self, email: str):
        self.email = email
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search_articles(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search PubMed articles with abstract retrieval"""
        try:
            async with httpx.AsyncClient() as client:
                # First get PMIDs from search
                search_params = {
                    'db': 'pubmed',
                    'term': query,
                    'retmax': str(max_results),
                    'retmode': 'json',
                    'sort': 'relevance',
                    'tool': 'nutriverify',
                    'email': self.email
                }
                
                search_response = await client.get(
                    f"{self.base_url}/esearch.fcgi",
                    params=search_params
                )
                search_data = search_response.json()
                pmids = search_data['esearchresult']['idlist']

                if not pmids:
                    return []

                # Get article details including abstracts using efetch
                efetch_params = {
                    'db': 'pubmed',
                    'id': ','.join(pmids),
                    'retmode': 'xml',
                    'rettype': 'abstract',
                    'tool': 'nutriverify',
                    'email': self.email
                }
                
                efetch_response = await client.get(
                    f"{self.base_url}/efetch.fcgi",
                    params=efetch_params
                )

                # Parse XML to get abstracts
                root = ET.fromstring(efetch_response.text)
                articles_xml = root.findall(".//PubmedArticle")
                
                # Get summary data
                summary_params = {
                    'db': 'pubmed',
                    'id': ','.join(pmids),
                    'retmode': 'json',
                    'tool': 'nutriverify',
                    'email': self.email
                }
                
                summary_response = await client.get(
                    f"{self.base_url}/esummary.fcgi",
                    params=summary_params
                )
                summary_data = summary_response.json()
                
                articles = []
                for pmid, article_xml in zip(pmids, articles_xml):
                    try:
                        # Get abstract from XML
                        abstract_text = ""
                        abstract_element = article_xml.find(".//Abstract")
                        if abstract_element is not None:
                            # Collect all AbstractText elements
                            abstract_sections = abstract_element.findall(".//AbstractText")
                            for section in abstract_sections:
                                label = section.get('Label')
                                text = section.text or ''
                                if label:
                                    abstract_text += f"{label}: {text}\n"
                                else:
                                    abstract_text += f"{text}\n"
                        
                        # Get other metadata from summary
                        article_data = summary_data['result'][pmid]
                        
                        article = {
                            'pmid': pmid,
                            'title': article_data.get('title', ''),
                            'authors': [author.get('name', '') for author in article_data.get('authors', [])],
                            'journal': article_data.get('source', ''),
                            'date': article_data.get('pubdate', ''),
                            'publication_types': article_data.get('pubtype', []),
                            'keywords': article_data.get('keywords', []),
                            'abstract': abstract_text.strip(),
                            'doi': next((id_obj.get('value') for id_obj in article_data.get('articleids', []) 
                                       if id_obj.get('idtype') == 'doi'), None)
                        }
                        
                        articles.append(article)
                    
                    except Exception as e:
                        print(f"Error processing article {pmid}: {str(e)}")
                        continue

                return articles
                
        except Exception as e:
            print(f"Error searching articles: {str(e)}")
            return []