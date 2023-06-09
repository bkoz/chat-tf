#
# inference.py
#
# Load the train model and make an inference.
#
import numpy as np
import tensorflow as tf
from tensorflow import keras

Tokenizer = tf.keras.preprocessing.text.Tokenizer
pad_sequences = tf.keras.preprocessing.sequence.pad_sequences

# Load your text data
# Here I'm simply loading a relative file which contains the array of data (data.py)
from data import text_data_arr

# Tokenize the text
tokenizer = Tokenizer(char_level=True, lower=True)
tokenizer.fit_on_texts(text_data_arr)

sequence_length = 100

model = keras.models.load_model("model/1")
model.summary()

# Evaluate the model and generate text:
def generate_text(seed_text, model, tokenizer, sequence_length, num_chars_to_generate):
    generated_text = seed_text

    for _ in range(num_chars_to_generate):
        token_list = tokenizer.texts_to_sequences([generated_text])
        token_list = pad_sequences(token_list, maxlen=sequence_length, padding="pre")
        predicted_probs = model.predict(token_list, verbose=0)
        predicted_token = np.argmax(predicted_probs, axis=-1)[0]  # Get the index of the predicted token

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_token:
                output_word = word
                break

        generated_text += output_word

    return generated_text

seed_text = "John: How are you, Mike?"

print("Generating text...")
generated_text = generate_text(seed_text, model, tokenizer, sequence_length, num_chars_to_generate=800)
print(generated_text)

