# Usage Guide

## Overview

This data science research tool provides three ways to use it:

1. **Demo Mode** - See how the tool architecture works
2. **Example Mode** - Run with pre-configured examples  
3. **Interactive Mode** - Provide your own research queries

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key** (for modes 2 and 3):
   ```bash
   cp .env.example .env
   # Edit .env and add your API key: OPENAI_API_KEY=sk-...
   ```

## Mode 1: Architecture Demo

View how the components work together without API calls:

```bash
python demo.py
```

**Output:**
- Shows the 3-step workflow
- Demonstrates web scraping setup
- Shows vector database integration
- Displays mock summary generation

**Use when:**
- Learning about the architecture
- No API key available
- Testing the installation

## Mode 2: Example Mode

Run with pre-configured Wikipedia examples:

```bash
python main.py
```

**What it does:**
- Researches AI and Machine Learning topics
- Scrapes content from Wikipedia
- Stores in vector database
- Generates real summary using GPT-4

**Requirements:**
- Valid OpenAI API key in .env
- Internet connection

**Example output:**
```
STEP 1: Scraping websites...
Scraping 1/2: https://en.wikipedia.org/wiki/Artificial_intelligence
Scraping 2/2: https://en.wikipedia.org/wiki/Machine_learning

STEP 2: Storing content in vector database...
Added 2 documents to the database

STEP 3: Generating summary with OpenAI Agent...
Created assistant: asst_xxxxx

RESEARCH SUMMARY
================================================================
[AI-generated comprehensive summary based on the content]
```

## Mode 3: Interactive Mode

Provide your own research query and URLs:

```bash
python cli.py
```

**Workflow:**

1. **Enter research query:**
   ```
   Enter your research query:
   > What are the latest trends in cloud computing?
   ```

2. **Enter URLs (one per line, empty line to finish):**
   ```
   Enter URLs to research (one per line, empty line to finish):
   > https://aws.amazon.com/blogs/aws/
   > https://cloud.google.com/blog/
   > https://azure.microsoft.com/en-us/blog/
   >
   ```

3. **View results:**
   - See scraping progress
   - Database storage confirmation
   - AI-generated summary

**Requirements:**
- Valid OpenAI API key in .env
- Internet connection
- Valid URLs that can be scraped

## Programmatic Usage

Use the tool in your own Python scripts:

```python
from main import ResearchTool

# Initialize
tool = ResearchTool()

# Define research parameters
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
query = "What are the main themes in these articles?"

# Perform research
try:
    summary = tool.research_websites(urls, query)
    print(summary)
finally:
    tool.cleanup()
```

### Using Individual Components

**Web Scraper:**
```python
from web_scraper import WebScraper

scraper = WebScraper()
content = scraper.scrape_url("https://example.com")
print(content['title'])
print(content['content'])
```

**Vector Database:**
```python
from vector_db import VectorDatabase

db = VectorDatabase(collection_name="my_research")
db.add_documents([
    {
        'url': 'https://example.com',
        'title': 'Example',
        'content': 'Content here'
    }
])

results = db.search("my query", n_results=5)
print(results)
```

**Research Agent:**
```python
import os
from research_agent import ResearchAgent

os.environ['OPENAI_API_KEY'] = 'your-key'
agent = ResearchAgent()

summary = agent.generate_summary(
    content="Your content here",
    user_query="What are the key points?"
)
print(summary)

agent.cleanup()
```

## Tips

1. **API Costs**: The tool uses GPT-4 Turbo which has associated costs. Monitor your OpenAI usage.

2. **Rate Limits**: If scraping many URLs, the tool includes a delay between requests to respect rate limits.

3. **Content Length**: Web scraper limits content to 10,000 characters per page to manage token usage.

4. **Error Handling**: The tool handles common errors like network issues and invalid URLs.

5. **Clean URLs**: For best results, use URLs that contain substantial text content (articles, blogs, documentation).

## Troubleshooting

### "OpenAI API key not found"
- Ensure .env file exists and contains `OPENAI_API_KEY=your-key`
- Check that the .env file is in the project root directory
- Verify the API key is valid

### "Failed to scrape"
- Check if the URL is accessible
- Verify you have internet connection
- Some sites may block scraping - try different URLs

### ChromaDB errors
- Ensure chromadb is installed: `pip install chromadb`
- Clear existing collections if needed
- Check for port conflicts if running locally

### Import errors
- Install all dependencies: `pip install -r requirements.txt`
- Use Python 3.8 or higher
- Activate your virtual environment if using one

## Next Steps

1. Try the demo mode first to understand the workflow
2. Run example mode with the provided Wikipedia URLs
3. Experiment with interactive mode using your own URLs
4. Integrate the tool into your own projects

For more information, see [README.md](README.md).
