import pyttsx3
import base64
import os

class AudioEngine:
    def __init__(self):
        # Initialize pyttsx3
        self.engine = pyttsx3.init()
        # Set properties (optional)
        self.engine.setProperty('rate', 150)  # Speed percent (can go over 100)
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

    def generate_audio(self, text: str, mode: str = "default") -> str:
        """
        Generates audio from text and returns it as a base64 encoded string.
        Uses a temporary file to save audio, reads it, then deletes it.
        """
        temp_file = "response_audio.wav"
        
        # Adjust voice/tone based on mode (Basic implementation for SAPI5)
        voices = self.engine.getProperty('voices')
        if mode == "therapist":
            self.engine.setProperty('rate', 130) # Slower, more soothing
            # Try to find a female voice if available, often at index 1 on Windows
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
        elif mode == "stranger":
             self.engine.setProperty('rate', 145)
             self.engine.setProperty('voice', voices[0].id)
        else:
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('voice', voices[0].id)

        try:
            # Save to file
            self.engine.save_to_file(text, temp_file)
            self.engine.runAndWait()
            
            # Read file and encode to base64
            with open(temp_file, "rb") as audio_file:
                audio_bytes = audio_file.read()
                base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            
            return base64_audio
        except Exception as e:
            print(f"Error generating audio: {e}")
            return ""
        finally:
            # Clean up
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

if __name__ == "__main__":
    ae = AudioEngine()
    b64 = ae.generate_audio("Hello, this is a test of the emergency broadcast system.", "therapist")
    print(f"Generated {len(b64)} bytes of base64 audio.")
