# backend.py

import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# Optional translator
try:
    from googletrans import Translator
    translator_available = True
except:
    translator_available = False


class DevNovaAssistant:
    def __init__(self, dataset_path):
        self.faq_data = pd.read_csv(dataset_path)

        if 'Question' not in self.faq_data.columns or 'Answer' not in self.faq_data.columns:
            raise ValueError("Dataset must contain 'Question' and 'Answer' columns.")

        self.questions = self.faq_data['Question'].astype(str).tolist()
        self.answers = self.faq_data['Answer'].astype(str).tolist()

        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        self.question_embeddings = self.model.encode(
            self.questions,
            convert_to_tensor=True
        )

        if translator_available:
            self.translator = Translator()
        else:
            self.translator = None

    def get_response(self, user_input):
        try:
            if not user_input.strip():
                return "Please enter a valid query."

            if self.translator:
                try:
                    user_input = self.translator.translate(user_input, dest='en').text
                except:
                    pass

            query_embedding = self.model.encode(
                user_input,
                convert_to_tensor=True
            )

            scores = util.cos_sim(query_embedding, self.question_embeddings)
            best_match_idx = torch.argmax(scores).item()

            return self.answers[best_match_idx]

        except Exception as e:
            return f"Error: {str(e)}"