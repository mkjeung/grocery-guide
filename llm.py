from openai import OpenAI
import threading
import openai
import os
import time
from apirequest import get_product_ecoscore
from tts import text_to_speech

class GPTModel:
    def __init__(self) -> None:
        self.gpt = OpenAI(api_key='', base_url = "https://api.llama-api.com")
        self.loading = False
        self.messages = []

    def generate_output(self, item, score):
        score = score.lower()
        if score not in ['a', 'b', 'c', 'd', 'e']:
            return f"Could not find score for {item}"
        if score == 'a' or score == 'b':
            message = f"""This is a great choice! {item} has a sustainability score of {score.upper()}."""
        else:
            message = f"""
Your item {item} has a poor sustainability score of {score}. 
"""
            prompt = f"""
A grocery store shopper is buying an unsustainable item, {item}. Suggest more sustainable alternatives. Respond in one polite sentence listing alternatives. Do not go beyond one sentence.
"""
            return message + self.generate_llm_response(prompt)

    def generate_llm_response(self, prompt: str) -> str:
        self.messages.append({'role': 'user', 'content': prompt})
        
        if self.loading:
            return "A prompt is already being processed."
        
        response = "The response is taking too long. Please try again later."
        
        def llm_call():
            nonlocal response
            try:
                print("Loading LLM!")
                self.loading = True
                res = self.gpt.chat.completions.create(
                    model='llama3.1-8b',
                    messages=self.messages
                )
                response = res.choices[0].message.content
                print(f"[generate_llm_response]: response: {response}")
            except Exception as e:
                response = f"An error occurred: {str(e)}"
                print(f"[generate_llm_response]: Error: {response}")
            finally:
                self.loading = False

        # Start the LLM call in a separate thread
        thread = threading.Thread(target=llm_call)
        thread.start()
        thread.join(timeout=5)  # Wait up to 3 seconds
        
        if thread.is_alive():
            self.loading = False  # Ensure loading flag is reset
            print("[generate_llm_response]: Timed out.")

        return response


if __name__ == "__main__":
    model = GPTModel()  
    
    barcode = "3017620422003"  
    product_name, ecoscore = get_product_ecoscore(barcode)
    print(product_name)
    eco_message = model.generate_output(product_name, ecoscore)
    text_to_speech(eco_message)
