import re

def extract_text(input_string):
    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  
                               u"\U0001F300-\U0001F5FF"  
                               u"\U0001F680-\U0001F6FF"  
                               u"\U0001F700-\U0001F77F"  
                               u"\U0001F780-\U0001F7FF"  
                               u"\U0001F800-\U0001F8FF"  
                               u"\U0001F900-\U0001F9FF"  
                               u"\U0001FA00-\U0001FA6F"  
                               u"\U0001FA70-\U0001FAFF"  
                               u"\U00002702-\U000027B0"  
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    #input_string = emoji_pattern.sub(r'', input_string)

    # Encontra o primeiro número, ponto ou letra após a remoção dos emojis
    match = re.search(r'[\d\.a-zA-Z]', input_string)
    if match:
        result = input_string[match.start():]
        return result
    else:
        return input_string

#input_string = "📚- Apoio Efolio A"
input_string = "✅- 1. Noções de Lógica"
result = extract_text(input_string)
print(result)
