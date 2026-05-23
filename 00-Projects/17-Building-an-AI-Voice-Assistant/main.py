import os
import tempfile
# Para grabar audio.
import sounddevice as sd
# Para guardar el audio en un fichero.
import soundfile as sf
# Para crear ficheros temporales
import openai
from dotenv import load_dotenv

load_dotenv()

# Coge de .env automáticamente el nombre: OPENAI_API_KEY
client = openai.OpenAI()

SAMPLE_RATE = 16000
MAX_DURATION = 30
SAMPLES = SAMPLE_RATE * MAX_DURATION


def record_audio() -> str:
    """Record from microphone, return path to temp WAV file."""
    input("Press Enter to start recording...")
    print("Recording...Press Enter to stop.")

    # Parámetros de rec
    #  Número de samples
    #  Ratio de samples por segundo
    #  Número de canales (1=mono, 2=stereo)
    #  dtype
    audio_data = sd.rec(SAMPLES,
                        samplerate=SAMPLE_RATE,
                        channels=1,
                        dtype="float64")

    # Cuando el usuario pulsó Intro para parar, venimos aquí.
    input()
    sd.stop()
    print("Recording stopped.")
    
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio_data, SAMPLE_RATE)
    return tmp.name


def transcribe(audio_path: str) -> str:
    """Send audio to OpenAI Whisper API and return the transcript."""
    with open(audio_path, 'rb') as file:
        output = client.audio.transcriptions.create(
            model='whisper-1',
            file=file,
            response_format='text')
    return output


def think(text: str) -> str:
    """Send text to GPT and return the response."""
    response = client.responses.create(
        model='gpt-5-nano',
        instructions="You are a helpful voice assistant. Keep responses short and conversational.",
        input=text)
    return response.output_text


def speak(text: str):
    """Convert text to speech and play it."""
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=text
    ) as response:
        response.stream_to_file(tmp.name)
        
    data, sr = sf.read(tmp.name)
    sd.play(data, sr)
    sd.wait()
    os.unlink(tmp.name)


audio_file = record_audio()
transcript = transcribe(audio_file)
print(f"\nYou said: {transcript}")
os.unlink(audio_file)

reply = think(transcript)
print(f"AI: {reply}")

speak(reply)