import requests
import time

def search_pubmed():
    """
    Basic PubMed search following Entrez guidelines
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': 'ketogenic diet',
        'retmax': 5,
        'retmode': 'json',
        'usehistory': 'y'  # This will give us a WebEnv and query_key for subsequent requests
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print("Search Results:")
        print(f"Total found: {data['esearchresult']['count']}")
        print("\nPaper IDs:")
        for pmid in data['esearchresult']['idlist']:
            print(f"PMID: {pmid}")
            
        # Also print WebEnv and query_key if we want to use them later
        print("\nSearch Session Info:")
        print(f"WebEnv: {data['esearchresult'].get('webenv', 'Not found')}")
        print(f"QueryKey: {data['esearchresult'].get('querykey', 'Not found')}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    search_pubmed()