"""Editor Agent for reviewing and finalizing newsletter content."""
from typing import Dict, List
from crewai import Agent
import re
from datetime import datetime

class EditorAgent:
    @staticmethod
    def create(llm) -> Agent:
        return Agent(
            role='Newsletter Editor',
            goal='Review, refine, and ensure the quality of the newsletter content',
            backstory="""You are an experienced editor with expertise in technology 
            publications. You ensure content is accurate, engaging, well-structured, 
            and maintains a consistent style throughout. You are also responsible for 
            ensuring the content is up to date and relevant to the latest trends in the 
            technology industry. Include all the links to the sources in the content.""",
            tools=[],  # No additional tools needed for editing
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    @staticmethod
    def review_content(content: str) -> Dict[str, any]:
        """
        Review and improve newsletter content.
        
        Args:
            content: The draft newsletter content
            
        Returns:
            Dict containing:
            - improved_content: Edited content
            - suggestions: List of improvement suggestions
            - quality_score: Numerical score of content quality
        """
        suggestions = []
        quality_score = 0.0
        improved_content = content
        
        # Check for common issues
        if len(content) < 100:
            suggestions.append("Content is too short - needs more detail")
            quality_score -= 0.2
        
        # Check for proper markdown formatting
        if not re.search(r'#{1,6} ', content):
            suggestions.append("Missing section headers")
            quality_score -= 0.1
        
        if not re.search(r'\[.*?\]\(.*?\)', content):
            suggestions.append("Missing hyperlinks")
            quality_score -= 0.1
        
        # Check for proper spacing
        if re.search(r'\n{3,}', content):
            suggestions.append("Excessive blank lines - formatting needs cleanup")
            improved_content = re.sub(r'\n{3,}', '\n\n', improved_content)
            quality_score -= 0.1
        
        # Check for consistent header hierarchy
        headers = re.findall(r'^(#{1,6}) ', content, re.MULTILINE)
        if headers:
            header_levels = [len(h) for h in headers]
            if any(header_levels[i] - header_levels[i-1] > 1 for i in range(1, len(header_levels))):
                suggestions.append("Inconsistent header hierarchy")
                quality_score -= 0.1
        
        # Check for broken markdown links
        broken_links = re.findall(r'\[([^\]]+)\]\(\s*\)', content)
        if broken_links:
            suggestions.append(f"Found {len(broken_links)} broken link(s)")
            quality_score -= 0.1 * len(broken_links)
        
        # Check for proper list formatting
        lists = re.findall(r'^\s*[-*+]\s', content, re.MULTILINE)
        if lists and not re.search(r'^\s*[-*+]\s.*\n$', content, re.MULTILINE):
            suggestions.append("List items should end with newlines")
            quality_score -= 0.1
        
        # Base quality score starts at 1.0 and is reduced for issues
        quality_score = max(0.0, 1.0 + quality_score)
        
        # Add positive feedback if content meets criteria
        if quality_score > 0.8:
            suggestions.append("Content is well-structured and properly formatted")
        
        return {
            "improved_content": improved_content,
            "suggestions": suggestions,
            "quality_score": quality_score
        }

    @staticmethod
    def finalize_newsletter(
        content: str,
        metadata: Dict = None
    ) -> str:
        """
        Finalize the newsletter for publication.
        
        Args:
            content: The reviewed content
            metadata: Optional metadata to include
            
        Returns:
            Final markdown formatted newsletter
        """
        final_content = []
        
        # Add header with metadata
        final_content.append("# AI Technology Newsletter")
        final_content.append(f"*Issue Date: {datetime.now().strftime('%B %d, %Y')}*\n")
        
        if metadata:
            if metadata.get("topic"):
                final_content.append(f"**Focus Topic:** {metadata['topic']}\n")
            if metadata.get("summary"):
                final_content.append("## Executive Summary")
                final_content.append(f"{metadata['summary']}\n")
        
        # Add main content
        final_content.append(content)
        
        # Add footer
        final_content.append("\n---")
        final_content.append("*This newsletter is automatically generated using AI technology.*")
        final_content.append("*For more information, please contact us.*")
        
        return "\n".join(final_content) 