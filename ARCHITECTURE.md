# System Architecture

## Overview

The Data Science Research Tool is designed with a modular architecture that separates concerns and enables easy testing and maintenance.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   demo.py    │  │   main.py    │  │   cli.py     │        │
│  │              │  │              │  │              │        │
│  │ Architecture │  │   Example    │  │ Interactive  │        │
│  │     Demo     │  │     Mode     │  │     Mode     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CORE COMPONENTS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │  web_scraper.py    │  │   vector_db.py     │               │
│  ├────────────────────┤  ├────────────────────┤               │
│  │ - WebScraper       │  │ - VectorDatabase   │               │
│  │   • scrape_url()   │  │   • add_documents()│               │
│  │   • scrape_urls()  │  │   • search()       │               │
│  └────────────────────┘  └────────────────────┘               │
│           │                        │                            │
│           └────────────┬───────────┘                            │
│                        │                                        │
│                        ▼                                        │
│           ┌────────────────────────┐                           │
│           │  research_agent.py     │                           │
│           ├────────────────────────┤                           │
│           │ - ResearchAgent        │                           │
│           │   • generate_summary() │                           │
│           └────────────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Websites   │  │   ChromaDB   │  │  OpenAI API  │        │
│  │              │  │              │  │              │        │
│  │  HTTP/HTTPS  │  │   Vector     │  │   GPT-4      │        │
│  │   Content    │  │   Database   │  │  Assistants  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. INPUT PHASE
   User provides query + URLs
          │
          ▼
   ┌──────────────┐
   │  CLI/Main    │
   └──────────────┘

2. SCRAPING PHASE
   Extract web content
          │
          ▼
   ┌──────────────┐
   │ WebScraper   │ ──► HTTP Request ──► Website
   └──────────────┘ ◄── HTML Response ◄─┘
          │
          ▼
   Document Objects
   {url, title, content}

3. STORAGE PHASE
   Store in vector database
          │
          ▼
   ┌──────────────┐
   │ VectorDB     │ ──► Embeddings ──► ChromaDB
   └──────────────┘

4. ANALYSIS PHASE
   Generate summary
          │
          ▼
   ┌──────────────┐
   │ResearchAgent │ ──► API Call ──► OpenAI
   └──────────────┘ ◄── Summary ◄───┘
          │
          ▼
   Display to User
```

## Component Details

### WebScraper (`web_scraper.py`)

**Purpose**: Extract text content from websites

**Key Methods**:
- `scrape_url(url)`: Scrape single URL
- `scrape_urls(urls)`: Scrape multiple URLs with rate limiting

**Dependencies**: requests, beautifulsoup4

**Error Handling**: Returns error documents on failure

### VectorDatabase (`vector_db.py`)

**Purpose**: Store and retrieve document embeddings

**Key Methods**:
- `add_documents(documents)`: Store documents as vectors
- `search(query, n_results)`: Semantic search
- `reset_collection()`: Clear database

**Dependencies**: chromadb

**Features**: Automatic embedding generation, semantic search

### ResearchAgent (`research_agent.py`)

**Purpose**: Generate intelligent summaries using OpenAI

**Key Methods**:
- `generate_summary(content, query)`: Single document summary
- `generate_summary_from_documents(documents, query)`: Multi-source summary
- `cleanup()`: Delete assistant

**Dependencies**: openai

**Features**: GPT-4 Turbo, thread-based conversations, structured prompts

## Usage Patterns

### Pattern 1: Full Pipeline (main.py)
```python
tool = ResearchTool()
summary = tool.research_websites(urls, query)
tool.cleanup()
```

### Pattern 2: Component-by-Component
```python
# Scrape
scraper = WebScraper()
docs = scraper.scrape_urls(urls)

# Store
db = VectorDatabase()
db.add_documents(docs)

# Analyze
agent = ResearchAgent()
summary = agent.generate_summary_from_documents(docs, query)
agent.cleanup()
```

### Pattern 3: Interactive (cli.py)
```python
query, urls = get_user_input()
# ... process as in Pattern 2 ...
```

## Configuration

### Environment Variables (.env)
```
OPENAI_API_KEY=sk-...
```

### Dependencies (requirements.txt)
- Core: openai, chromadb, beautifulsoup4, requests
- Utils: python-dotenv

## Testing Strategy

### Unit Tests (`test_research_tool.py`)
- WebScraper: Mock HTTP requests
- VectorDatabase: Real ChromaDB operations
- ResearchAgent: Mock OpenAI API

### Integration Testing
- Use demo.py for end-to-end workflow validation
- Test with real websites in development

## Security Considerations

1. **API Keys**: Stored in .env (gitignored)
2. **Rate Limiting**: Delay between web requests
3. **Content Limits**: Cap scraped content size
4. **Error Handling**: Graceful degradation

## Scalability

### Current Limitations
- Single-threaded scraping
- In-memory ChromaDB
- Sequential processing

### Potential Improvements
- Async scraping with aiohttp
- Persistent ChromaDB with server mode
- Batch processing for large document sets
- Caching layer for repeated queries

## Monitoring & Debugging

### Logging Points
1. Scraping progress (per URL)
2. Database operations (add, search)
3. Agent creation and completion
4. Error conditions

### Debug Mode
Run demo.py to verify architecture without API costs

## Deployment Options

1. **Local Development**: Python + pip install
2. **Docker Container**: Package with dependencies
3. **Cloud Function**: Serverless deployment
4. **API Service**: Flask/FastAPI wrapper

---

For implementation details, see individual module documentation.
For usage instructions, see [USAGE.md](USAGE.md).
