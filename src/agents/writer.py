"""Writer Agent for creating engaging newsletter content."""
from typing import Dict, List
from crewai import Agent
# import markdown
import re

class WriterAgent:
    @staticmethod
    def create(llm) -> Agent:
        return Agent(
            role='Content Writer',
            goal='Create engaging and informative newsletter content from research materials',
            backstory="""You are a skilled content writer specializing in technology 
            and AI topics. You excel at transforming complex information into clear, 
            engaging content that resonates with both technical and non-technical readers. 
            You are also responsible for ensuring the content is up to date and relevant to 
            the latest trends in the technology industry. Include all the links to the 
            sources in the content.""",
            tools=[],  # No additional tools needed for content writing
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    @staticmethod
    def create_section_content(
        section_title: str,
        research_data: Dict,
        style_guide: Dict = None
    ) -> str:
        """
        Create content for a newsletter section.
        
        Args:
            section_title: Title of the section
            research_data: Dictionary containing research information
            style_guide: Optional style guidelines
            
        Returns:
            Markdown formatted content for the section
        """
        content = []
        
        # Add section header
        content.append(f"## {section_title}\n")
        
        # Get section-specific data
        section_data = research_data.get("sections", {}).get(section_title, [])
        
        if section_title == "Latest News":
            content.extend(WriterAgent._format_news_section(section_data))
        elif section_title == "Community Discussions":
            content.extend(WriterAgent._format_community_section(section_data))
        elif section_title == "Social Media Insights":
            content.extend(WriterAgent._format_social_section(section_data))
        elif section_title == "Video Content":
            content.extend(WriterAgent._format_video_section(section_data))
        else:
            content.extend(WriterAgent._format_general_section(section_data))
        
        return "\n".join(content)

    @staticmethod
    def format_markdown(content: str) -> str:
        """
        Format content in proper markdown.
        
        Args:
            content: Raw content to format
            
        Returns:
            Properly formatted markdown content
        """
        # Clean up any double newlines
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # Ensure proper spacing around headers
        content = re.sub(r'(#{1,6} .+?)(?:\n(?!\n))', r'\1\n\n', content)
        
        # Ensure proper spacing around lists
        content = re.sub(r'(\n- .+?)(?:\n(?![\n-]))', r'\1\n', content)
        
        # Ensure proper spacing around blockquotes
        content = re.sub(r'(\n> .+?)(?:\n(?!\n))', r'\1\n\n', content)
        
        return content.strip()

    @staticmethod
    def _format_news_section(news_items: List[Dict]) -> List[str]:
        """Format news items into markdown content."""
        content = []
        for item in news_items:
            title = item.get("title", "").strip()
            description = item.get("description", "").strip()
            url = item.get("url", "").strip()
            date = item.get("date", "").strip()
            
            if title and url:
                content.append(f"### [{title}]({url})")
                if date:
                    content.append(f"*Published: {date}*")
                if description:
                    content.append(f"\n{description}\n")
        return content

    @staticmethod
    def _format_community_section(community_items: List[Dict]) -> List[str]:
        """Format community discussions into markdown content."""
        content = []
        for item in community_items:
            title = item.get("title", "").strip()
            text = item.get("text", "").strip()
            url = item.get("url", "").strip()
            author = item.get("author", "").strip()
            
            if title and url:
                content.append(f"### [{title}]({url})")
                if author:
                    content.append(f"*Posted by {author}*")
                if text:
                    # Truncate long text
                    if len(text) > 300:
                        text = text[:297] + "..."
                    content.append(f"\n{text}\n")
        return content

    @staticmethod
    def _format_social_section(social_items: List[Dict]) -> List[str]:
        """Format social media content into markdown content."""
        content = []
        for item in social_items:
            text = item.get("text", "").strip()
            url = item.get("url", "").strip()
            author = item.get("author", "").strip()
            
            if text:
                content.append(f"> {text}")
                if author:
                    content.append(f"*— {author}*")
                if url:
                    content.append(f"[View on Twitter]({url})\n")
        return content

    @staticmethod
    def _format_video_section(video_items: List[Dict]) -> List[str]:
        """Format video content into markdown content."""
        content = []
        for item in video_items:
            title = item.get("title", "").strip()
            description = item.get("description", "").strip()
            url = item.get("url", "").strip()
            channel = item.get("channel", "").strip()
            
            if title and url:
                content.append(f"### [{title}]({url})")
                if channel:
                    content.append(f"*By {channel}*")
                if description:
                    # Truncate long descriptions
                    if len(description) > 200:
                        description = description[:197] + "..."
                    content.append(f"\n{description}\n")
        return content

    @staticmethod
    def _format_general_section(items: List[Dict]) -> List[str]:
        """Format general content into markdown content."""
        content = []
        for item in items:
            title = item.get("title", "").strip()
            description = item.get("description", "").strip()
            url = item.get("url", "").strip()
            
            if title and url:
                content.append(f"### [{title}]({url})")
                if description:
                    content.append(f"\n{description}\n")
        return content 