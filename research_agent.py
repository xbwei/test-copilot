"""
OpenAI Agent module for generating summaries using the Assistants API.
"""
import os
from openai import OpenAI
from typing import List, Dict, Optional
import time


class ResearchAgent:
    """OpenAI agent for analyzing and summarizing website content."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the research agent.
        
        Args:
            api_key: OpenAI API key (uses env var if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.assistant = None
        self._create_assistant()
    
    def _create_assistant(self):
        """Create an OpenAI assistant for research tasks."""
        self.assistant = self.client.beta.assistants.create(
            name="Research Assistant",
            instructions="""You are a research assistant that analyzes website content and generates comprehensive summaries.
            Your summaries should:
            1. Identify key themes and topics
            2. Extract important facts and data points
            3. Synthesize information from multiple sources
            4. Present findings in a clear, structured format
            5. Highlight connections and patterns across sources""",
            model="gpt-4-turbo-preview",
            tools=[]
        )
        print(f"Created assistant: {self.assistant.id}")
    
    def generate_summary(self, content: str, user_query: str) -> str:
        """
        Generate a summary of the provided content based on user query.
        
        Args:
            content: Content to summarize
            user_query: User's research query
            
        Returns:
            Generated summary
        """
        # Create a thread
        thread = self.client.beta.threads.create()
        
        # Create the message with user query and content
        prompt = f"""Based on the following research query: "{user_query}"

Please analyze and summarize the following content:

{content}

Provide a comprehensive summary that addresses the research query."""
        
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        
        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )
        
        # Wait for completion
        while run.status in ['queued', 'in_progress']:
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        if run.status == 'completed':
            # Retrieve messages
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            
            # Get the assistant's response
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
        
        return f"Error: Assistant run status is {run.status}"
    
    def generate_summary_from_documents(self, documents: List[Dict], user_query: str) -> str:
        """
        Generate a summary from multiple documents.
        
        Args:
            documents: List of document dictionaries with 'url', 'title', and 'content'
            user_query: User's research query
            
        Returns:
            Generated summary
        """
        # Combine content from all documents
        combined_content = "\n\n".join([
            f"Source: {doc['title']} ({doc['url']})\n{doc['content'][:2000]}"
            for doc in documents
        ])
        
        return self.generate_summary(combined_content, user_query)
    
    def cleanup(self):
        """Delete the assistant to clean up resources."""
        if self.assistant:
            self.client.beta.assistants.delete(self.assistant.id)
            print(f"Deleted assistant: {self.assistant.id}")
