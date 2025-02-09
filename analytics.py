from openai import OpenAI
import openai
import os
import time


def txt_reading():
    items_dict = {}
    with open("data.txt", "r") as file:
        for line in file:
            item, score = line.strip().split(",")
            items_dict[item] = int(score)

    return items_dict

class GPTModel:
    def __init__(self) -> None:
        self.gpt = OpenAI(api_key='LA-3f0a8c11e9454fe5828778015edc487d7a77ef71f1d844808c92a6f91363cc54', base_url = "https://api.llama-api.com")
        self.loading = False
        self.messages = []
    

    def summary(self, items_dict):
        score = score.lower()
        if not len(items_dict):
            return "There are no items to be analyzed."
        else:
            message = f"""
You have shopped for {", ".join(items_dict.keys())} \n Here is the overall sustainability review for these items. 
"""
            prompt = f"""
A grocery shopper is buying a variety of items: {", ".join(items_dict.keys())}. Those items had the following \
sustainability scores: {", ".join(items_dict.values())}. Given this information, please give a polite summary of the \
grocery trip, and some tips for how the shopper might be able to be more sustainable on the next trip.\
 Do not go beyond one about 4 sentences.
"""
            with open("data.txt", "r+") as file:
                file.truncate(0)
            return message + self.generate_llm_response(prompt)

    def generate_llm_response(self, prompt: str) -> str:
        self.messages.append({'role': 'user', 'content': prompt})
        if self.loading:
            response = "A prompt is already being processed."
        else:
            try:
                self.loading = True
                res = self.gpt.chat.completions.create(
                    model='llama3.1-8b',
                    messages=self.messages
                )
                response = res.choices[0].message.content
                print(f"[generate_llm_response]: response: {response}")
            except Exception as e:
                self.loading = False
                response = f"An error occurred: {str(e)}"
                print(f"[generate_llm_response]: Error: {response}")
            finally:
                self.loading = False

        return response


if __name__ == "__main__":
    model = GPTModel() 
    items_dicts = txt_reading()
    analytics_message = model.summary(items_dicts)
    print(analytics_message)
