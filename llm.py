from openai import OpenAI
from prompts import Prompts
import time

class GPTModel:
    def __init__(self, dims) -> None:
        self.gpt = OpenAI(api_key="a")
        self.prompts = Prompts()
        self.dims = dims
        self.loading = False
        self.messages = []

    def generate_output(item, score):
        score = score.lower()
        if score not in ['a', 'b', 'c', 'd', 'e']:
            return f"Could not find score for {item}"
        if score == 'a' or score == 'b':
            return f"""This is a great choice! {item} has a sustainability score of {score}."""
        elif score == 'c':
            return ""
        elif score == 'd' or score == 'e':
            return ""
            

    def generate_llm_response(self, prompt: str, model: str) -> str:
        self.messages.append({'role': 'user', 'content': prompt})
        if self.loading:
            response = "A prompt is already being processed."
        else:
            try:
                self.loading = True
                start = time.time()
                res = self.gpt.chat.completions.create(
                    model='gpt-4o',
                    messages=self.messages
                )
                response = res.choices[0].message.content
                
                end = time.time()
                #print("time:", end-start)
                self.last_runtime = end-start
                print(f"[generate_llm_response]: response: {response}")
                self.add_message_history(prompt, response, model)
            except Exception as e:
                self.loading = False
                response = f"An error occurred: {str(e)}"
                print(f"[generate_llm_response]: Error: {response}")

            finally:
                self.loading = False
            return response
    
    def add_message_history(self, prompt, response, model):
        self.messages.append({"role": "assistant", "content": response})
