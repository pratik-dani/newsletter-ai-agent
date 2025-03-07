"""Configuration settings for the newsletter agent system."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Configurations
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Newsletter Configuration
DEFAULT_NEWSLETTER_SECTIONS = [
    "Latest News",
    "Industry Updates",
    "Tools & Frameworks",
    "Companies & Startups",
    "Research & Development",
    "Community Discussions",
    "Video Content",
    "Podcasts",
]

# Agent Configuration
MAX_RETRIES = 3
TEMPERATURE = 0.7
MODEL_NAME = "gemini-pro"  # Google's Gemini Pro model 