import openai
import json

def gpt3_completion_qcm(question, contexte, ancienne_reponse_gpt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": contexte},
            {"role": "assistant", "content": ancienne_reponse_gpt},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]



nombre_questions = 2

def ask_qcm_prime(document):
    ReponseString = "[" + gpt3_completion_qcm(
        'Génère un qcm de ' + str(nombre_questions) + ' questions avec 1 réponse juste et 3 réponses fausses à partir du contexte fourni. Je veux que tu renvoies le qcm sous la forme suivante : {"answer": "Quelle est la capitale de la France ?","choices": ["Berlin", "Madrid", "Lisbonne", "Paris"],"correct": 4} Tu renvoies juste la réponse sous cette forme, tu ne renvoies rien d autre. Tu sépares les résultats par des virgules',
        document,
        "",
    ) + "]"
    reponse_json=json.loads(ReponseString)

    for k in range(nombre_questions):
        reponse_json[k]['correct'] -= 1

    return reponse_json


