import re
import unicodedata

class TextCleaner:
    """
    Ported from Copilot version.
    Handles cleaning of Japanese text: URL removal, symbols, normalization.
    """
    def __init__(self, 
                 remove_numbers: bool = False,
                 remove_symbols: bool = True,
                 normalize_whitespace: bool = True):
        self.remove_numbers = remove_numbers
        self.remove_symbols = remove_symbols
        self.normalize_whitespace = normalize_whitespace

    def clean(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        
        # Normalize (Half-width to Full-width, NFKC)
        text = unicodedata.normalize('NFKC', text)
        
        # Remove URLs
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text)
        
        # Remove Emails
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
        
        if self.normalize_whitespace:
            text = text.replace('\u3000', ' ')
            text = re.sub(r'\s+', ' ', text)
            
        if self.remove_numbers:
            text = re.sub(r'[0-9０-９]', '', text)
            
        if self.remove_symbols:
            # Remove Japanese punctuation and common symbols
            symbols = '。，、！？・；：（）「」『』【】〔〕…―'
            for s in symbols:
                text = text.replace(s, '')
            # Use a safer way to remove all punctuation
            import string
            punct = string.punctuation
            for p in punct:
                text = text.replace(p, '')
            
        return text.strip()
