import sys
from openai import OpenAI

# Configura el cliente de OpenAI con la URL base de OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Reemplaza con tu API key de OpenRouter
)

def chat_with_openrouter():
    print("Bienvenido al chat con OpenRouter. Escribe 'salir' para terminar la conversación.")
    
    while True:
        # Solicita la entrada del usuario
        user_input = input("Tú: ")
        
        if user_input.lower() == 'salir':
            print("Saliendo del chat...")
            break
        
        # Envía la solicitud a OpenRouter con streaming
        response_stream = client.chat.completions.create(
            model="openai/gpt-4o",  # Puedes cambiar el modelo si lo deseas
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            stream=True  # Habilita el streaming
        )
        
        # Imprime la respuesta en tiempo real
        print("OpenRouter: ", end="")
        for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="")
                sys.stdout.flush()  # Asegura que el contenido se imprima inmediatamente
        print("\n")

if __name__ == "__main__":
    chat_with_openrouter()