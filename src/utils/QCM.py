import openai
import json
from src.utils.init_db import db as database
from flask import jsonify
from bson import json_util
import json



def parse_json(data):
    return json.loads(json_util.dumps(data))


collection = database.answer


def add_answer(qcm):
    collection.insert_one(parse_json(qcm))
    return jsonify({"message": "Document ajouté avec succès"}), 201


def update_student_feedback(question_id, feedback):
    if feedback == 'thumb_up':
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.0": 1}})
    if feedback == 'thumb_down':
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.1": -1}})
    return jsonify({"message": "Document modifié avec succès"}), 201
        

def update_difficulty(question_id, difficulty):
    if difficulty == "très facile":
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.0": 1}})
    if difficulty == "facile":
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.1": 1}})
    if difficulty == "moyen":
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.2": 1}})
    if difficulty == "difficile":
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.3": 1}})
    if difficulty == "très difficile":
        collection.update_one({"_id": ObjectId(question_id)},{"$inc": {"student_feedback.4": 1}})


def gpt4_completion_qcm(question, contexte, ancienne_reponse_gpt):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": contexte},
            {"role": "assistant", "content": ancienne_reponse_gpt+"en code latex et sans rien dire de latex"},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]


nb_questions_generees = 3


def ask_qcm_prime(subject,level, prompt):
    contexte = f'L objectif est de faire réviser l élève sur des cours de {subject} de classe de {level}, en te prenant comme sujet {prompt}. Utilise latex pour les équations mathématiques'
    ReponseString = "[" + gpt4_completion_qcm(
        'Génère un qcm de ' + str(nb_questions_generees) + ' questions avec 1 réponse juste et 3 réponses fausses à partir du contexte fourni. Je veux que tu renvoies le qcm sous la forme suivante : {"question": "Quelle est la capitale de la France ?","choices": ["Berlin", "Madrid", "Lisbonne", "Paris"],"correct": 4} Tu renvoies juste la réponse sous cette forme, tu ne renvoies rien d autre. Tu sépares les résultats par des virgules',
        contexte,
        "",
    ) + "]"
    response_json=json.loads(ReponseString)

    for k in range(nb_questions_generees):
        response_json[k]['correct'] -= 1
        response_json[k]['level'] = level
        response_json[k]['subject'] = subject

    return response_json


def get_question_from_db(level, subject, nb_questions):
    # Récupérer deux questions correspondant au niveau et au sujet
    questions_cursor = collection.find({"level": level, "subject": subject}).limit(nb_questions)

    # Convertir le curseur en liste
    questions = list(questions_cursor)

    # Vérifier si des questions ont été trouvées
    if questions:
        formatted_questions = []
        for question_data in questions:
            formatted_question = {
                "question": question_data["question"],
                "choices": question_data["choices"],
                "correct": question_data["correct"],
                "id": str(question_data["_id"])
            }
            print(question_data["_id"])
            formatted_questions.append(formatted_question)
        return formatted_questions
    else:
        return {"error": "Aucune question trouvée pour ce niveau et sujet"}

