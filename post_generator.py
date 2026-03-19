from llm_helper import llm
from few_shot import FewShotPost 

few_shot = FewShotPost()    
def get_length_str(length):
    if length == "Short":
        return "1-5 lines"
    elif length == "Medium":
        return "5-10 lines"
    else:
        return "more than 10 lines"

def get_prompt(length, language, tag):
    length_str = get_length_str(length)
    prompt = f'''
    
    Describe about the {tag} in {language} within {length_str} in a way that is engaging and informative. Use a tone that is suitable for a professional audience on LinkedIn.
    Make sure to include a call to action at the end of the post, encouraging readers to engage with the content, share their thoughts, or take a specific action related to the topic.
    
    '''
    
    examples = few_shot.get_filtered_posts(length=length, language=language, tag=tag)
    
    #prompt += "Here are some examples of LinkedIn posts on the same topic:\n"  
    if len(examples) > 0:
        prompt += "Here are some examples of LinkedIn posts on the same topic:\n"
        for i, post in enumerate(examples):
            post_text = post['text']
            prompt += f"\n\n Example {i+1}: \n\n {post_text}"
            
            if i == 1:
                break
    return prompt

def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response


if __name__ == "__main__":
    post = generate_post(length="Short", language="English", tag="Generative AI")
    print(post)