"""This module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

import os
import asyncio
from apify import Actor
from dotenv import load_dotenv
from src.newsletter_crew import NewsletterCrew
from datetime import datetime

async def main() -> None:
    """
    Main entry point for the newsletter generation system.
    
    This coroutine handles the initialization of the system, processes user input,
    and generates the newsletter using the AI agent crew.
    """
    async with Actor as actor:
        try:
            actor.log.info('Initializing Newsletter Generation System...')
            
            # Load environment variables
            load_dotenv()
            
            # Check for required environment variables
            if not os.getenv("GOOGLE_API_KEY"):
                raise EnvironmentError(
                    "GOOGLE_API_KEY environment variable is required. "
                    "Please set it in your .env file."
                )
            
            # Get input from the actor
            actor_input = await actor.get_input() or {}
            user_input = actor_input.get('topic')
            
            # Use default topic if none provided
            if not user_input:
                user_input = (
                    "I want to know everything about AI agents – current news, "
                    "AI agentic platforms and frameworks, and companies in this field."
                )
                actor.log.info("No topic provided, using default topic")
            
            actor.log.info(f'Generating newsletter for topic: {user_input}')
            
            # Create the newsletter crew
            crew = NewsletterCrew(actor)
            
            # Generate the newsletter
            newsletter_content = crew.process_user_input(user_input)
            print(newsletter_content)
            # Check if the content indicates an error
            # if newsletter_content.startswith("# Error Generating Newsletter"):
            #     raise RuntimeError(newsletter_content)
            
            # Push the result to the actor's default dataset
            await actor.push_data({
                'topic': user_input,
                'content': newsletter_content,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            })
            
            actor.log.info('Newsletter generation completed successfully!')
            
        except Exception as e:
            error_msg = f'Error in newsletter generation: {str(e)}'
            actor.log.error(error_msg)
            
            # Push error information to the dataset
            await actor.push_data({
                'topic': user_input if 'user_input' in locals() else None,
                'error': error_msg,
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            })
            
            raise

if __name__ == "__main__":
    asyncio.run(main())
