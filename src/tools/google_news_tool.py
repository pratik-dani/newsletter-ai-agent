from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from apify import Actor
from src.tools.base import RunApifyActor

class GoogleNewsScraperInput(BaseModel):
    """Input schema for GoogleNewsScraper tool."""
    keywords: List[str] = Field(
        description="The keywords used to search for news articles"
    )


    maxItems: Optional[int] = Field(
        description="Set the maximum number of items you want to scrape for each keyword. If left unset, the actor will extract all available news.",
        default=20
    )

class GoogleNewsScraperTool(BaseTool):
    name: str = "Google News Scraper"
    description: str = "Tool for scraping Google News articles with configurable parameters"
    args_schema: type[BaseModel] = GoogleNewsScraperInput
    actor: Actor = Field(description="Apify Actor instance")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _run(
        self,
        keywords: List[str],
        language: Optional[str] = "US:en",
        maxItems: Optional[int] = None
    ) -> str:
        run_inputs = {
            "keywords": keywords,
            "language": language
        }
        
        if maxItems:
            run_inputs["maxItems"] = maxItems

        proxy = {
            "useApifyProxy": True,
            "apifyProxyGroups": [
                "RESIDENTIAL"
            ]
        }
        run_inputs["proxy"] = proxy
        
        run_actor = RunApifyActor(self.actor)
        dataset = run_actor._run("aymorato/super-fast-google-news-scraper-pay-per-result", run_inputs)
        return dataset