from typing import Union


class Broadcast:
    def __init__(self, payload: dict) -> None:
        """
        The broadcast class containing most of the information about a broadcast.

        Attributes
        ----------
        id : str
            The ID of the broadcast.
        title : str
            The title of the broadcast.
        url : str
            The URL of the broadcast.
        thumbnail : str
            The URL of the thumbnail of the broadcast.
        score : int
            The total score of the broadcast.
        comment_count : int
            The total number of comments on the broadcast.
        created : int
            The timestamp of when the broadcast was created.
        author_name : str
            The username of the author of the broadcast (Returns 'u/[deleted]' if username is not found).
        subreddit_name : str
            The name of the subreddit the broadcast is in.
        published_at : int
            The timestamp of when the broadcast was started.
        upvotes : int
            The total number of upvotes on the broadcast.
        downvotes : int
            The total number of downvotes on the broadcast.
        is_first_broadcast : bool
            If the broadcast is the author's first broadcast.
        chat_disabled : bool
            If the chat is disabled for the broadcast.
        broadcast_time : str
            The current running time of the broadcast.
        estimated_remaining_time : str
            The estimated remaining time of the broadcast.
        is_live : bool
            If the broadcast is currently live.
        rank : int
            The rank of the broadcast.
        global_rank : int
            The global rank of the broadcast.
        subreddit_rank : int
            The rank of the broadcast in the subreddit.
        total_streams : int
            The total number of streams in the subreddit.
        unique_watchers : int
            The number of unique watchers of the broadcast.
        continuous_watchers : int
            The number of continuous watchers of the broadcast.
        total_continuous_watchers : int
            The total number of continuous watchers of the broadcast.
        """
        self.id = payload["post"]["id"]
        self.title = payload["post"]["title"]
        self.url = payload["post"]["url"]
        self.score = payload["post"]["score"]
        self.comment_count = payload["post"]["commentCount"]
        if payload["post"]["authorInfo"]:
            self.author_name = payload["post"]["authorInfo"]["name"]
        else:
            self.author_name = "[deleted]"
        self.subreddit_name = payload["post"]["subreddit"]["name"]
        self.published_at = payload["stream"]["publish_at"]
        self.upvotes = payload["upvotes"]
        self.downvotes = payload["downvotes"]
        self.is_first_broadcast = payload["is_first_broadcast"]
        self.chat_disabled = payload["chat_disabled"]
        self.broadcast_time = payload["broadcast_time"]
        self.estimated_remaining_time = payload["estimated_remaining_time"]
        if payload["stream"]["state"] == "IS_LIVE":
            self.is_live = True
        else:
            self.is_live = False
        self.rank = payload["rank"]
        self.global_rank = payload["global_rank"]
        self.subreddit_rank = payload["rank_in_subreddit"]
        self.total_streams = payload["total_streams"]
        self.unique_watchers = payload["unique_watchers"]
        self.continuous_watchers = payload["continuous_watchers"]
        self.total_continuous_watchers = payload["total_continuous_watchers"]

        self.thumbnail = payload["stream"]["thumbnail"]

    def __repr__(self) -> str:
        return f"Broadcast({self.id})"


class Broadcasts:
    def __init__(self, contents: list = None) -> None:
        """
        The broadcast list class containing all of the broadcasts fetched from the API.\

        Attributes
        ----------
        broadcasts : list
            The list of broadcasts.
        """
        self.broadcasts = []
        if contents:
            self.broadcasts = contents

    def top_broadcast(self, subreddit: str = None) -> Union[Broadcast, None]:
        """
        Gets the top broadcast.

        Parameters
        ----------
        subreddit : str
            Optional paramater to find the top broadcast on a specific subreddit.

        Returns
        -------
        Broadcast
            The top broadcast.
        """
        if not len(self.broadcasts):
            return None

        if subreddit is None:
            return self.broadcasts[0]
        else:
            subreddit = subreddit.lower()
            for broadcast in self.broadcasts:
                if broadcast.subreddit_name.lower() == subreddit:
                    return broadcast
        return None

    def has_broadcast(self, id: str) -> Union[Broadcast, bool]:
        """
        Checks if the broadcast list contains a broadcast with a specified ID.

        Parameters
        ----------
        id : str
            The ID of the broadcast.

        Returns
        -------
        Broadcast
            If the broadcast list contains a broadcast with the specified ID.
        """
        for broadcast in self.broadcasts:
            if broadcast.id == id:
                return broadcast
        return False

    def has_streamer(self, name: str) -> Union[Broadcast, bool]:
        """
        Checks if the broadcast list contains a broadcast from a specified user.

        Parameters
        ----------
        name : str
            The streamer to search for.

        Returns
        -------
        Broadcast
            If the broadcast list contains a broadcast from the specified user.
        """
        name = name.lower()
        for broadcast in self.broadcasts:
            if broadcast.author_name.lower() == name:
                return broadcast
        return False

    def __repr__(self) -> str:
        return f"Broadcasts({', '.join(repr(broadcast) for broadcast in self.broadcasts)})"
