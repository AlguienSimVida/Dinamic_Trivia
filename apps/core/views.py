# from django.shortcuts import render
# from decouple import config
# import openai
# from django.shortcuts import redirect, render
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# import json
# import time

# openai.api_key = config("OPENAI_API_KEY")


# @csrf_exempt
# def generate_trivia(request, retries=5):
#     if request.method == "POST":
#         topic = request.POST.get("topic")
#         difficulty = request.POST.get("difficulty")

#         prompt = (
#             f"Genera una trivia sobre el tema '{topic}' con un grado de dificultad '{difficulty}'. "
#             "La trivia debe contener exactamente 3 preguntas y seguir estrictamente la siguiente estructura: \n\n"
#             "{\n"
#             '    "question_1": {\n'
#             '        "question": "Texto de la pregunta",\n'
#             '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
#             '        "correct_answer": "Opción correcta"\n'
#             "    },\n"
#             '    "question_2": {\n'
#             '        "question": "Texto de la pregunta",\n'
#             '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
#             '        "correct_answer": "Opción correcta"\n'
#             "    },\n"
#             '    "question_3": {\n'
#             '        "question": "Texto de la pregunta",\n'
#             '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
#             '        "correct_answer": "Opción correcta"\n'
#             "    }\n"
#             "}"
#         )

#         for _ in range(retries):
#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": "Eres un asistente especializado en crear trivias basadas en el tema y nivel de dificultad dados. Sigue estrictamente la estructura proporcionada y no incluyas explicaciones adicionales.",
#                         },
#                         {"role": "user", "content": prompt},
#                     ],
#                 )

#                 trivia_dict = json.loads(response.choices[0].message["content"].strip())
#                 request.session["questions"] = trivia_dict
#                 return render(request, "pages/trivia.html", {"questions": trivia_dict})

#             except openai.error.RateLimitError:
#                 time.sleep(2 ** (5 - retries))
#                 retries -= 1

#             except openai.error.OpenAIError as e:
#                 return render(
#                     request,
#                     "pages/trivia.html",
#                     {"error": f"Error en la solicitud: {e}"},
#                 )

#     return render(request, "pages/trivia.html")


# @csrf_exempt
# def verify_answers(request):
#     if request.method == "POST":
#         user_answers = {}
#         for key, value in request.POST.items():
#             if key.startswith("question_"):
#                 user_answers[key] = value

#         questions = request.session.get("questions", [])
#         print(questions)
#         correct_answers = 0
#         total_questions = len(questions)

#         for i, question in enumerate(questions):
#             user_answer = user_answers.get(f"question_{i+1}")
#             prompt = f"Pregunta: {question['text']}\nRespuesta del usuario: {user_answer}\n¿Es correcta esta respuesta? Responde solo con 'Sí' o 'No'."

#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": "Eres un asistente que verifica respuestas de trivia.",
#                         },
#                         {"role": "user", "content": prompt},
#                     ],
#                 )
#                 verification = response.choices[0].message["content"].strip().lower()
#                 print(f"Prompt: {prompt}")
#                 print(f"Verification: {verification}")
#                 if "sí" in verification:
#                     correct_answers += 1

#             except openai.error.OpenAIError as e:
#                 return render(
#                     request,
#                     "pages/trivia_result.html",
#                     {"error": f"Error en la verificación: {e}"},
#                 )

#         score = f"{correct_answers} de {total_questions} respuestas correctas"
#         return render(
#             request,
#             "pages/trivia_result.html",
#             {"score": score, "total_questions": total_questions},
#         )

#     return redirect("generate_trivia")
import json
import time
from django.shortcuts import render, redirect
import openai


def generate_trivia(request, retries=5):
    if request.method == "POST":
        topic = request.POST.get("topic")
        difficulty = request.POST.get("difficulty")

        prompt = (
            f"Genera una trivia sobre el tema '{topic}' con un grado de dificultad '{difficulty}'. "
            "La trivia debe contener exactamente 3 preguntas y seguir estrictamente la siguiente estructura: \n\n"
            "{\n"
            '    "question_1": {\n'
            '        "question": "Texto de la pregunta",\n'
            '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
            '        "correct_answer": "Opción correcta"\n'
            "    },\n"
            '    "question_2": {\n'
            '        "question": "Texto de la pregunta",\n'
            '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
            '        "correct_answer": "Opción correcta"\n'
            "    },\n"
            '    "question_3": {\n'
            '        "question": "Texto de la pregunta",\n'
            '        "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],\n'
            '        "correct_answer": "Opción correcta"\n'
            "    }\n"
            "}"
        )

        for _ in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un asistente especializado en crear trivias basadas en el tema y nivel de dificultad dados. Sigue estrictamente la estructura proporcionada y no incluyas explicaciones adicionales.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )

                trivia_dict = json.loads(response.choices[0].message["content"].strip())
                questions = [
                    {
                        "id": key,
                        "question": value["question"],
                        "options": value["options"],
                        "correct_answer": value["correct_answer"],
                    }
                    for key, value in trivia_dict.items()
                ]
                request.session["questions"] = questions
                request.session["current_question_index"] = 0
                request.session["results"] = []
                return redirect("show_question")

            except openai.error.RateLimitError:
                time.sleep(2 ** (5 - retries))
                retries -= 1

            except openai.error.OpenAIError as e:
                return render(
                    request,
                    "pages/trivia.html",
                    {"error": f"Error en la solicitud: {e}"},
                )

    return render(request, "pages/trivia.html")


def show_question(request):
    questions = request.session.get("questions", [])
    current_index = request.session.get("current_question_index", 0)

    if current_index < len(questions):
        current_question = questions[current_index]
        return render(
            request,
            "pages/trivia.html",
            {
                "questions": None,
                "current_question": current_question,
                "current_question_number": current_index + 1,
                "total_questions": len(questions),
            },
        )
    else:
        return redirect("show_results")


def next_question(request):
    if request.method == "POST":
        answer = request.POST.get("answer")
        questions = request.session.get("questions", [])
        current_index = request.session.get("current_question_index", 0)

        if current_index < len(questions):
            current_question = questions[current_index]
            request.session["results"].append(
                {
                    "question": current_question["question"],
                    "options": current_question["options"],
                    "correct_answer": current_question["correct_answer"],
                    "user_answer": answer,
                }
            )
            request.session["current_question_index"] = current_index + 1
            return redirect("show_question")

    return redirect("show_results")


def show_results(request):
    results = request.session.get("results", [])
    correct_answers = sum(1 for r in results if r["user_answer"] == r["correct_answer"])
    return render(
        request,
        "pages/trivia.html",
        {
            "questions": None,
            "results": results,
            "correct_answers": correct_answers,
            "total_questions": len(results),
        },
    )
