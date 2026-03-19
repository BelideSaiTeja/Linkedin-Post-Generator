import json
import pandas as pd

class FewShotPost:
    def __init__(self, file_path="processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
        
    def load_posts(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            posts = json.load(file)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x:x).sum()
            self.unique_tags = set(list(all_tags))
            self.unique_lengths = self.df['length'].unique()
            self.unique_languages = self.df['language'].unique()
            
    
    def categorize_length(self, line_count):
        if line_count <=5:
            return "Short"
        elif line_count <=10:
            return "Medium"
        else:
            return "Long"
    
    
    def get_tags(self):
        return self.unique_tags
    
    def get_lengths(self):
        return self.unique_lengths
    
    def get_languages(self):
        return self.unique_languages
    
    
    def get_filtered_posts(self, length, language, tag):
        filtered_df = self.df[
            (self.df['length'] == length) &
            (self.df['language'] == language) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        
        return filtered_df.to_dict(orient='records')
    

if __name__ == "__main__":
    fs = FewShotPost()
    posts = fs.get_filtered_posts(length="Short", language="English", tag="Job Search")
    print(fs.get_lengths())
    #print(fs.get_languages())
    #print(posts)