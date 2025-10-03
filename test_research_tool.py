"""
Test suite for the research tool components.
Tests basic functionality without requiring API keys.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from web_scraper import WebScraper
from vector_db import VectorDatabase


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = WebScraper()
    
    def test_initialization(self):
        """Test scraper initialization."""
        self.assertIsNotNone(self.scraper)
        self.assertEqual(self.scraper.timeout, 10)
        self.assertIn('User-Agent', self.scraper.headers)
    
    @patch('web_scraper.requests.get')
    def test_scrape_url_success(self, mock_get):
        """Test successful URL scraping."""
        # Mock response
        mock_response = Mock()
        mock_response.text = '<html><head><title>Test Page</title></head><body><p>Test content</p></body></html>'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test scraping
        result = self.scraper.scrape_url('https://example.com')
        
        # Assertions
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['title'], 'Test Page')
        self.assertIn('Test content', result['content'])
    
    @patch('web_scraper.requests.get')
    def test_scrape_url_error(self, mock_get):
        """Test error handling in URL scraping."""
        # Mock exception
        mock_get.side_effect = Exception('Connection error')
        
        # Test scraping
        result = self.scraper.scrape_url('https://example.com')
        
        # Assertions
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['title'], 'Error')
        self.assertIn('Failed to scrape', result['content'])


class TestVectorDatabase(unittest.TestCase):
    """Test cases for VectorDatabase class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.db = VectorDatabase(collection_name="test_collection")
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.db.reset_collection()
        except:
            pass
    
    def test_initialization(self):
        """Test database initialization."""
        self.assertIsNotNone(self.db)
        self.assertIsNotNone(self.db.collection)
        self.assertEqual(self.db.collection_name, "test_collection")
    
    def test_add_documents(self):
        """Test adding documents to the database."""
        documents = [
            {
                'url': 'https://example.com',
                'title': 'Test Document',
                'content': 'This is test content'
            }
        ]
        
        # Should not raise an exception
        self.db.add_documents(documents)
        
        # Verify document was added
        all_docs = self.db.get_all_documents()
        self.assertGreater(len(all_docs['ids']), 0)
    
    def test_search(self):
        """Test searching documents in the database."""
        # Add test documents
        documents = [
            {
                'url': 'https://example1.com',
                'title': 'AI Article',
                'content': 'This is about artificial intelligence'
            },
            {
                'url': 'https://example2.com',
                'title': 'ML Article',
                'content': 'This is about machine learning'
            }
        ]
        self.db.add_documents(documents)
        
        # Search
        results = self.db.search('artificial intelligence', n_results=1)
        
        # Assertions
        self.assertIsNotNone(results)
        self.assertIn('documents', results)


class TestResearchAgent(unittest.TestCase):
    """Test cases for ResearchAgent class (mock-based)."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('research_agent.OpenAI')
    def test_initialization(self, mock_openai):
        """Test agent initialization."""
        from research_agent import ResearchAgent
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock assistant creation
        mock_assistant = Mock()
        mock_assistant.id = 'test-assistant-id'
        mock_client.beta.assistants.create.return_value = mock_assistant
        
        # Initialize agent
        agent = ResearchAgent()
        
        # Assertions
        self.assertIsNotNone(agent)
        self.assertEqual(agent.api_key, 'test-key')
        mock_client.beta.assistants.create.assert_called_once()


if __name__ == '__main__':
    unittest.main()
