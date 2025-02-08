from openai import OpenAI
import openai
import os

import time
from apirequest import get_product_ecoscore

class GPTModel:
    def __init__(self, dims) -> None:
        self.api_key = "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"  
        openai.api_key = self.api_key

        self.gpt = openai 
        self.dims = dims
        self.loading = False
        self.messages = []

    def generate_output(self, item, score):
        score = score.lower()
        if score not in ['a', 'b', 'c', 'd', 'e']:
            return f"Could not find an Eco-Score for {item}."

        if score in ['a', 'b']:
            return f"Great choice! {item} has an Eco-Score of {score.upper()}, meaning it is a sustainable option."
        elif score == 'c':
            return f"{item} has an Eco-Score of C. It is an alright choice."
        elif score == 'd':
            return f"{item} has an Eco-Score of D. Consider a more sustainable alternative if possible."
        elif score == 'e':
            return f"{item} has an Eco-Score of E, meaning it has a high environmental impact. You may want to find a greener option."


    def generate_llm_response(self, prompt: str, model: str = "gpt-4o") -> str:
        self.messages.append({'role': 'user', 'content': prompt})
        if self.loading:
            return "A prompt is already being processed."

        try:
            self.loading = True
            start = time.time()

            res = self.gpt.chat.completions.create(
                model=model,  
                messages=self.messages
            )

            response = res.choices[0].message.content

            end = time.time()
            self.last_runtime = end - start

            print(f"[generate_llm_response]: Response: {response}")
            self.add_message_history(prompt, response)

        except Exception as e:
            response = f"Error: {str(e)}"
            print(f"[generate_llm_response]: {response}")
        finally:
            self.loading = False

        return response

    def add_message_history(self, prompt, response):
        self.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    model = GPTModel(dims=100)  
    
    barcode = "3017620422003"  # Example barcode (Nutella)
    product_name, ecoscore = get_product_ecoscore(barcode)
    
    eco_message = model.generate_output(product_name, ecoscore)
    print(eco_message)
    
    user_prompt = f"What are more sustainable alternatives to {product_name}?"
    ai_response = model.generate_llm_response(user_prompt)
    print(ai_response)
