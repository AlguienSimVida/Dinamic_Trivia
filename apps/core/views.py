from django.shortcuts import render
from decouple import config
import openai
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time
openai.api_key = config("OPENAI_API_KEY")

@csrf_exempt
def generate_trivia(request, retries=5):
    if request.method == "POST":
        topic = request.POST.get("topic")
        difficulty = request.POST.get("difficulty")
        
        prompt = f"Genera una trivia sobre el tema '{topic}' con un grado de dificultad '{difficulty}'."
        
        for _ in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un asistente que se limita a crear trivias con el tema dado, el grado de dificultad solicitado y no pases las respuestas de la trivia y solo hazla de 3 preguntas.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )
                trivia_text = response.choices[0].message['content'].strip()
                questions = trivia_text.split('\n\n')
                structured_questions = []
                for question in questions:
                    parts = question.split('\n')
                    if len(parts) > 1:
                        structured_questions.append({
                            'text': parts[0],
                            'answers': parts[1:]
                        })
                request.session['questions'] = structured_questions
                return render(request, 'pages/trivia.html', {'questions': structured_questions})
                
            except openai.error.RateLimitError:
                time.sleep(2 ** (5 - retries))
                retries -= 1

            except openai.error.OpenAIError as e:
                return render(request, 'pages/trivia.html', {'error': f"Error en la solicitud: {e}"})

    return render(request, 'pages/trivia.html')
        

@csrf_exempt
def verify_answers(request):
    if request.method == "POST":
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                user_answers[key] = value
        
        questions = request.session.get('questions', [])
        print(questions)
        correct_answers = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            user_answer = user_answers.get(f'question_{i+1}')
            prompt = f"Pregunta: {question['text']}\nRespuesta del usuario: {user_answer}\n¿Es correcta esta respuesta? Responde solo con 'Sí' o 'No'."
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un asistente que verifica respuestas de trivia.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )
                verification = response.choices[0].message['content'].strip().lower()
                print(f"Prompt: {prompt}")
                print(f"Verification: {verification}")
                if 'sí' in verification:
                    correct_answers += 1

            except openai.error.OpenAIError as e:
                return render(request, 'pages/trivia_result.html', {'error': f"Error en la verificación: {e}"})
        
        score = f"{correct_answers} de {total_questions} respuestas correctas"
        return render(request, 'pages/trivia_result.html', {'score': score, 'total_questions': total_questions})

    return redirect('generate_trivia')