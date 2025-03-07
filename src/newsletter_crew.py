"""Newsletter Crew that coordinates the agents to generate the newsletter."""
from typing import Dict, List
from crewai import Crew, Task, LLM
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.agents.editor import EditorAgent
from src.config.config import DEFAULT_NEWSLETTER_SECTIONS
import os

class NewsletterCrew:
    def __init__(self, actor):
        # Initialize agents
        self.llm = LLM(
            model="gemini/gemini-2.0-flash-lite",
            temperature=0.7,
            api_key=os.getenv("GOOGLE_API_KEY"),  # Make sure to set this in your .env file
            verbose=False  # Suppress LLM output
        )
        self.actor = actor
        self.researcher = ResearcherAgent.create(self.llm, self.actor)
        self.writer = WriterAgent.create(self.llm)
        self.editor = EditorAgent.create(self.llm)
        
        # Create the crew
        self.crew = Crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[],
            verbose=True
        )

    def generate_newsletter(self, topic: str) -> str:
        """
        Generate a complete newsletter about the given topic.
        
        Args:
            topic: The main topic for the newsletter
            
        Returns:
            Markdown formatted newsletter content
        """
        self.actor.log.info(f"Generating newsletter for topic: {topic}")
        tasks = []
        
        # Research task
        research_task = Task(
            description=f"Research comprehensive information about {topic}. Focus on latest news, developments, and trends.",
            expected_output="""A detailed research report containing:
            1. Latest news and developments
            2. Key industry trends
            3. Important companies and platforms
            4. Community discussions and social media insights
            5. Relevant video content
            Format: JSON with sections for each category""",
            agent=self.researcher
        )
        tasks.append(research_task)
        
        # Writing task
        writing_task = Task(
            description="Transform the research data into engaging newsletter sections",
            expected_output=f"""A well-structured newsletter draft with:
            1. Clear section headers
            2. Engaging content for each section
            3. Proper markdown formatting
            4. Links to sources
            Format: Markdown with proper headers and formatting
            Use the research to create content for sections: {', '.join(DEFAULT_NEWSLETTER_SECTIONS)}""",
            agent=self.writer,
        )
        tasks.append(writing_task)
        
        # Editing task
        editing_task = Task(
            description="Review, improve, and finalize the newsletter content",
            expected_output="""A polished newsletter with:
            1. Professional formatting
            2. Consistent style
            3. Error-free content
            4. Proper metadata and structure
            5. All the links to the sources in the content
            Format: Final markdown document ready for distribution""",
            agent=self.editor
        )
        tasks.append(editing_task)
        
        # Update crew tasks
        self.crew.tasks = tasks
        
        try:
            # Execute the tasks
            result = self.crew.kickoff()
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.actor.log.error(f"Error in newsletter generation: {str(e)}")
            raise

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate a newsletter.
        
        Args:
            user_input: User's request/requirements for the newsletter
            
        Returns:
            Generated newsletter in markdown format
        """
        # For now, we'll just pass the input directly to generate_newsletter
        # In the future, we can add more preprocessing and parameter extraction
        return self.generate_newsletter(user_input) 