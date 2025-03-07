"""Researcher Agent for gathering information about specified topics."""
from typing import List, Dict
from crewai import Agent
from src.tools import GoogleScraperTool, RedditScraperTool, TwitterScraperTool, YouTubeScraperTool, GoogleNewsScraperTool

class ResearcherAgent:
    @staticmethod
    def create(llm, actor) -> Agent:
        return Agent(
            role='Research Specialist',
            goal='Gather comprehensive and accurate information about specified topics',
            backstory="""You are an expert research specialist with a keen eye for detail 
            and the ability to find the most relevant and up-to-date information. You 
            specialize in AI technology, industry trends, and market analysis.""",
            tools=[
                GoogleScraperTool(actor=actor),
                RedditScraperTool(actor=actor),
                TwitterScraperTool(actor=actor),
                YouTubeScraperTool(actor=actor),
                GoogleNewsScraperTool(actor=actor)
            ],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    @staticmethod
    def research_topic(topic: str, actor) -> Dict:
        """
        Research a specific topic and return structured information.
        
        Args:
            topic: The topic to research
            actor: Apify Actor instance
            
        Returns:
            Dict containing research results with keys:
            - summary: Brief overview
            - key_points: List of main points
            - sources: List of reference URLs
        """
        results = {
            "summary": "",
            "key_points": [],
            "sources": [],
            "sections": {}
        }
        
        # Initialize tools
        google_tool = GoogleScraperTool(actor=actor)
        reddit_tool = RedditScraperTool(actor=actor)
        twitter_tool = TwitterScraperTool(actor=actor)
        youtube_tool = YouTubeScraperTool(actor=actor)
        news_tool = GoogleNewsScraperTool(actor=actor)
        
        # Search parameters
        search_params = {
            "queries": [topic],
            "resultsPerPage": 5,
            "maxPagesPerQuery": 2,
            "languageCode": "en",
            "quickDateRange": "m1"  # Last month
        }
        
        try:
            # Get latest news and articles
            news_results = news_tool._run(**search_params)
            if isinstance(news_results, list):
                results["sections"]["Latest News"] = news_results
                results["sources"].extend([item.get("url") for item in news_results if item.get("url")])
            
            # Get general web results
            web_results = google_tool._run(**search_params)
            if isinstance(web_results, list):
                results["sections"]["General Information"] = web_results
                results["sources"].extend([item.get("url") for item in web_results if item.get("url")])
            
            # Get community discussions
            reddit_results = reddit_tool._run(
                subreddits=["artificial", "MachineLearning", "AINews"],
                searchType="relevance",
                searchQuery=topic,
                maxItems=10
            )
            if isinstance(reddit_results, list):
                results["sections"]["Community Discussions"] = reddit_results
                results["sources"].extend([item.get("url") for item in reddit_results if item.get("url")])
            
            # Get social media insights
            twitter_results = twitter_tool._run(
                searchTerms=[topic],
                maxItems=10,
                sortBy="relevance"
            )
            if isinstance(twitter_results, list):
                results["sections"]["Social Media Insights"] = twitter_results
            
            # Get video content
            youtube_results = youtube_tool._run(
                searchTerms=[topic],
                maxItems=5,
                sortBy="relevance"
            )
            if isinstance(youtube_results, list):
                results["sections"]["Video Content"] = youtube_results
                results["sources"].extend([item.get("url") for item in youtube_results if item.get("url")])
            
            # Extract key points from all sources
            all_content = []
            for section_results in results["sections"].values():
                if isinstance(section_results, list):
                    for item in section_results:
                        if isinstance(item, dict):
                            content = item.get("title", "") + " " + item.get("description", "")
                            if content.strip():
                                all_content.append(content)
            
            # Create summary and key points
            results["summary"] = "\n".join(all_content[:3])  # First 3 items for summary
            results["key_points"] = [content for content in all_content[3:10]]  # Next 7 items for key points
            
            # Remove duplicates from sources
            results["sources"] = list(set(results["sources"]))
            
        except Exception as e:
            print(f"Error during research: {str(e)}")
            
        return results 