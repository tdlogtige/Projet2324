from flask import Flask, render_template, request, jsonify
import os
from src.utils.story_manager import *
from src.utils.QCM import get_question_from_db, add_answer, ask_qcm_prime, database


app = Flask(__name__)

remember_question = ""



@app.route("/")
def template():
    return render_template('index.html')


@app.route('/page_base.html')
def page_base():
    level = request.args.get('level')
    subject = request.args.get('subject')
    return render_template('page_base.html', level=level, subject=subject)


@app.route('/create_question.html', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        selected_class = request.form['class']
        selected_subject = request.form['subject']
        selected_chapter = request.form['chapter']
        prompt = request.form['prompt']

        qcm_questions = ask_qcm_prime(selected_subject, selected_class, selected_chapter, prompt)

        # Ajouter un indice à chaque question et à chaque choix
        for i, question in enumerate(qcm_questions):
            question['index'] = i
            for j, choice in enumerate(question['choices']):
                choice = {'index': j, 'text': choice}
                question['choices'][j] = choice

        return render_template('question_display.html', questions=qcm_questions, selected_class=selected_class, selected_subject=selected_subject, selected_chapter=selected_chapter)

    return render_template('create_question.html')


@app.route('/get_chapters', methods=['GET'])
def get_chapters():
    selected_class = request.args.get('class')
    selected_subject = request.args.get('subject')

    # Collection chapitres de Mongo
    collection = database.chapitres

    # Récupérer les chapitres pour la classe et la matière sélectionnées
    document = collection.find_one({"classe": selected_class})
    if document and selected_subject in document['matières']:
        chapters = document['matières'][selected_subject]
    else:
        chapters = []

    return jsonify(chapters)

@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    data = request.json
    selected_class = data['class']
    selected_subject = data['subject']
    new_chapter = data['new_chapter']

    # Collection chapitres de Mongo
    collection = database.chapitres

    # Ajouter le nouveau chapitre à la base de données
    query = {"classe": selected_class}
    update = {"$addToSet": {f"matières.{selected_subject}": new_chapter}}
    collection.update_one(query, update)

    return jsonify({"success": True})


@app.route('/add_question', methods=['POST'])
def add_question():
    
    question_data = request.json

    add_answer(question_data)

    return jsonify({'status': 'success'})


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
    chapter = request.args.get('chapter')  
    nb_questions = request.args.get('nb_questions', type=int, default=2)  # Valeur par défaut est 2
    qcm_response = get_question_from_db(level, subject, chapter, nb_questions)
    return {"answer": qcm_response}



