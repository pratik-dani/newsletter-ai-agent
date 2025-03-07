from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from apify import Actor
from src.tools.base import RunApifyActor

class GoogleScraperInput(BaseModel):
    """Input schema for GoogleScraper tool."""
    queries: List[str] = Field(
        description="Search terms or Google Search URLs. Can use advanced techniques like 'AI site:twitter.com'. Limit 32 words per query."
    )

    resultsPerPage: Optional[int] = Field(
        description="Number of results to return per page",
        default=10
    )

    languageCode: Optional[str] = Field(
        default="en",
        description="Language for search results (passed as hl parameter)"
    )
    
    forceExactMatch: Optional[bool] = Field(
        default=False,
        description="Wrap query in quotes for exact phrase matching"
    )
    
    site: Optional[str] = Field(
        default=None,
        description="Limit search to specific site (e.g. site:example.com)"
    )
    
    relatedToSite: Optional[str] = Field(
        default=None,
        description="Filter pages related to specific site (e.g. related:example.com)"
    )
    
    wordsInTitle: Optional[List[str]] = Field(
        default=[],
        description="Filter pages with specific words in title using intitle: operator"
    )
    
    wordsInText: Optional[List[str]] = Field(
        default=[],
        description="Filter pages with specific words in text using intext: operator"
    )
    
    wordsInUrl: Optional[List[str]] = Field(
        default=[],
        description="Filter pages with specific words in URL using inurl: operator"
    )
    
    quickDateRange: Optional[str] = Field(
        default="d30",
        description="Filter by date range (e.g. d10, w2, m6, y1)"
    )
    
    beforeDate: Optional[str] = Field(
        default=None,
        description="Filter results before date using before: operator (YYYY-MM-DD)"
    )
    
    afterDate: Optional[str] = Field(
        default=None,
        description="Filter results after date using after: operator (YYYY-MM-DD)"
    )
    
    fileTypes: Optional[List[str]] = Field(
        default=[],
        description="Filter by file types using filetype: operator"
    )
    
    mobileResults: Optional[bool] = Field(
        default=False,
        description="Return mobile version of search results instead of desktop"
    )
    
    includeUnfilteredResults: Optional[bool] = Field(
        default=False,
        description="Include lower quality results normally filtered by Google"
    )

class GoogleScraperTool(BaseTool):
    name: str = "Google Scraper"
    description: str = "Tool for scraping Google search results with configurable parameters"
    args_schema: type[BaseModel] = GoogleScraperInput
    actor: Actor = Field(description="Apify Actor instance")
    model_config = ConfigDict(arbitrary_types_allowed=True)
    def _run(
        self,
        queries: List[str],
        resultsPerPage: Optional[int] = 10,
        languageCode: Optional[str] = "en",
        forceExactMatch: Optional[bool] = False,
        site: Optional[str] = None,
        relatedToSite: Optional[str] = None,
        wordsInTitle: Optional[List[str]] = [],
        wordsInText: Optional[List[str]] = [],
        wordsInUrl: Optional[List[str]] = [],
        quickDateRange: Optional[str] = None,
        beforeDate: Optional[str] = None,
        afterDate: Optional[str] = None,
        fileTypes: Optional[List[str]] = [],
        mobileResults: Optional[bool] = False,
        includeUnfilteredResults: Optional[bool] = False
    ) -> str:
        run_inputs = {
            "queries": "\n".join(queries)
        }
        
        if resultsPerPage:
            run_inputs["resultsPerPage"] = resultsPerPage
        run_inputs["maxPagesPerQuery"] = 1
        if languageCode:
            run_inputs["languageCode"] = languageCode
        if forceExactMatch:
            run_inputs["forceExactMatch"] = forceExactMatch
        if site:
            run_inputs["site"] = site
        if relatedToSite:
            run_inputs["relatedToSite"] = relatedToSite
        if wordsInTitle:
            run_inputs["wordsInTitle"] = wordsInTitle
        if wordsInText:
            run_inputs["wordsInText"] = wordsInText
        if wordsInUrl:
            run_inputs["wordsInUrl"] = wordsInUrl
        if quickDateRange:
            run_inputs["quickDateRange"] = quickDateRange
        if beforeDate:
            run_inputs["beforeDate"] = beforeDate
        if afterDate:
            run_inputs["afterDate"] = afterDate
        if fileTypes:
            run_inputs["fileTypes"] = fileTypes
        if mobileResults:
            run_inputs["mobileResults"] = mobileResults
        if includeUnfilteredResults:
            run_inputs["includeUnfilteredResults"] = includeUnfilteredResults
            
        run_actor = RunApifyActor(self.actor)
        dataset = run_actor._run("apify/google-search-scraper", run_inputs)
        return dataset
