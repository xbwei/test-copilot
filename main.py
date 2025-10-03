"""
Main application for the data science research tool.
Researches websites, stores content in vector database, and generates summaries.
"""
import os
import sys
from typing import List
from dotenv import load_dotenv

from web_scraper import WebScraper
from vector_db import VectorDatabase
from research_agent import ResearchAgent


class ResearchTool:
    """Main research tool that coordinates web scraping, storage, and summarization."""
    
    def __init__(self):
        """Initialize the research tool."""
        load_dotenv()
        
        self.scraper = WebScraper()
        self.vector_db = VectorDatabase()
        self.agent = ResearchAgent()
    
    def research_websites(self, urls: List[str], query: str) -> str:
        """
        Research websites and generate a summary.
        
        Args:
            urls: List of URLs to research
            query: Research query/question
            
        Returns:
            Generated summary
        """
        print("\n" + "="*60)
        print("STEP 1: Scraping websites...")
        print("="*60)
        documents = self.scraper.scrape_urls(urls)
        
        print("\n" + "="*60)
        print("STEP 2: Storing content in vector database...")
        print("="*60)
        self.vector_db.add_documents(documents)
        
        print("\n" + "="*60)
        print("STEP 3: Generating summary with OpenAI Agent...")
        print("="*60)
        summary = self.agent.generate_summary_from_documents(documents, query)
        
        return summary
    
    def cleanup(self):
        """Clean up resources."""
        self.agent.cleanup()


def main():
    """Main entry point for the application."""
    print("="*60)
    print("Data Science Research Tool")
    print("Powered by OpenAI Agent API")
    print("="*60)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\nERROR: OPENAI_API_KEY environment variable not set!")
        print("Please create a .env file with your OpenAI API key.")
        print("See .env.example for reference.")
        return
    
    # Example usage
    print("\n[Demo Mode] Using example URLs and query...")
    
    # Example URLs and query
    example_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning"
    ]
    example_query = "What are the key concepts in AI and machine learning?"
    
    print(f"\nResearch Query: {example_query}")
    print(f"URLs to research: {', '.join(example_urls)}\n")
    
    # Create research tool
    tool = ResearchTool()
    
    try:
        # Perform research
        summary = tool.research_websites(example_urls, example_query)
        
        print("\n" + "="*60)
        print("RESEARCH SUMMARY")
        print("="*60)
        print(summary)
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\nError during research: {str(e)}")
    finally:
        # Clean up
        tool.cleanup()


if __name__ == "__main__":
    main()
