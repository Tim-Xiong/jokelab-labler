from flask import Flask, render_template, request, jsonify, flash, session
from models import db, Joke, Visitor, Label, LabelSegment
from sqlalchemy import func
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def check_visitor():
    """
    Check if the visitor has a unique visitor ID in the session.
    If the 'visitor_id' is not present in the session, generate a new unique visitor ID,
    create a new Visitor object with this ID, add it to the database session, and commit the session.
    This function ensures that each visitor has a unique identifier for tracking purposes.
    """
    if 'visitor_id' not in session:
        session['visitor_id'] = str(uuid.uuid4())
        visitor = Visitor(id=session['visitor_id'])
        db.session.add(visitor)
        db.session.commit()

@app.route('/')
def index():
    """
    Render the index.html template.
    Returns:
        A rendered HTML template for the index page.
    """
    return render_template('index.html')

@app.route('/get_joke')
def get_joke():
    """
    Retrieve a joke that has the fewest labels and has not been labeled by the current visitor.
    This function queries the database to find a joke that has the fewest labels associated with it.
    It ensures that the joke has not been labeled by the current visitor (identified by session['visitor_id']).
    If no such joke is found, it returns a JSON response indicating that there are no more jokes to label.
    Returns:
        Response: A JSON response containing the joke's id and text if a joke is found.
                  If no joke is found, returns a JSON response with a message and a 404 status code.
    """
    # Get joke with fewest labels
    subquery = db.session.query(
        Label.joke_id,
        func.count(Label.id).label('label_count')
    ).group_by(Label.joke_id).subquery()
    
    joke = db.session.query(Joke).outerjoin(
        subquery, Joke.id == subquery.c.joke_id
    ).order_by(
        func.coalesce(subquery.c.label_count, 0)
    ).filter(
        ~Joke.labels.any(Label.visitor_id == session['visitor_id'])
    ).first()
    
    if not joke:
        return jsonify({'message': 'No more jokes to label'}), 404
    
    return jsonify({
        'id': joke.id,
        'text': joke.text
    })

@app.route('/submit_label', methods=['POST'])
def submit_label():
    """
    Handles the submission of a joke label.
    This function processes a JSON request containing a joke ID, segments, and a no_punchline flag.
    It validates the input, creates a new label, and optionally adds segments to the label.
    The label and segments are then saved to the database.
    Returns:
        Response: A JSON response indicating success or failure of the label submission.
    """
    data = request.json
    joke_id = data.get('joke_id')
    segments = data.get('segments', [])
    no_punchline = data.get('no_punchline', False)
    
    if not joke_id:
        return jsonify({'error': 'Missing joke ID'}), 400
    
    if not segments and not no_punchline:
        return jsonify({'error': 'Must either provide segments or mark as no punchline'}), 400
    
    # Create new label
    label = Label(
        joke_id=joke_id,
        visitor_id=session['visitor_id'],
        no_punchline=no_punchline,
        created_at=datetime.utcnow()
    )
    
    db.session.add(label)
    
    # Add segments if any
    for segment in segments:
        start_idx = segment.get('start')
        end_idx = segment.get('end')
        if start_idx is not None and end_idx is not None:
            segment = LabelSegment(
                start_index=start_idx,
                end_index=end_idx,
                label=label
            )
            db.session.add(segment)
    
    db.session.commit()
    
    return jsonify({'message': 'Label submitted successfully'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

