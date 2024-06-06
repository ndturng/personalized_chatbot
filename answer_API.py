import requests
import os

from dotenv import load_dotenv
load_dotenv()
# get key from env file

api_token = os.getenv("HUGGING_FACE_API_KEY")
headers = {"Authorization": f"Bearer {api_token}"}

# This model is a fine-tuned version of BERT for question answering on the SQuAD 2.0 dataset
model_name = "deepset/bert-base-cased-squad2"


def answer_question(question, context):
    # Combine the context and question into a single prompt, must be a dict
    prompt = {
        "question": question,
        "context": context
    }

    # Define the payload for the request
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
            "min_length": 50,
            "top_k": 50,
            "top_p": 0.8,
            "temperature": 0.6,
            "length_penalty": 1.5
        },
    }

    # Make the request to the Hugging Face Inference API
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_name}",
        headers=headers,
        json=payload,
    )

    # Parse the response
    response_json = response.json()
    # handle errors
    if "error" in response_json:
        error_message = response_json["error"]
        
        return f"An error occurred: {error_message}"
    
    # Extract and return the answer
    answer = response_json[0]["answer"]
    return answer


# Example usage
context_1 = "In 1969, humans landed on the moon for the first time in history. The Apollo 11 mission, led by NASA, successfully carried astronauts Neil Armstrong, Buzz Aldrin, and Michael Collins to the lunar surface. Armstrong and Aldrin walked on the moon, conducting experiments and collecting samples, while Collins orbited above. This monumental achievement was the result of years of dedicated work by scientists, engineers, and countless support staff. The mission symbolized the pinnacle of human ingenuity and exploration, pushing the boundaries of what was considered possible. The famous words, 'That's one small step for man, one giant leap for mankind,' spoken by Neil Armstrong, became etched in history."
question_1 = "What did the Apollo 11 mission symbolize, and what was its significance?"

context_2 = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design. However, it has become a global cultural icon of France and one of the most recognizable structures in the world. The Eiffel Tower is the most-visited paid monument in the world, with millions of people ascending it every year. It is also a symbol of love and romance, making it a popular destination for couples and tourists alike."
question_2 = "What is the Eiffel Tower's significance and why is it a popular tourist destination?"

answer = answer_question(question_2, context_2)
print("Answer:", answer)
# This model give too brief answers