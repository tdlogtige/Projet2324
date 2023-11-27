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

    # Ajoute les données dans MongoDB
    collection.insert_one(parse_json(qcm))

    return jsonify({"message": "Document ajouté avec succès"}), 201



def gpt3_completion_qcm(question, contexte, ancienne_reponse_gpt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": contexte},
            {"role": "assistant", "content": ancienne_reponse_gpt+"en code latex et sans rien dire de latex"},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]


nombre_questions = 2


def ask_qcm_prime(document):
    ReponseString = "[" + gpt3_completion_qcm(
        'Génère un qcm de ' + str(nombre_questions) + ' questions avec 1 réponse juste et 3 réponses fausses à partir du contexte fourni. Je veux que tu renvoies le qcm sous la forme suivante : {"answer": "Quelle est la capitale de la France ?","choices": ["Berlin", "Madrid", "Lisbonne", "Paris"],"correct": 4} Tu renvoies juste la réponse sous cette forme, tu ne renvoies rien d autre. Tu sépares les résultats par des virgules, en code latex avec $',
        document,
        "",
    ) + "]"
    response_json=json.loads(ReponseString)

    for k in range(nombre_questions):
        response_json[k]['correct'] -= 1
        #add_answer(response_json[k])

    return response_json