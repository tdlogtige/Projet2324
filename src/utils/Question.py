import openai

def gpt3_completion(entree_utilisateur, ctx, save=True):
    global contexte
    contexte = ctx
    contexte += [{"role": "user", "content": entree_utilisateur+"en code latex et sans rien dire à propos de latex"}]
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=contexte.copy(),
    )["choices"][0]["message"]["content"]

    contexte += [{"role": "assistant", "content": res}]

    with open("contexte.txt", "a", encoding="utf-8") as sauvegarde:
        sauvegarde.write("§u:"+entree_utilisateur + "\n§a:" + res + "\n")

    return res



def gpt3_completion_perso(level, subject, question, contexte, ancienne_reponse_gpt):
    role_content = f"Tu es un professeur particulier qui pose des questions de {subject} au niveau {level} sur le cours suivant : DEBUT{contexte} FIN. Reste dans le contexte du programme de classe de ton élève. Sois rigoureux avec ton élève."

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_content},
            {"role": "assistant", "content": ancienne_reponse_gpt + "en code latex et sans rien dire de latex"},
            {"role": "user", "content": question},
        ],
    )["choices"][0]["message"]["content"]
