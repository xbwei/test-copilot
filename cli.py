"""
Interactive CLI for the data science research tool.
"""
import os
import sys
from dotenv import load_dotenv

from web_scraper import WebScraper
from vector_db import VectorDatabase
from research_agent import ResearchAgent


def get_user_input():
    """Get research query and URLs from user input."""
    print("\n" + "="*60)
    print("Data Science Research Tool - Interactive Mode")
    print("="*60)
    
    # Get research query
    print("\nEnter your research query:")
    query = input("> ").strip()
    
    if not query:
        print("Error: Query cannot be empty")
        return None, None
    
    # Get URLs
    print("\nEnter URLs to research (one per line, empty line to finish):")
    urls = []
    while True:
        url = input("> ").strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("Error: At least one URL is required")
        return None, None
    
    return query, urls


def main():
    """Main entry point for interactive CLI."""
    load_dotenv()
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\nERROR: OPENAI_API_KEY environment variable not set!")
        print("Please create a .env file with your OpenAI API key.")
        print("See .env.example for reference.")
        return
    
    # Get user input
    query, urls = get_user_input()
    
    if not query or not urls:
        return
    
    print(f"\nStarting research on {len(urls)} URL(s)...")
    
    # Initialize components
    scraper = WebScraper()
    vector_db = VectorDatabase()
    agent = ResearchAgent()
    
    try:
        # Scrape websites
        print("\n" + "="*60)
        print("Scraping websites...")
        print("="*60)
        documents = scraper.scrape_urls(urls)
        
        # Store in vector database
        print("\n" + "="*60)
        print("Storing content in vector database...")
        print("="*60)
        vector_db.add_documents(documents)
        
        # Generate summary
        print("\n" + "="*60)
        print("Generating summary with OpenAI Agent...")
        print("="*60)
        summary = agent.generate_summary_from_documents(documents, query)
        
        # Display results
        print("\n" + "="*60)
        print("RESEARCH SUMMARY")
        print("="*60)
        print(f"\nQuery: {query}\n")
        print(summary)
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\nError during research: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        agent.cleanup()


if __name__ == "__main__":
    main()
