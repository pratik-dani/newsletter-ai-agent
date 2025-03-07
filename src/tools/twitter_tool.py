from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from apify import Actor
from src.tools.base import RunApifyActor

class TwitterScraperInput(BaseModel):
    """Input schema for TwitterScraper tool."""
    searchTerms: Optional[List[str]] = Field(
        description="Search terms to find tweets containing these terms. Alternative to using Twitter URLs.",
        default=None
    )

    sort: Optional[str] = Field(
        description="How to sort the returned tweets. Setting to 'Latest' yields more results.",
        default="Top",
        enum=["Top", "Latest"]
    )

    start: Optional[str] = Field(
        description="Scrape tweets starting from this date (format: YYYY-MM-DD)",
        default=None
    )

    end: Optional[str] = Field(
        description="Scrape tweets until this date (format: YYYY-MM-DD)", 
        default=None
    )

class TwitterScraperTool(BaseTool):
    name: str = "Twitter Scraper"
    description: str = "Tool for scraping Twitter content with configurable parameters"
    args_schema: type[BaseModel] = TwitterScraperInput
    actor: Actor = Field(description="Apify Actor instance")
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _run(
        self,
        searchTerms: Optional[List[str]] = None,
        sort: Optional[str] = "latest",
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> str:
        run_inputs = {}
        
        if searchTerms:
            run_inputs["searchTerms"] = searchTerms
        if sort:
            run_inputs["sort"] = sort
        run_inputs["maxItems"] = 5
        if start:
            run_inputs["start"] = start
        if end:
            run_inputs["end"] = end

        run_actor = RunApifyActor(self.actor)
        dataset = run_actor._run("apidojo/twitter-scraper-lite", run_inputs)
        return dataset


# from crewai.tools import BaseTool
# from pydantic import BaseModel, Field, ConfigDict
# from typing import List, Optional, Literal
# from apify import Actor
# from src.tools.base import RunApifyActor

# class TwitterScraperInput(BaseModel):
#     """Input schema for TwitterScraper tool."""
#     searchTerms: List[str] = Field(
#         description="Search terms you want to search from Twitter (X). You can refer to https://github.com/igorbrigadir/twitter-advanced-search."
#     )

#     startUrls: Optional[List[str]] = Field(
#         description="Twitter (X) URLs. Paste the URLs and get the results immediately. Tweet, Profile, Search or List URLs are supported.",
#         default=None
#     )    
    
#     twitterHandles: Optional[List[str]] = Field(
#         description="Twitter handles that you want to search on Twitter (X)",
#         default=None
#     )
    
#     conversationIds: Optional[List[str]] = Field(
#         description="Conversation IDs that you want to search on Twitter (X)",
#         default=None
#     )
    
#     maxItems: Optional[int] = Field(
#         description="Maximum number of items that you want as output.",
#         default=None
#     )
    
#     sort: Optional[Literal["Top", "Latest"]] = Field(
#         description="Sorts search results by the given option. Only works with search terms and search URLs.",
#         default=None
#     )
    
#     tweetLanguage: Optional[str] = Field(
#         default="en",
#         description="Restricts tweets to the given language, given by an ISO 639-1 code."
#     )
    
#     onlyVerifiedUsers: Optional[bool] = Field(
#         description="If selected, only returns tweets by users who are verified.",
#         default=None
#     )
    
#     onlyTwitterBlue: Optional[bool] = Field(
#         description="If selected, only returns tweets by users who are Twitter Blue subscribers.",
#         default=None
#     )
    
#     onlyImage: Optional[bool] = Field(
#         description="If selected, only returns tweets that contain images.",
#         default=None
#     )
    
#     onlyVideo: Optional[bool] = Field(
#         description="If selected, only returns tweets that contain videos.",
#         default=None
#     )
    
#     onlyQuote: Optional[bool] = Field(
#         description="If selected, only returns tweets that are quotes.",
#         default=None
#     )
    
#     author: Optional[str] = Field(
#         description="Returns tweets sent by the given user. It should be a Twitter (X) Handle.",
#         default=None
#     )
    
#     inReplyTo: Optional[str] = Field(
#         description="Returns tweets that are replies to the given user. It should be a Twitter (X) Handle.",
#         default=None
#     )
    
#     mentioning: Optional[str] = Field(
#         description="Returns tweets mentioning the given user. It should be a Twitter (X) Handle.",
#         default=None
#     )
    
#     geotaggedNear: Optional[str] = Field(
#         description="Returns tweets sent near the given location.",
#         default=None
#     )
    
#     withinRadius: Optional[str] = Field(
#         description="Returns tweets sent within the given radius of the given location.",
#         default=None
#     )
    
#     geocode: Optional[str] = Field(
#         description="Returns tweets sent by users located within a given radius of the given latitude/longitude.",
#         default=None
#     )
    
#     placeObjectId: Optional[str] = Field(
#         description="Returns tweets tagged with the given place.",
#         default=None
#     )
    
#     minimumRetweets: Optional[int] = Field(
#         description="Returns tweets with at least the given number of retweets.",
#         default=None
#     )
    
#     minimumFavorites: Optional[int] = Field(
#         description="Returns tweets with at least the given number of favorites.",
#         default=None
#     )
    
#     minimumReplies: Optional[int] = Field(
#         description="Returns tweets with at least the given number of replies.",
#         default=None
#     )
    
#     start: Optional[str] = Field(
#         description="Returns tweets sent after the given date.",
#         default=None
#     )
    
#     end: Optional[str] = Field(
#         description="Returns tweets sent before the given date.",
#         default=None
#     )
    
#     includeSearchTerms: Optional[bool] = Field(
#         description="If selected, a field will be added to each tweets about the search term that was used to find it.",
#         default=None
#     )

# class TwitterScraperTool(BaseTool):
#     name: str = "Twitter Scraper"
#     description: str = "Tool for scraping Twitter (X) content with configurable parameters"
#     args_schema: type[BaseModel] = TwitterScraperInput
#     actor: Actor = Field(description="Apify Actor instance")
#     model_config = ConfigDict(arbitrary_types_allowed=True)
#     def _run(
#         self,
#         searchTerms: List[str],
#         startUrls: Optional[List[str]] = None,
#         twitterHandles: Optional[List[str]] = None,
#         conversationIds: Optional[List[str]] = None,
#         maxItems: Optional[int] = None,
#         sort: Optional[str] = None,
#         tweetLanguage: Optional[str] = "en",
#         onlyVerifiedUsers: Optional[bool] = None,
#         onlyTwitterBlue: Optional[bool] = None,
#         onlyImage: Optional[bool] = None,
#         onlyVideo: Optional[bool] = None,
#         onlyQuote: Optional[bool] = None,
#         author: Optional[str] = None,
#         inReplyTo: Optional[str] = None,
#         mentioning: Optional[str] = None,
#         geotaggedNear: Optional[str] = None,
#         withinRadius: Optional[str] = None,
#         geocode: Optional[str] = None,
#         placeObjectId: Optional[str] = None,
#         minimumRetweets: Optional[int] = None,
#         minimumFavorites: Optional[int] = None,
#         minimumReplies: Optional[int] = None,
#         start: Optional[str] = None,
#         end: Optional[str] = None,
#         includeSearchTerms: Optional[bool] = None
#     ) -> str:
#         run_inputs = {}
        
#         if startUrls:
#             run_inputs["startUrls"] = startUrls
#         if searchTerms:
#             run_inputs["searchTerms"] = searchTerms
#         if twitterHandles:
#             run_inputs["twitterHandles"] = twitterHandles
#         if conversationIds:
#             run_inputs["conversationIds"] = conversationIds
#         if maxItems:
#             run_inputs["maxItems"] = maxItems
#         if sort:
#             run_inputs["sort"] = sort
#         if tweetLanguage:
#             run_inputs["tweetLanguage"] = tweetLanguage
#         if onlyVerifiedUsers:
#             run_inputs["onlyVerifiedUsers"] = onlyVerifiedUsers
#         if onlyTwitterBlue:
#             run_inputs["onlyTwitterBlue"] = onlyTwitterBlue
#         if onlyImage:
#             run_inputs["onlyImage"] = onlyImage
#         if onlyVideo:
#             run_inputs["onlyVideo"] = onlyVideo
#         if onlyQuote:
#             run_inputs["onlyQuote"] = onlyQuote
#         if author:
#             run_inputs["author"] = author
#         if inReplyTo:
#             run_inputs["inReplyTo"] = inReplyTo
#         if mentioning:
#             run_inputs["mentioning"] = mentioning
#         if geotaggedNear:
#             run_inputs["geotaggedNear"] = geotaggedNear
#         if withinRadius:
#             run_inputs["withinRadius"] = withinRadius
#         if geocode:
#             run_inputs["geocode"] = geocode
#         if placeObjectId:
#             run_inputs["placeObjectId"] = placeObjectId
#         if minimumRetweets:
#             run_inputs["minimumRetweets"] = minimumRetweets
#         if minimumFavorites:
#             run_inputs["minimumFavorites"] = minimumFavorites
#         if minimumReplies:
#             run_inputs["minimumReplies"] = minimumReplies
#         if start:
#             run_inputs["start"] = start
#         if end:
#             run_inputs["end"] = end
#         if includeSearchTerms:
#             run_inputs["includeSearchTerms"] = includeSearchTerms

#         run_actor = RunApifyActor(self.actor)
#         dataset = run_actor._run("apidojo/tweet-scraper", run_inputs)
#         return dataset
