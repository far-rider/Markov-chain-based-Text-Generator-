import random
import re
from collections import defaultdict

def preprocess_text(text):
    return re.findall(r"\b\w+\b|[.,!?;]", text)

def build_markov_chain(text, order=2):
    words = preprocess_text(text)
    markov_chain = defaultdict(list)
    
    for i in range(len(words) - order):
        key = tuple(words[i:i + order])  # Use 'order' words as key
        next_word = words[i + order]
        markov_chain[key].append(next_word)
    
    return markov_chain

def find_best_seed(markov_chain, seed):
    seed_words = tuple(preprocess_text(seed))

    # First, check if the seed is directly in the Markov chain
    if seed_words in markov_chain:
        return seed_words  # Found exact match!

    # Otherwise, find the closest match based on the first word
    for key in markov_chain.keys():
        if key[:len(seed_words)] == seed_words:
            return key  # Found a close match

    return random.choice(list(markov_chain.keys()))  # Fallback to a random seed

def generate_text(markov_chain, length=50, seed=None, randomness=True):
    """Generates text using a Markov chain."""
    if not markov_chain:
        return "Error: Markov chain is empty."

    if seed is None:
        seed = random.choice(list(markov_chain.keys()))
    else:
        seed = tuple(preprocess_text(seed))
        seed = find_best_seed(markov_chain, ' '.join(seed))  # Now correctly finds best match

    generated_words = list(seed)

    for _ in range(length):
        key = tuple(generated_words[-len(seed):])
        if key in markov_chain:
            next_word = random.choice(markov_chain[key]) if randomness else markov_chain[key][0]
            generated_words.append(next_word)
        else:
            break  # Stop if we reach an unknown state
    
    return ' '.join(generated_words)

if __name__ == "__main__":
    sample_text = (
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. "
        "It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."
        "It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"
        "Once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it. "
        "And what is the use of a book, thought Alice, without pictures or conversation?"
    )

    markov_chain = build_markov_chain(sample_text, order=2)

    user_seed = input("Enter a starting word or phrase: ")
    generated_text = generate_text(markov_chain, length=20, seed=user_seed)
    print("\nGenerated Text:\n", generated_text)