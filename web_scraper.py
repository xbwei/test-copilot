"""
Web scraper module for extracting content from websites.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import time


class WebScraper:
    """Scrapes web content from given URLs."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the web scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        """
        Scrape content from a single URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing url, title, and content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else url
            
            # Extract text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'title': title,
                'content': text[:10000]  # Limit content size
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'title': 'Error',
                'content': f'Failed to scrape: {str(e)}'
            }
    
    def scrape_urls(self, urls: List[str], delay: float = 1.0) -> List[Dict[str, str]]:
        """
        Scrape content from multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of dictionaries containing scraped content
        """
        results = []
        for i, url in enumerate(urls):
            print(f"Scraping {i+1}/{len(urls)}: {url}")
            result = self.scrape_url(url)
            results.append(result)
            
            if i < len(urls) - 1:
                time.sleep(delay)
        
        return results
