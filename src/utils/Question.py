import openai

def gpt3_completion(entree_utilisateur, ctx, save=True):
    global contexte
    contexte = ctx
    contexte += [{"role": "user", "content": entree_utilisateur}]
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=contexte.copy(),
    )["choices"][0]["message"]["content"]

    contexte += [{"role": "assistant", "content": res}]

    with open("contexte.txt", "a", encoding="utf-8") as sauvegarde:
        sauvegarde.write("§u:"+entree_utilisateur + "\n§a:" + res + "\n")

    return res