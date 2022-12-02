from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

from app import db
from app.api.models import Word, WordDefinition, Library
from app.utils.word_utils import search_word, add_word_point

@main.route('/')
@main.route('/index')
@login_required
def index():
    count = Library.get_count(current_user.id)
    return render_template('main/index.html', count=count)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        request_word = request.form.get('word')
        word = Word.query.filter_by(word=request_word).first()
        if word:
            word_in_library = Library.word_exists(current_user.id, word.id)
            word_definitions = WordDefinition.query.filter_by(word_id=word.id).all()
            add_word_point(user_id=current_user.id, word_id=word.id, point=1, reason="search")
            return render_template('main/search.html', word=word, word_definitions=word_definitions, word_in_library=word_in_library)
        else:
            try:
                response = search_word(request_word)
                if response:
                    word = Word(
                        word=response['word'],
                    )
                    db.session.add(word)
                    db.session.commit()
                    word_in_library = Library.word_exists(current_user.id, word.id)
                    for definition in response['results']:
                        word_definition = WordDefinition(
                            word_id=word.id,
                            definition=definition['definition'],
                            part_of_speech=definition['partOfSpeech']
                        )
                        db.session.add(word_definition)
                        db.session.commit()
                    add_word_point(user_id=current_user.id, word_id=word.id, point=1, reason="search")
                    return render_template('main/search.html', word=word, word_definitions=Word.get_definitions(word.id), word_in_library=word_in_library)
            except:
                flash('word or word definition not found', category='error')
    return render_template('main/search.html', word="", word_definitions=[], word_in_library=False)

@main.route('/library')
@login_required
def library():
    library_items = Library.get_all(current_user.id)
    return render_template('main/library.html', library_items=library_items)

@main.route('/practice')
@login_required
def practice():
    count = Library.get_count(current_user.id)
    return render_template('main/practice.html', count=count)