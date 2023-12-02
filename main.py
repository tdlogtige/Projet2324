from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
from src.utils.story_manager import *
from src.utils.QCM import ask_qcm_prime


app = Flask(__name__)
app.secret_key = 'une_cle_secrete'  # Nécessaire pour utiliser les sessions

remember_question = ""

@app.route("/")
def template():
    return render_template('index.html')


@app.route('/page_base.html')
def page_base():
    level = request.args.get('level')
    subject = request.args.get('subject')
    
    # Stocker les paramètres dans la session pour une utilisation ultérieure
    session['level'] = level
    session['subject'] = subject

    return render_template('page_base.html', level=level, subject=subject)


@app.route("/prompt", methods=['POST'])
def prompt():
    level = request.args.get('level', 'defaultLevel')
    subject = request.args.get('subject', 'defaultSubject')
    reponse = ask_question_to_pdf_perso(request.form["prompt"], level, subject)
    return {"answer": reponse}



@app.route("/question", methods=['GET'])
def pose_question():
    level = request.args.get('level', 'defaultLevel')
    subject = request.args.get('subject', 'defaultSubject')
    return {"answer": ask_question_to_pdf_perso("Pose moi une question sur un détail du cours pour mon niveau et ce sujet", False, level, subject)}


@app.route("/answer", methods=['POST'])
def reponse_question():
    level = request.args.get('level', 'defaultLevel')
    subject = request.args.get('subject', 'defaultSubject')
    reponse = ask_question_to_pdf_perso("Ma réponse est : " + request.form["prompt"] +
                                  ". Dis si elle est juste et le cas échéant donne la réponse en pas plus de 3 phrases.", level, subject)
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
    # Récupérer les paramètres de la session
    level = session.get('level')
    subject = session.get('subject')
    reponse = ask_qcm_perso(level, subject)
    return {"answer": reponse}


@app.route("/load-chat", methods=["GET"])
def load_chat():
    return {"answer": contexte}


