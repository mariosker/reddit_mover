from tqdm import tqdm
import credentials
from reddit_instance import reddit_instance

original_reddit = reddit_instance(credentials.original_reddit_credentials)
secondary_reddit = reddit_instance(credentials.secondary_reddit_credentials)

secondary_reddit.duplicate_preferences(original_reddit)
secondary_reddit.duplicate_subreddits_from_instance(original_reddit,
                                                    delete_difference=False)
secondary_reddit.duplicate_multireddits_from_instance(original_reddit)
