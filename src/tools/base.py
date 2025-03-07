import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()


class RunApifyActor:
    """Run an Apify actor and return the results."""
    def __init__(self, actor):
        self.actor = actor

    def _run(self, actor_name, run_input):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._run_async(actor_name, run_input))
        finally:
            # loop.close()
            pass

    async def _run_async(self, actor_name, run_input):
        """Run an Apify actor and return the results."""
        try:
            actor_run = await self.actor.call(actor_name, run_input=run_input)
            if actor_run is None:
                raise RuntimeError('Actor task failed to start.')
            run_client = self.actor.apify_client.run(actor_run.id)
            await run_client.wait_for_finish()
            dataset_client = run_client.dataset()
            items = await dataset_client.list_items()
            dataset_items = items.items
            return dataset_items
        except Exception as e:
            return f"Error running Apify actor: {str(e)}"
