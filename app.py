from flask import Flask, request, jsonify, render_template
import openai
import speech_recognition as sr
import pyttsx3

# Initialize Flask app
app = Flask(__name__)

# OpenAI API Key
openai.api_key = 'your-api-key'

def speak(text):
    """Convert the text to speech using pyttsx3."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def listen():
    """Listen for voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question...")
        audio = recognizer.listen(source)
        
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "Sorry, I could not understand your speech. Could you please repeat?"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return "Sorry, I couldn't reach the speech recognition service."

def get_gpt_response(query):
    """Get a response from OpenAI's GPT-3 (Chat Model) for the given query."""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    print("Serving the front-end...")
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    print("Processing voice input...")
    query = listen()
    
    if query:
        print(f"User said: {query}")
        response = get_gpt_response(query)
        print(f"GPT-3 says: {response}")
        speak(response)
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No input detected."})

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)