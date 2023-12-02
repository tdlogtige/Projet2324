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




def gpt4_completion_qcm(question, contexte, ancienne_reponse_gpt):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": contexte},
            {"role": "assistant", "content": ancienne_reponse_gpt+"en code latex et sans rien dire de latex"},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]


nombre_questions = 2


def ask_qcm_prime(subject,level):
    contexte = f'L objectif est de faire réviser l élève sur des cours de {subject} de classe de {level}. Utilise latex pour les équations mathématiques'
    ReponseString = "[" + gpt4_completion_qcm(
        'Génère un qcm de ' + str(nombre_questions) + ' questions avec 1 réponse juste et 3 réponses fausses à partir du contexte fourni. Je veux que tu renvoies le qcm sous la forme suivante : {"question": "Quelle est la capitale de la France ?","choices": ["Berlin", "Madrid", "Lisbonne", "Paris"],"correct": 4} Tu renvoies juste la réponse sous cette forme, tu ne renvoies rien d autre. Tu sépares les résultats par des virgules',
        contexte,
        "",
    ) + "]"
    response_json=json.loads(ReponseString)

    for k in range(nombre_questions):
        response_json[k]['correct'] -= 1
        response_json[k]['level'] = level
        response_json[k]['subject'] = subject
        add_answer(response_json[k])

    return response_json