from typing import List
from profilecore.core.module import AnalysisModule
from profilecore.text.cleaner import TextCleaner

class TextAnalyzer(AnalysisModule):
    """
    Combines cleaning (Copilot style) and Sudachi analysis (Gemini style).
    """
    def run(self, input_key: str, text_col: str):
        df = self.context.get_data(input_key)
        if df is None: return
        
        self.log(f"Starting text analysis on column: {text_col}")
        
        # 1. Clean Text
        cleaner = TextCleaner()
        df[f'{text_col}_cleaned'] = df[text_col].apply(cleaner.clean)
        
        # 2. Tokenize (Sudachi)
        df['tokens'] = df[f'{text_col}_cleaned'].apply(self._tokenize)
        
        self.context.set_data(f"{input_key}_analyzed", df)
        self.log("Text analysis complete.")

    def _tokenize(self, text: str) -> List[str]:
        if not text: return []
        try:
            from sudachipy import dictionary, tokenizer
            t_obj = dictionary.Dictionary().create()
            mode = tokenizer.Tokenizer.SplitMode.C
            # Extract Nouns, Verbs, Adjectives (Basic forms)
            tokens = []
            for m in t_obj.tokenize(text, mode):
                pos = m.part_of_speech()[0]
                if pos in ['名詞', '動詞', '形容詞']:
                    tokens.append(m.dictionary_form())
            return tokens
        except ImportError:
            return text.split()
