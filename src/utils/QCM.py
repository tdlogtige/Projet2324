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


def gpt4_completion_perso(level, subject, question):
    role_content = f"Tu es un professeur particulier qui pose des questions de {subject} au niveau {level}. Reste dans le contexte du programme de classe de ton élève. Sois rigoureux avec ton élève."

    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": role_content},
            #{"role": "assistant", "content": ancienne_reponse_gpt + "en code latex et sans rien dire de latex"},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]


def ask_qcm_perso(level, subject):
    ReponseString = gpt4_completion_perso(
        level,
        subject,
        'Génère un qcm de' + str(nombre_questions) + ' questions avec 1 réponse juste et 3 réponses fausses en respectant bien les consignes du contexte fourni, à savoir sur la matière {subject} et la classe {level}. Je veux que tu renvoies le qcm sous la forme suivante : {"answer": "Quelle est la capitale de la France ?","choices": ["Berlin", "Madrid", "Lisbonne", "Paris"],"correct": 4} Tu renvoies juste la réponse sous cette forme, tu ne renvoies rien d autre. Tu sépares les résultats par des virgules. Tu renvoies UNIQUEMENT sous le format que je t ai donne, tu ne dis rien d autre. '
#Pour les équations, tu peux écrire en code latex avec $. N oublies pas que tu dois poser une question en rapport avec la classe et la matière fournies dans le contexte.    
    )

    print(ReponseString)

    response_json=json.loads('[' + ReponseString + ']')

    for k in range(nombre_questions):
        response_json[k]['correct'] -= 1
        #add_answer(response_json[k])

    return response_json