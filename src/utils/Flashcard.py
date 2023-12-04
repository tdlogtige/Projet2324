class Flashcard:

    def __init__(self, preprompt):
        self._preprompt = preprompt
    def generate_new(self, existing):
        prec=""
        for i in existing:
            prec+=i.question+", "
        res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": self._preprompt},{"role": "user", "content":"Génère une question sur le cours, différente de celles-ci : "+prec }].copy(),
    )["choices"][0]["message"]["content"]
        self._question=res
        self._answer=openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": self._preprompt},{"role": "user", "content":res }].copy(),
    )["choices"][0]["message"]["content"]

    @property
    def question(self):
        return self._question
    @question.setter
    def question(self, value):
        self._question=value
    
    @property
    def answer(self):
        return self._answer
    @answer.setter
    def answer(self, value):
        self._answer=value