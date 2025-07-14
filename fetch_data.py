import time


def get_user_conversations_on_any_post(
    username, scan_user_posts_limit=100, fetch_comments_per_post_limit=None, reddit=None
):
    """
    Fettches comments made by the user on any post (their own or others'),
    and then for each unique post they commented on, retrieves the full conversation
    (all comments) on that post. This ensures each post's conversation is stored once.

    Args:
        username (str): The Reddit username.
        scan_user_posts_limit (int): The maximum number of the user's own comments
                                        to scan to identify unique posts they interacted with.
                                        This helps manage initial API calls if a user has
                                        tens of thousands of comments. PRAW's user.comments.new()
                                        typically provides up to 1000 comments.
        fetch_comments_per_post_limit (int, optional): The maximum depth/number of
                                                      comments to retrieve per post when
                                                      fetching the full conversation.
                                                      Set to None for as many as API allows
                                                      (PRAW's replace_more can fetch up to ~1000 comments).
        reddit (praw.Reddit, optional): An initialized PRAW Reddit instance.

    Returns:
        dict: A dictionary where keys are submission IDs and values are dictionaries
              containing 'submission_info' (details about the post) and 'comments_on_post'
              (a list of all comments on that post, regardless of author).
    """
    all_conversations_on_posts = {}
    posts_to_fetch_full_comments_from = set()  # Use a set to store unique submission IDs

    try:
        redditor = reddit.redditor(username)
        print(
            f"Scanning recent comments by {username} to identify unique posts they've interacted with..."
        )

        # Step 1: Get a sample of the user's comments to find unique posts they've commented on.
        # This is efficient as it only hits the user's comment history endpoint.
        # We use .new() for recent comments, but you could use .top() or other sorts.
        for submission in redditor.submissions.new(limit=scan_user_posts_limit):
            posts_to_fetch_full_comments_from.add(submission.id)

        print(
            f"Identified {len(posts_to_fetch_full_comments_from)} unique posts where {username} has commented."
        )

        # Step 2: For each unique post, fetch the full conversation (all comments on that post)
        for submission_id in posts_to_fetch_full_comments_from:
            # Ensure we don't re-fetch if somehow already processed (e.g., if a post was also by the user)
            if submission_id in all_conversations_on_posts:
                continue

            try:
                # Fetch the submission object for the identified post
                submission = reddit.submission(id=submission_id)
                print(
                    f"\nFetching full conversation for post: '{submission.title}' (ID: {submission.id})"
                )

                # Replace 'MoreComments' objects to get a more complete comment tree.
                # This is crucial for getting all replies and the full context of the discussion.
                submission.comments.replace_more(limit=fetch_comments_per_post_limit)

                # Flatten the comment forest to iterate through all comments (top-level and replies)
                post_comments_data = []
                for comment in submission.comments.list():
                    comment_info = {
                        "id": comment.id,
                        "body": comment.body,
                        "author": comment.author.name if comment.author else "[deleted]",
                        "created_utc": comment.created_utc,
                        "score": comment.score,
                        "permalink": "https://www.reddit.com" + comment.permalink,
                        "parent_id": comment.parent_id,  # ID of the parent comment or submission
                        "depth": comment.depth,  # How deep in the reply chain the comment is
                    }
                    post_comments_data.append(comment_info)

                # Store the submission info and all comments on it
                all_conversations_on_posts[submission.id] = {
                    "submission_info": {
                        "title": submission.title,
                        "url": submission.url,
                        "author": (
                            submission.author.name if submission.author else "[deleted]"
                        ),
                        "subreddit": submission.subreddit.display_name,
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "is_self": submission.is_self,
                        "selftext": submission.selftext if submission.is_self else None,
                    },
                    "comments_on_post": post_comments_data,
                }
                print(f"  Fetched {len(post_comments_data)} comments on this post.")
                time.sleep(
                    1
                )  # Small delay to be polite to the API and avoid hitting limits too hard

            except Exception as e:
                print(f"  Error fetching conversation for submission ID {submission_id}: {e}")
                # This could happen if a post was deleted, is private, or is inaccessible.
                continue

        print(
            f"\nCompleted fetching conversations from {len(all_conversations_on_posts)} unique posts where {username} commented."
        )
        return all_conversations_on_posts

    except Exception as e:
        print(f"An error occurred during initial user scan for {username}: {e}")
        print("Possible reasons: Invalid username, private profile, or API rate limits.")
        return {}


