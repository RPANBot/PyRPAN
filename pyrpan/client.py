import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from asyncpraw import Reddit
from asyncpraw.models import Submission
from expiringdict import ExpiringDict

from . import constants
from .exceptions import InvalidRequest
from .models import Broadcast, Broadcasts

logger = logging.getLogger(__name__)


class PyRPAN:
    """
    Client class for the PyRPAN API Wrapper.
    Attributes
    ----------
    reddit : str
        The Reddit instance to use to access the Reddit API.
    top_broadcasts_cache : ExpiringDict
        A cache of the top broadcasts.
    api_url : str
        URL to access the RPAN API.
    session : aiohttp.ClientSession
        For creating client session and to make requests.
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        Construct the PyRPAN wrapper.

        Parameters
        ----------
        client_id : str
            Client ID generated from creating an app at https://old.reddit.com/prefs/apps/.
        client_secret : str
            Client Secret generated from creating an app at https://old.reddit.com/prefs/apps/.
        """
        self.api_url = "https://strapi.reddit.com"
        self.top_broadcasts_cache = ExpiringDict(max_len=3, max_age_seconds=300)
        self.reddit = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Reddit Public Access Network (RPAN) API Wrapper by b1uejay27.",
        )
        self._session = None
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        """Close the client session."""
        if self._session is not None:
            await self._session.close()

    async def fetch(
        self, method: str, route: str, *, headers: Optional[dict] = None, data: Optional[dict] = None
    ) -> Optional[dict]:
        """
        Fetching a response from the API
        Parameters
        ----------
        route : str
            The API route you want to make a call to
        headers : dict
            Headers for the API call, Defaults to None
        data : dict
            Data for the API call, Defaults to None
        Returns
        -------
        Optional[dict]
            The response from the API.
        """
        if headers is None:
            headers = {}

        headers = {
            "User-Agent": "Reddit Public Access Network (RPAN) API Wrapper by b1uejay27.",
            "Cache-Control": "no-cache",
            **headers,
        }

        if not self._session:
            self._session = aiohttp.ClientSession()

        async with self._lock:
            async with self._session.request(
                method=method, url=self.api_url + route, headers=headers, data=data
            ) as res:
                # Handle status codes
                if res.status in [200, 201, 204]:
                    data = await res.json()

                if res.status == 400:
                    raise InvalidRequest("Bad request - Request performed was invalid.")

                if res.status == 429:
                    raise InvalidRequest("Too many requests - Slow down your requests.")

                if res.status == 500:
                    raise InvalidRequest("Internal Server Error - Something went wrong.")

        return data

    async def get_viewer_subreddits(self) -> list:
        """
        Gets a list of the recommended viewer RPAN subreddits.

        Returns
        -------
        list
            The list of viewer subreddits.
        """
        data = await self.fetch(method="GET", route="/recommended_viewer_subreddits")
        return data["data"]

    async def get_broadcast(self, id: str) -> Optional[Broadcast]:
        """
        Gets a broadcast by ID.

        Parameters
        ----------
        id : str
            ID of the broadcast you want to fetch.
        Returns
        -------
        Broadcast
            The retrived broadcast or None.
        """
        data = await self.fetch(method="GET", route=f"/broadcasts/{id}")
        if data["status"] == "success":
            payload = data["data"]

            return Broadcast(payload=payload)
        else:
            return None

    async def get_broadcasts(self) -> Optional[Broadcasts]:
        """
        Fetches all the currently active broadcasts.

        Returns
        -------
        Broadcasts
            The retrived broadcasts or None.
        """
        data = await self.fetch(method="GET", route="/broadcasts")
        if data["status"] == "success":
            broadcasts = []
            if len(data["data"]):
                for broadcast in data["data"]:
                    payload = broadcast
                    broadcasts.append(Broadcast(payload=payload))

                return Broadcasts(contents=broadcasts)
        else:
            return None

    async def get_last_broadcast(self, username: str) -> Optional[Broadcast]:
        """
        Gets the last broadcast of a user.

        Parameters
        ----------
        username : str
            The username of the user you want to get the last broadcast for.

        Returns
        -------
        Broadcast
            The found last broadcast or None.
        """
        user = await self.reddit.redditor(username)

        async for submission in user.submissions.new(limit=25):
            if self.is_rpan_broadcast(submission.url):
                return await self.submission_to_broadcast(submission)
        return None

    async def get_top_broadcasts(self, time_period: str = None) -> tuple:
        """
        Gets the top broadcast on each subreddit (from within a specific time period).

        Parameters
        ----------
        time_period : str
            The time period from which you would like to get the top broadcasts for.

        Returns
        -------
        tuple
            A tuple of the top broadcasts in each subreddit and the time period used.
        """
        allowed_time_periods = [
            "hour",
            "day",
            "week",
            "month",
            "year",
            "all",
        ]

        if time_period:
            time_period = time_period.lower()

        if time_period not in allowed_time_periods:
            time_period = "week"

        if time_period in self.top_broadcasts_cache:
            return self.top_broadcasts_cache[time_period], time_period
        else:
            top_broadcasts = {}
            for subreddit in constants.RPAN_SUBREDDITS:
                subreddit = await self.reddit.subreddit(subreddit)
                async for submission in subreddit.search(
                    'flair_name:"Broadcast"',
                    sort="top",
                    time_filter=time_period,
                    limit=1,
                ):
                    top_broadcasts[subreddit] = submission

            self.top_broadcasts_cache[time_period] = top_broadcasts
            return top_broadcasts, time_period

    async def submission_to_broadcast(self, submission: Submission) -> Optional[Broadcast]:
        """
        Turns a PRAW submission into a broadcast class.

        Parameters
        ----------
        submission : str
            The submission to turn into a broadcast class.

        Returns
        -------
        Broadcast
            The broadcast class.
        """
        return Broadcast(
            payload={
                "post": {
                    "id": submission.fullname,
                    "title": submission.title,
                    "url": submission.url,
                    "authorInfo": {"name": submission.author.name},
                    "subreddit": {"name": submission.subreddit.display_name},
                },
                "stream": {
                    "state": "IS_LIVE",  # TODO: Switch stream state
                    "publish_at": submission.created_utc,
                },
            }
        )

    def format_broadcast_timestamp(self, timestamp: int) -> str:
        """
        Formats a timestamp of a broadcast. This is used by the broadcast notifications.

        Parameters
        ----------
        timestamp : int
            The timestamp to format.

        Returns
        -------
        str
            The timestamp in a set format.
        """
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)

    def is_rpan_broadcast(self, link: str) -> bool:
        """
        Checks if a link is a valid RPAN broadcast.

        Parameters
        ----------
        link : str
            The link to check.

        Returns
        -------
        bool
            If the link is a valid RPAN broadcast.
        """
        if "reddit.com/rpan/" in link:
            return True
        else:
            return False
