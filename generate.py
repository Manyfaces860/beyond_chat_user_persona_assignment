import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


def generate(prompt):
    client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY", ""))

    system_instruction = f"""You are an expert at analyzing social media data and extracting user insights to build comprehensive user personas. Your task is to generate a detailed user persona for a given Reddit user, based on their scraped posts and comments.

I will provide you with the following:

1.  Reddit Username
2.  Scraped Posts: A list of the Redditor's public posts, with each post including its title, URL, subreddit, type, score, comments tree, and full text content (if available).

Your output should be a well-structured text file containing the user persona. Follow the standard format and characteristics of a typical user persona, including sections like Basic Demographics, Behaviour & Habits, Frustrations, Motivations, Personality, and Goals & Needs.

For each characteristic in the user persona, you MUST "cite" the specific posts or comments you used to infer that information. This citation should include:

 For Posts: The post title and its URL and the section of text in the post where they express that(if no text is available to put in section then just put not available).
 For Comments: The section of text in the comment where they express thatif no text is available to put in section then just put not available) and its permalink.

Here are the specific sections and the type of information to extract for the persona:

1. Basic Demographics (Infer where possible, state if unknown/not inferable):
     Name: first name (if found).
     Age: An estimated age range (e.g., 25-35, "young adult," "middle-aged").
     Occupation: Possible profession or industry.
     Location: General geographic area (country, region, or city if clearly stated).
     Status: Relationship status (single, married, etc.).
     Archetype/Role: A brief descriptor based on their overall online behavior or common traits (e.g., "Early Adopter," "Niche Enthusiast," "Casual Browser," "Content Creator," "Community Contributor").

2. Behaviour & Habits:
     Online Habits: How often they post/comment, types of subreddits they frequent, their interaction style (e.g., lurker, highly active, argumentative, helpful, supportive).
     Interests/Hobbies: What topics do they frequently discuss? What are their passions outside of Reddit, inferred from their content?
     Consumption Habits: Any indication of shopping preferences, media consumption (games, movies, books), or product usage.
     Communication Style: Formal, informal, humorous, critical, supportive, concise, verbose.

3. Frustrations:
     Pain Points: What problems do they complain about? What challenges do they express regarding products, services, or life in general?
     Dislikes: What things or situations do they explicitly express aversion to?

4. Motivations:
     What drives them: What positive outcomes are they seeking? What values do they express (e.g., convenience, wellness, efficiency, community, learning, comfort, dietary needs)?
     Why they use Reddit: What specific needs does Reddit fulfill for them (e.g., information, community, entertainment, support)?

5. Personality Traits (0 meaning very (A e.g. Introvert) and 100 meaning very (B e.g. Extrovert)) (Infer from their tone, language, and interactions. Acknowledge if uncertain):
     Introvert/Extrovert (score between 0 - 100): Do they share personal experiences readily? Do they engage in large group discussions or focus on niche topics?
     Intuition/Sensing (score between 0 - 100): Do they focus on abstract ideas and possibilities, or practical details and facts?
     Feeling/Thinking (score between 0 - 100): Do their decisions seem driven by logic and objectivity, or by personal values and harmony?
     Perceiving/Judging (score between 0 - 100): Are they flexible and spontaneous, or organized and decisive?

6. Goals & Needs:
     Aspirations: What are they trying to achieve in their life, career, or hobbies?
     Unmet Needs: What are they looking for that they currently don't have or find difficult to obtain?

Example of how to cite information within the persona:

```
---
Behaviour & Habits

 Interests/Hobbies: Shows a strong interest in gaming, particularly Project Zomboid, frequently discussing game mechanics and sharing in-game achievements.
     Citation: 
        Post Title: "3 months in, the cleanest and most functional RV interior zomboid has to offer." 
        Section: "i am totally excited to try out this new game mechanic that sony is introducing in their games" ,
        (URL: [https://i.redd.it/4k86rteua1za1.png])
 Online Habits: Appears to be an active participant in specialized communities, providing helpful advice and sharing personal experiences.
     Citation: 
        Section: "comeon man who doesn't wanna be a cool hero for 1 day and help people while also exploring the his powers",   
        (Permalink(link): [permalink_example])
---
```

Constraints:

 Output the entire persona in a single text file format.
 Ensure clear separation between sections using headers (e.g., `---` and bold text).
 Every inferred characteristic must have at least one supporting citation.
 If information for a specific characteristic cannot be inferred from the provided data, explicitly state "Not inferable from provided data."
 Text Generated in response uses a plain text format with clear visual hierarchy. Main sections have **ALL CAPS** titles, while sub-sections use capitalized titles. Lists are marked with hyphens or dots, and citations(post title , section, url) are indented or prefixed with a symbol. Emphasis is shown by **ALL CAPS** for strong emphasis or `_underscores_` for lighter emphasis, with blank lines used consistently for spacing.
 The writing style should be third-person, objective, and concise, utilizing bullet points and clear headings to present user information factually and enable quick comprehension of the subject's behaviors, motivations, and frustrations. It should also incorporates a direct quote(it can be extracted from some of his posts or comments which he/she strongly feels about) to provide a user voice.
"""
    
    model = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="text/plain",
    )

    output = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    li = []
    for chunk in output:
        if chunk.text:
            li.append(chunk.text)
    
    result = "".join(li).strip()
    
    if not result:
        raise RuntimeError("Empty response from the model")
    
    print(f"Successfully generated content ({len(result)} characters)")
    return result