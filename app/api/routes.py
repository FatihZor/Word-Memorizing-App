import random
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app import db
from app.api.models import Word, WordDefinition, Library, Point
from app.utils.word_utils import add_word_point

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/add-to-library', methods=['POST'])
@login_required
def add_to_library():
    if request.method == 'POST':
        word_id = request.json.get('word_id')
        word = Word.query.filter_by(id=int(word_id)).first()
        if word:
            try:
                library = Library(
                    user_id=current_user.id,
                    word_id=word.id
                )
                db.session.add(library)
                db.session.commit()
                return jsonify({'success': True})
            except:
                return jsonify({'success': False})
        else:
            return jsonify({'success': False})
    return jsonify({})

@api.route('/get-question', methods=['GET'])
@login_required
def get_question():
    if request.method == 'GET':
        words = Word.get_all()
        answers = []
        correct_answer = words.pop(random.randint(0, len(words) - 1))
        wrong_answer_1 = words.pop(random.randint(0, len(words) - 1))
        wrong_answer_2 = words.pop(random.randint(0, len(words) - 1))
        add_word_point(user_id=current_user.id, word_id=correct_answer.id, point=1, reason="practice")
        add_word_point(user_id=current_user.id, word_id=wrong_answer_1.id, point=1, reason="practice")
        add_word_point(user_id=current_user.id, word_id=wrong_answer_2.id, point=1, reason="practice")
        answers.append(correct_answer.word)
        answers.append(wrong_answer_1.word)
        answers.append(wrong_answer_2.word)
        random.shuffle(answers)
        definitions = []        
        for definition in Word.get_definitions(correct_answer.id):
            definitions.append(definition)
        question = random.choice(definitions)
        add_word_point(user_id=current_user.id, word_id=definition.word.id, point=-2, reason="question")
        data = {
            'question': question.definition,
            'answers': answers,
            'question_id': question.id,
            'success': True
        }
        return jsonify(data)
    return jsonify({'success': False})

@api.route('/check-answer', methods=['POST'])
@login_required
def check_answer():
    if request.method == 'POST':
        answer = request.json.get('answer')
        question_id = request.json.get('question_id')
        print(answer, question_id)
        question = WordDefinition.query.filter_by(id=question_id).first()
        if question:
            if question.word.word == answer:
                add_word_point(user_id=current_user.id, word_id=question.word.id, point=2, reason="correct")
                return jsonify({'success': True, 'message': 'Correct! (2 Point for Word)'})
            else:
                add_word_point(user_id=current_user.id, word_id=question.word.id, point=-2, reason="incorrect")
                return jsonify({'success': False, 'message': 'Incorrect! (-2 Point for Word)'})
       
    return jsonify({'success': False})

@api.route('/get-point', methods=['POST'])
@login_required
def get_point():
    if request.method == 'POST':
        word_id = request.json.get('word_id')
        print(word_id)
        word = Word.query.filter_by(id=word_id).first()
        if word:
            point = Point.get_points(word_id=word.id, user_id=current_user.id)
            return jsonify({'success': True, 'word': word.word, 'point': point})
    return jsonify({'success': False})