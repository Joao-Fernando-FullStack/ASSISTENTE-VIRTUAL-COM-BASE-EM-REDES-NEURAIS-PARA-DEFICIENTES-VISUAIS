import tensorflow as tf
import numpy as np

# Dados de treinamento (exemplo simples de diálogo)
training_data = [
    ("Olá!", "Olá! Como posso ajudar?"),
    ("Qual é o clima hoje?", "O clima está ensolarado."),
    ("O que você está fazendo?", "Estou aqui para responder suas perguntas."),
    ("Tchau!", "Até mais!"),
]

# Criar dicionários de mapeamento de palavras para índices e vice-versa
word_to_index = {word: idx for idx, (input_text, _) in enumerate(training_data) for word in input_text.split()}
index_to_word = {idx: word for word, idx in word_to_index.items()}

# Preparar dados de treinamento
X_train = np.array([[word_to_index[word] for word in input_text.split()] for input_text, _ in training_data])
y_train = np.array([[word_to_index[word] for word in output_text.split()] for _, output_text in training_data])

# Parâmetros da rede neural
vocab_size = len(word_to_index)
embedding_dim = 16
hidden_units = 32

# Criar modelo RNN
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=X_train.shape[1]),
    tf.keras.layers.SimpleRNN(hidden_units, return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(vocab_size, activation='softmax'))
])

# Compilar o modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Treinar o modelo
model.fit(X_train, y_train, epochs=100)

# Função para gerar respostas
def generate_response(input_text):
    input_seq = np.array([[word_to_index[word] for word in input_text.split()]])
    output_seq = model.predict(input_seq)
    output_text = ' '.join([index_to_word[idx] for idx in output_seq[0].argmax(axis=-1)])
    return output_text


# Testar o assistente virtual
user_input = "Qual é o clima hoje?"
response = generate_response(user_input)
print(f"Resposta do assistente: {response}")




