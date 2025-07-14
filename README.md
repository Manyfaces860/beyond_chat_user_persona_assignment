# Reddit User Persona Generator

This project consists of Python scripts designed to scrape a Reddit user's posts and comments, and then leverage a large language model (LLM) to generate a detailed user persona based on the scraped data.

## Features

- **Reddit Data Scraping:** Fetches a specified Reddit user's recent posts and comments, including full conversation threads on posts they've interacted with.

- **User Persona Generation:** Utilizes the Google Gemini API to create a comprehensive user persona, inferring details like demographics, behaviors, frustrations, motivations, personality traits, and goals.

- **Contextual Citations:** Each inferred characteristic in the persona is cited with direct links and text snippets from the Reddit posts or comments that informed the inference.

- **Structured Output:** The generated user persona is saved as a plain text file, following a clear, hierarchical format with sections and bullet points.

## Setup

### Prerequisites

- Python 3.8+

### Installation

This project provides two methods for installing dependencies: using `uv` (recommended for speed and efficiency) or using `pip`.

1. **Clone the repository (or save the files):**
   Save the `fetch_data.py`, `generate.py`, and `main.py` files into a single directory. A `requirements.txt` file is in the same directory with the following content:

   ```
   google-genai
   praw
   dotenv
   ```

2. **Choose your installation method:**

   #### Option 1: Using `uv` (Recommended)

   - **Install `uv`:** If you don't have `uv` installed, follow the [Installation Guide](https://astral.sh/blog/uv-the-fast-python-package-installer).
   - **Install dependencies:** Navigate to your project directory in the terminal and run:

     ```bash
     uv add -r requirements.txt
     ```

     or 

     Run below command if you cloned the repository to setup the dependencies

     ```bash
     uv sync --locked
     ```

   #### Option 2: Using `pip`

   - **Install dependencies:** Navigate to your project directory in the terminal and run:

     ```bash
     pip install -r requirements.txt
     ```

### Environment Variables

This project requires sensitive API keys and user credentials, which are managed using a `.env` file. Reddit_client_credentials and Gemini_api_key

1. **Create a `.env` file:**
   In the root of your project directory, create a file named `.env`.

2. **Add the following variables to your `.env` file:**

   ```dotenv
   REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID"
   REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET"
   REDDIT_USER_NAME="YOUR_REDDIT_ACCOUNT_USERNAME"
   GOOGLE_GENAI_API_KEY="YOUR_GEMINI_API_KEY"
   ```

### How to Get API Keys and Credentials

#### Reddit API Credentials (PRAW)

1. **Create a Reddit Application:**

   - Go to [Reddit's app preferences page](https://www.reddit.com/prefs/apps).
   - Scroll to the bottom and click "create another app...".
   - Fill in the details:
     - **Name:** Choose a unique name for your application (e.g., "MyPersonaBot").
     - **Type:** Select "script".
     - **description:** (Optional) A brief description.
     - **about url:** (Optional) Your website or project link.
     - **redirect uri:** Enter `http://localhost:8080` (this is a placeholder for script-type apps).
   - Click "create app".

2. **Retrieve Credentials:**

   - After creating the app, you will see your app details.
   - `REDDIT_CLIENT_ID`: This is the string under "personal use script" (e.g., `xxxxxxxxxxxxx`).
   - `REDDIT_CLIENT_SECRET`: This is the string next to "secret" (e.g., `yyyyyyyyyyyyyyyyyyyyyyyyyyy`).
   - `REDDIT_USER_NAME`: Your Reddit account username.

#### Google Gemini API Key

1. **Access Google AI Studio:**

   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Sign in with your Google account.

2. **Create API Key:**

   - On the "Get API key" page, click "Create API key in new project" or select an existing project.
   - Copy the generated API key. This will be your `GOOGLE_GENAI_API_KEY`.

## How to Run

1. **Configure `main.py`:**
   Open the `main.py` file. Locate the `url` variable and change it to the Reddit user's profile URL you wish to analyze.

   ```python
   url = "https://www.reddit.com/user/TARGET_REDDIT_USERNAME/" # Change this
   ```

   You can also adjust the `scan_user_posts_limit` and `fetch_comments_per_post_limit` in the `get_user_conversations_on_any_post` call to control the depth of scraping.

2. **Run the script:**
   From your terminal, in the project directory, execute:

   ```bash
   python main.py
   ```

   or 

   ```bash
   uv run main.py
   ```

## Output

Upon successful execution, the script will:

1. Print status messages to the console regarding the scraping and persona generation process.

2. Save the generated output files in the **`output/`** directory. This directory will be created automatically if it doesn't exist.

   - `{target_username}_conversations.json`: This file will contain all the raw scraped Reddit data.
   - `{target_username}_persona.txt`: This file will contain the generated user persona, complete with citations.
