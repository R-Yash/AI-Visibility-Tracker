
def get_prompt_generator(category):
    return f"""
**Role:** You are an expert Search Query Analyst for a major search engine. Your goal is to predict the "User Search Journey."

**Task:**
I will provide you with a specific **Category** or **Seed Keyword**.
You must generate exactly **5 relevant follow-up search queries** that a user would likely type next.

**Guidelines for Query Generation:**
1.  **Diversify Intent:** Do not just rewrite the keyword. You must cover these 5 distinct user needs:
    * *Cost/Value:* (e.g., pricing, cheap, ROI)
    * *Comparison:* (e.g., alternatives, vs competitors)
    * *Specific Use Case:* (e.g., for small business, for beginners)
    * *Technical/Setup:* (e.g., integration, how to use, installation)
    * *Social Proof/Risk:* (e.g., reviews, pros and cons, common problems)
2.  **Format:** Output only the 5 queries as a bulleted list. No introductory text.
3.  **Tone:** Keep queries natural, concise, and like something a human would actually type into a search bar.

**Example Input:**
"Project Management Software"

**Example Output:**
* free project management tools for startups
* Asana vs Trello vs Jira comparison
* project management software pricing 2024
* best pm tools for remote teams
* common implementation challenges with project management software

**Current Input:**
"{category}"
"""