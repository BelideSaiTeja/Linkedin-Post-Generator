import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from requests import post
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
    
    print(enriched_posts)
    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)
    
    with open(processed_file_path, 'w', encoding='utf-8') as file:
        json.dump(enriched_posts, file, indent=4)


def extract_metadata(post):
    
    template = '''

        You are a JSON generator.

            Your task is to extract metadata from a LinkedIn post.

            You MUST return ONLY valid JSON.
            If you add any extra text, the answer is WRONG.

            Rules:
            1. Output must be ONLY JSON. No explanations, no comments, no markdown, no words before or after JSON.
            2. No explanations.
            3. No markdown.
            4. No words before or after JSON.
            5. JSON must contain EXACTLY these keys:
            - line_count
            - language
            - tags
            6. tags must contain MAXIMUM 2 items in a list format like ["tag1", "tag2"]. If there are more than 2 tags, pick the most relevant ones. If there are no tags, return an empty list.
            7. language must be either "English" or "Hinglish".

            Now extract metadata from the below post in the below mentioned example format only without any additional information:

            {post}
            JSON:
            '''
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm 
    response = chain.invoke({'post': post})
    
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response)
    except OutputParserException:
        raise OutputParserException('Invalid JSON returned by model')
    return res

def get_unified_tags(posts_with_metadata):
    all_tags = set()
    for post in posts_with_metadata:
        all_tags.update(post['tags'])
    
    unique_tags_list = ', '.join(all_tags)
    
    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

if __name__ == "__main__":
    process_posts("sample_posts.json", "processed_posts.json")
