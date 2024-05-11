class TextToSpeechConverter:
    def __init__(self, api_key, output_dir="data"):
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)  # Ensure output directory exists
    def convert_to_speech(self, text, output_filename):
        # Define the full path for the output file
        output_file_path = self.output_dir / f"{output_filename}.mp3" 
        # Create the audio speech
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )
        # Save the binary audio content to the file
        response.stream_to_file(output_file_path)
        return None

