from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize the GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


def answer_question(question, context):
    # Combine the context and question into a single prompt
    # prompt = f"Role: System. Content: You are to generate a response based solely on the context provided. Do not repeat the prompt\n\n \
    # Role: User. Content: {context}. Question: {question}\n\n \
    # Role: Assistant. Content: Answer:"

    # prompt = f"Based on the context provided, generate a response to the following question:\n\n\
    # Context: {context}\n\nQuestion: {question}\n\nAnswer: "

    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

    # Tokenize the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generate the answer
    # outputs = model.generate(
    #     inputs,
    #     max_length=500,
    #     num_return_sequences=1,
    #     pad_token_id=tokenizer.eos_token_id,
    # )
    outputs = model.generate(
        inputs,
        top_k=50,  
        top_p=0.95,  
        max_length=500,  # Reduced max length
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,  # Increased no repeat n-gram size to reduce repetition
        early_stopping=True      # Enables early stopping to prevent long repetitive sequences
    )

    # Decode the generated text
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract the answer part from the generated text
    answer = answer.split("Answer:")[1].strip()
    return answer


# Example usage
context = (
    "Steve Jobs was a complex and compelling personality, a one-of-a-kind innovator whose career and life were marked by an intense passion for perfection and an unyielding drive to create revolutionary products. His charisma and vision inspired a legion of followers, and his insistence on end-to-end control over his products led to a series of groundbreaking innovations that transformed the tech industry. Jobs' approach to design, which combined aesthetics with functionality, resulted in products like the iPhone, iPad, and MacBook, which became cultural icons and set new standards in the industry. Despite his sometimes abrasive leadership style, Jobs' legacy is defined by his relentless pursuit of excellence and his ability to anticipate and shape consumer desires."
)
question = "How did Steve Jobs' insistence on end-to-end control over his products contribute to the success of innovations like the iPhone, iPad, and MacBook?"

answer = answer_question(question, context)
print("Answer:", answer)
