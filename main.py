import json
import os
from dotenv import load_dotenv
import praw
import sys

from fetch_data import get_user_conversations_on_any_post
from generate import generate

# Extract username from URL
url = "https://www.reddit.com/user/Euphoric-Welder5889/"


# Load environment variables
try:
    load_dotenv()
    print("Environment variables loaded successfully.")
except Exception as e:
    print(f"Error loading environment variables: {e}")
    print("Please ensure you have a .env file in your project directory.")
    sys.exit(1)

# Initialize PRAW
try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        user_agent=f"python:myredditbot:v1.0 (by u/{os.getenv('REDDIT_USER_NAME', '')})",
        username=os.getenv("REDDIT_USER_NAME", ""),
    )
    print("PRAW initialized successfully.")
except Exception as e:
    print(f"Error initializing PRAW: {e}")
    print("Please check your CLIENT_ID, CLIENT_SECRET, REDDIT_USER_NAME and internet connection.")
    sys.exit(1)


try:
    target_username = url.split("/")[-2]  # Extract username from URL
    if not target_username:
        raise ValueError("Invalid URL format")
    print(f"Target username: {target_username}")
except Exception as e:
    print(f"Error extracting username from URL: {e}")
    print("Please ensure the URL is in the format: https://www.reddit.com/user/USERNAME/")
    sys.exit(1)

# Create output directory if it doesn't exist
try:
    os.makedirs("output", exist_ok=True)
    print("Output directory created/verified.")
except Exception as e:
    print(f"Error creating output directory: {e}")
    sys.exit(1)

# Get conversations where the user commented on any post (their own or others')
try:
    print("Fetching user conversations...")
    user_conversations_on_any_post = get_user_conversations_on_any_post(
        target_username,
        scan_user_posts_limit=5,  # Number of posts to scan for comments
        fetch_comments_per_post_limit=15, # Number of comments to fetch per post
        reddit=reddit,
    )
    print(f"Successfully fetched conversations for user: {target_username}")
except Exception as e:
    print(f"Error fetching user conversations: {e}")
    print("This could be due to:")
    print("- Invalid username")
    print("- Reddit API rate limits")
    print("- Network connectivity issues")
    print("- Private or suspended user account")
    sys.exit(1)

# Save the fetched data to a JSON file
try:
    output_file = f"output/{target_username}_conversations.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(user_conversations_on_any_post, f, ensure_ascii=False, indent=2)
    print(f"Data saved to: {output_file}")
except Exception as e:
    print(f"Error saving data to JSON file: {e}")
    print("This could be due to:")
    print("- Insufficient disk space")
    print("- Permission issues")
    print("- Invalid characters in filename")
    sys.exit(1)

# Load the data back (or use the already loaded `user_conversations_on_any_post` directly)
try:
    with open(f"output/{target_username}_conversations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Data loaded successfully from JSON file.")
except Exception as e:
    print(f"Error loading data from JSON file: {e}")
    print("Using the original data in memory instead.")
    data = user_conversations_on_any_post

# Convert the loaded dictionary to a JSON string for the prompt
try:
    data_json_string = json.dumps(data)
    print("Data converted to JSON string for prompt.")
except Exception as e:
    print(f"Error converting data to JSON string: {e}")
    print("This could be due to non-serializable data in the fetched content.")
    sys.exit(1)

# Prepare the prompt for the persona generation model
try:
    prompt = f"""
Now Generate the user persona based on the provided Reddit data.

[DATA]
Redditor Username: {target_username}

{data_json_string}
"""
    print("Prompt prepared successfully.")
except Exception as e:
    print(f"Error preparing prompt: {e}")
    sys.exit(1)

# Generate the persona
try:
    print("Generating persona using AI model...")
    persona = generate(prompt)
    print("Persona generated successfully.")
    print("\n" + "="*50)
    print("GENERATED PERSONA:")
    print("="*50)
    print(persona)
    print("="*50)
except Exception as e:
    print(f"Error generating persona: {e}")
    print("This could be due to:")
    print("- Invalid or missing Google Gemini API key")
    print("- API rate limits exceeded")
    print("- Network connectivity issues")
    print("- Model service unavailable")
    sys.exit(1)

# Save the generated persona to a text file
try:
    persona_file = f"output/{target_username}_persona.txt"
    with open(persona_file, "w", encoding="utf-8") as f:
        f.write(persona)
    print(f"Persona saved to: {persona_file}")
except Exception as e:
    print(f"Error saving persona to file: {e}")
    print("The persona was generated successfully but could not be saved.")
    print("This could be due to:")
    print("- Insufficient disk space")
    print("- Permission issues")
    print("- Invalid characters in filename")
    # Don't exit here since the persona was generated successfully

print("\nScript completed successfully!")