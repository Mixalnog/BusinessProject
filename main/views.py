from django.shortcuts import render
from django.http import HttpResponse

import pytgpt.phind as phind
from browser_history.browsers import Chrome
from googletrans import Translator

def history(): # здесь можно будет указывать, какой браузер юзать
    browser = Chrome()
    history = browser.fetch_history().histories
    headers = [i[2] for i in history]
    return headers

bot = phind.PHIND(is_conversation=False)
tr = Translator()
history = history()
history = "; ".join([tr.translate(i).text for i in history])[:-2]

prompt_of_history = f"You are given the names of the sites separated by the sign '; ': {history}. Identify from 1 to 10 hobbies of the person who visited the sites with these titles. The hobby must match at least one of the site names. If your hobby matches the name of a website, product, or company, don't write it. If a hobby doesn't fit, don't write it. It is not necessary to specify all 10 hobbies. Print the result separated by commas. The answer should contain nothing but a list of hobbies separated by commas."
categories = bot.chat(prompt_of_history)

categories = tr.translate(categories, src="ru", dest="en")


def index(request):
    return render(request, 'main/index.html')

def testing(request):
    return render(request, 'main/core.html', {'variable': history})
def output(request):
    input = request.POST.get('user_input')

    question = tr.translate(input, src="ru", dest="en")
    prompt = f"Write the answer to the question: '{question.text}'. The answer must be precise and clear. Add from 1 to 3 examples from the following categories: {categories}. It is not necessary to specify all 3 examples. If the example does not fall into any of the categories, do not write it. If the example does not match the logic of your answer to the question, do not write it. Each example should not contain more than 3 sentences."

    resp = bot.chat(prompt)
    resp_trans = tr.translate(resp, src="en", dest="ru")

    formatted_txt = resp_trans.text.replace('.', '. ')

    return render(request, 'main/output.html', {'variable': formatted_txt})

