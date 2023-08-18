import os 
import re

def check_clear_history(text, filename='../data/memory.pkl'):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    keywords = [['clear', 'history'], ['delete', 'history']]
    words = text.split()

    if (any(all(keyword in words for keyword in keyword_group) for keyword_group in keywords)) and len(words) < 4:
        try:
            os.remove(filename)
            print(f"File '{filename}' deleted.")
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    else:
        print("Conditions not met. File not deleted.")
        return False