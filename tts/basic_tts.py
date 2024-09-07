from gtts import gTTS
# Text to convert to speech

def save_mp3(string):
# Create a gTTS object
    tts = gTTS(text=string, lang='en', slow=False)
    tts.save("output.mp3")

