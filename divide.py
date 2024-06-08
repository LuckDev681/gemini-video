import math

def divide_text(text, num_parts):
    # Split the text into words
    words = text.split()
    
    # Calculate the length of each part
    total_words = len(words)
    part_length = math.ceil(total_words / num_parts)
    
    # Divide the words into parts
    parts = [words[i:i + part_length] for i in range(0, total_words, part_length)]
    
    # Combine the words back into strings
    parts = [' '.join(part) for part in parts]
    
    return parts