import os
import base64
import time
import simpleaudio as sa
import errno
from openai import OpenAI
from elevenlabs import generate, set_api_key
USE_MOCK = False
client = OpenAI()
set_api_key(os.environ.get("ELEVENLABS_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_audio(text, dir_path):
    if USE_MOCK:
        # Return a path to a pre-generated dummy audio file
        return "audio.wav"
    audio = generate(text, voice=os.environ.get("ELEVENLABS_VOICE_ID"))
    file_name = "audio.wav"  # You might want a unique name for each file
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, "wb") as f:
        f.write(audio)

    # Return only the relative path
    return file_name
def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ],
        }
    ]

def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """,
            },
        ] + script + generate_new_line(base64_image),
        max_tokens=500
    )
    response_text = response.choices[0].message.content
    return response_text

def main(image_path):
    if USE_MOCK:
        # Return a path to a pre-generated dummy audio file
        return "Ultrices gravida dictum fusce ut placerat. Leo vel orci porta non. Sollicitudin nibh sit amet commodo nulla facilisi nullam. Hac habitasse platea dictumst quisque sagittis purus sit amet volutpat. Augue lacus viverra vitae congue eu consequat ac felis donec. Et pharetra pharetra massa massa ultricies. Urna cursus eget nunc scelerisque viverra. Risus nec feugiat in fermentum. Commodo ullamcorper a lacus vestibulum. Eu nisl nunc mi ipsum. Iaculis eu non diam phasellus vestibulum lorem sed risus ultricies. Tincidunt arcu non sodales neque sodales ut etiam. Ultrices neque ornare aenean euismod elementum nisi quis eleifend quam. Non arcu risus quis varius quam quisque id. Mattis pellentesque id nibh tortor id. Molestie nunc non blandit massa enim nec dui nunc. Orci dapibus ultrices in iaculis nunc. Ultrices gravida dictum fusce ut placerat orci nulla. ","audio.wav"
    base64_image = encode_image(image_path)
    analysis = analyze_image(base64_image, [])

    # Ensure the directory for the narration exists
    dir_path = "narrationweb"  # Relative directory path
    os.makedirs(dir_path, exist_ok=True)

    audio_file_name = generate_audio(analysis, dir_path)
    return analysis, audio_file_name

