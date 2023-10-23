from flask import Flask, render_template, request, jsonify
import os
from src.utils.ask_question_to_pdf import ask_question_to_pdf, ask_qcm
from src.utils.ask_question_to_pdf import contexte

app = Flask(__name__)

remember_question = ""


@app.route("/")
def template():
    return render_template('index.html')


@app.route("/prompt", methods=['POST'])
def prompt():
    reponse = ask_question_to_pdf(request.form["prompt"])
    return {"answer": reponse}


@app.route("/question", methods=['GET'])
def pose_question():
    return {"answer": ask_question_to_pdf("Pose moi une question sur un détail du cours", False)}


@app.route("/answer", methods=['POST'])
def reponse_question():
    reponse = ask_question_to_pdf("Ma réponse est : " +
                                  request.form["prompt"] +
                                  ". Dis si elle est juste et le cas échéant" +
                                  " donne la réponse en pas plus de 3 phrases.")
    return {"answer": reponse}

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # Vérifiez si le fichier est présent dans la requête
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['pdf']

    # Assurez-vous que le fichier a un nom
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = 'filename.pdf'
        filepath = os.path.join('src/utils', filename)
        file.save(filepath)
        return jsonify({'success': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file format'}), 400

@app.route("/qcm", methods=["GET"])
def pose_qcm():
    reponse = ask_qcm()
    return {"answer": reponse}

@app.route("/load-chat", methods=["GET"])
def load_chat():
    return {"answer": contexte}