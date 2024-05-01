import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import narratorweb

app = Flask(__name__)
firstTime = True
#new
@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory('narrationweb', filename)

@app.route('/')
def home():
    return render_template('narrator_output.html')
@app.route('/tab2')
def tab2():
    # Use the same 'narrator_output.html' template for Tab 2
    return render_template('narrator_output.html', tab_name='Tab 2')

@app.route('/tab3')
def tab3():
    # Use the same 'narrator_output.html' template for Tab 3
    return render_template('aboutus.html', tab_name='Tab 3')
#new
@app.route('/run-narrator')
def run_narrator():
    image_path = os.path.join(os.getcwd(), 'images/img.jpg')  # Path to the image
    analysis, audio_path = narratorweb.main(image_path)
    return render_template('narrator_output.html', analysis=analysis, audio_path=audio_path)

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            image.save(os.path.join('images', 'img.jpg'))
            return redirect(url_for('run_narrator'))
    return render_template('narrator_output.html')

@app.route('/narration/<filename>')
def download_file(filename):
    return send_from_directory('narration', filename)


@app.route('/change-voice', methods=['POST'])
def change_voice():
    # Perform the action to change the voice based on `selected_voice`
    # For example, update a global variable, a session variable, or a database entry
    narratorweb.change_voice(request.form['voice'])

if __name__ == '__main__':
    app.run(debug=True)
