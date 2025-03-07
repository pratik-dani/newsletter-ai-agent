from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from apify import Actor
from src.tools.base import RunApifyActor

class RedditScraperInput(BaseModel):
    """Input schema for RedditScraper tool."""
    searches: List[str] = Field(
        description="Here you can provide a search query which will be used to search Reddit's topics."
    )

    startUrls: Optional[List[str]] = Field(
        description="If you already have URL(s) of page(s) you wish to scrape, you can set them here. If you want to use the search field below, remove all startUrls here.",
        default=None
    )
    
    skipComments: Optional[bool] = Field(
        default=False,
        description="This will skip scrapping comments when going through posts"
    )
    
    skipUserPosts: Optional[bool] = Field(
        default=False,
        description="This will skip scrapping user posts when going through user activity"
    )
    
    skipCommunity: Optional[bool] = Field(
        default=False,
        description="This will skip scrapping community info but will still get community posts if they were not skipped."
    )
    
    
    searchPosts: Optional[bool] = Field(
        default=True,
        description="Will search for posts with the provided search"
    )
    
    searchComments: Optional[bool] = Field(
        default=False,
        description="Will search for comments with the provided search"
    )
    
    searchCommunities: Optional[bool] = Field(
        default=False,
        description="Will search for communities with the provided search"
    )
    
    searchUsers: Optional[bool] = Field(
        default=False,
        description="Will search for users with the provided search"
    )
    
    sort: Optional[Literal["relevance", "hot", "top", "new", "rising", "comments"]] = Field(
        default="new",
        description="Sort search by Relevance, Hot, Top, New or Comments"
    )
    
    time: Optional[Literal["all", "hour", "day", "week", "month", "year"]] = Field(
        default="month",
        description="Filter posts by last hour, week, day, month or year"
    )
    
    includeNSFW: Optional[bool] = Field(
        default=True,
        description="You can choose to include or exclude NSFW content from your search"
    )
    
    
    maxPostCount: Optional[int] = Field(
        default=10,
        description="The maximum number of posts that will be scraped for each Posts Page or Communities&Users URL"
    )
    
    postDateLimit: Optional[str] = Field(
        default=None,
        description="Use this value when you want to get only posts after a specific date"
    )
    
    maxComments: Optional[int] = Field(
        default=10,
        description="The maximum number of comments that will be scraped for each Comments Page. If you don't want to scrape comments you can set this to zero."
    )
    
    maxCommunitiesCount: Optional[int] = Field(
        default=2,
        description="The maximum number of Communities's pages that will be scraped if your search or startUrl is a Communities type."
    )
    
    maxUserCount: Optional[int] = Field(
        default=2,
        description="The maximum number of Users's pages that will be scraped."
    )
    
    scrollTimeout: Optional[int] = Field(
        default=40,
        description="Set the timeout in seconds in which the page will stop scrolling down to load new items"
    )
    
    debugMode: Optional[bool] = Field(
        default=False,
        description="Activate to see detailed logs"
    )

class RedditScraperTool(BaseTool):
    name: str = "Reddit Scraper"
    description: str = "Tool for scraping Reddit content with configurable parameters"
    args_schema: type[BaseModel] = RedditScraperInput
    actor: Actor = Field(description="Apify Actor instance")
    model_config = ConfigDict(arbitrary_types_allowed=True)
    def _run(
        self,
        searches: List[str],
        startUrls: Optional[List[str]] = None,
        skipComments: Optional[bool] = False,
        skipUserPosts: Optional[bool] = False,
        skipCommunity: Optional[bool] = False,
        searchPosts: Optional[bool] = True,
        searchComments: Optional[bool] = False,
        searchCommunities: Optional[bool] = False,
        searchUsers: Optional[bool] = False,
        sort: Optional[str] = "new",
        time: Optional[str] = None,
        includeNSFW: Optional[bool] = True,
        maxPostCount: Optional[int] = 20,
        postDateLimit: Optional[str] = None,
        maxComments: Optional[int] = 20,
        maxCommunitiesCount: Optional[int] = 2,
        maxUserCount: Optional[int] = 2,
        scrollTimeout: Optional[int] = 40,
        debugMode: Optional[bool] = False
    ) -> str:
        run_inputs = {}
        
        if startUrls:
            run_inputs["startUrls"] = startUrls
        if skipComments is not None:
            run_inputs["skipComments"] = skipComments
        if skipUserPosts is not None:
            run_inputs["skipUserPosts"] = skipUserPosts
        if skipCommunity is not None:
            run_inputs["skipCommunity"] = skipCommunity
        if searches:
            run_inputs["searches"] = searches
        if searchPosts is not None:
            run_inputs["searchPosts"] = searchPosts
        if searchComments is not None:
            run_inputs["searchComments"] = searchComments
        if searchCommunities is not None:
            run_inputs["searchCommunities"] = searchCommunities
        if searchUsers is not None:
            run_inputs["searchUsers"] = searchUsers
        if sort:
            run_inputs["sort"] = sort
        if time:
            run_inputs["time"] = time
        if includeNSFW is not None:
            run_inputs["includeNSFW"] = includeNSFW
        run_inputs["maxItems"] = 10
        if maxPostCount:
            run_inputs["maxPostCount"] = maxPostCount
        if postDateLimit:
            run_inputs["postDateLimit"] = postDateLimit
        if maxComments:
            run_inputs["maxComments"] = maxComments
        if maxCommunitiesCount:
            run_inputs["maxCommunitiesCount"] = maxCommunitiesCount
        if maxUserCount:
            run_inputs["maxUserCount"] = maxUserCount
        if scrollTimeout:
            run_inputs["scrollTimeout"] = scrollTimeout

        proxy = {
            "useApifyProxy": True,
            "apifyProxyGroups": [
                "RESIDENTIAL"
            ]
        }
        run_inputs["proxy"] = proxy
        
        run_actor = RunApifyActor(self.actor)
        dataset = run_actor._run("trudax/reddit-scraper-lite", run_inputs)
        return dataset