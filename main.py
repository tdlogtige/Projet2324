from flask import Flask, render_template, request, jsonify
import os
from src.utils.story_manager import *
from src.utils.QCM import get_question_from_db


app = Flask(__name__)

remember_question = ""



@app.route("/")
def template():
    return render_template('index.html')


@app.route('/page_base.html')
def page_base():
    level = request.args.get('level')
    subject = request.args.get('subject')
    # Ici, vous pouvez ajouter une logique pour adapter le contenu en fonction de level et subject
    return render_template('page_base.html', level=level, subject=subject)


@app.route('/create_question.html', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        selected_class = request.form['class']
        selected_subject = request.form['subject']
        prompt = request.form['prompt']

        # Appeler la fonction ask_qcm_prime
        qcm_questions = ask_qcm_prime(selected_subject, selected_class, prompt)

        # Retourner les questions QCM à la page HTML
        return render_template('question_display.html', questions=qcm_questions)

    return render_template('create_question.html')



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


@app.route("/load-chat", methods=["GET"])
def load_chat():
    return {"answer": contexte}


@app.route("/qcm", methods=["GET"])
def pose_qcm():
    level = request.args.get('level')
    subject = request.args.get('subject')
    nb_questions = request.args.get('nb_questions', type=int, default=2)  # Valeur par défaut est 2
    qcm_response = get_question_from_db(level, subject, nb_questions)
    print(json.dumps(qcm_response))
    return {"answer": qcm_response}
