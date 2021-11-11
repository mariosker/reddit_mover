import praw


class reddit_instance:
    def __init__(self, credentials) -> None:

        self.reddit = praw.Reddit(client_id=credentials['client_id'],
                                  client_secret=credentials['client_secret'],
                                  user_agent=credentials['user_agent'],
                                  username=credentials['username'],
                                  password=credentials['password'])
        self.user = self.reddit.user
        self.me = self.reddit.user.me()

    def get_subscribed_subreddits(self) -> list:
        return [sub.display_name for sub in self.user.subreddits(limit=None)]

    def subscribe_to_subredddits(self, subreddits):
        for sub in subreddits:
            self.reddit.subreddit(sub).subscribe()

    def unsubscribe_from_subredddits(self, subreddits):
        for sub in subreddits:
            self.reddit.subreddit(sub).unsubscribe()

    def get_multireddits(self):
        return list(self.user.multireddits())

    def add_multireddits(self, multireddits):
        for multi in multireddits:
            self.reddit.multireddit.create(display_name=multi.display_name,
                                           subreddits=multi.subreddits)

    def delete_multireddits(self, multireddits):
        for multi in multireddits:
            multi.delete()

    def duplicate_multireddits_from_instance(self, from_reddit_instance):
        from_subscribed_multireddits = from_reddit_instance.get_multireddits()
        to_subscribed_multireddits = self.get_multireddits()
        if to_subscribed_multireddits:
            self.delete_multireddits(to_subscribed_multireddits)
        if from_subscribed_multireddits:
            self.add_multireddits(from_subscribed_multireddits)

    def duplicate_subreddits_from_instance(self,
                                           from_reddit_instance,
                                           delete_difference=False):
        from_subscribed_subs = from_reddit_instance.get_subscribed_subreddits()
        self.subscribe_to_subredddits(from_subscribed_subs)

        if delete_difference:
            to_subscribed_subs = self.get_subscribed_subreddits()

            difference = list(
                set(from_subscribed_subs).difference(set(to_subscribed_subs)))
            self.unsubscribe_from_subredddits(difference)

    def duplicate_preferences(self, from_reddit_instance):
        original_preferences = from_reddit_instance.user.preferences()
        self.user.preferences.update(**original_preferences)
