from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from typing import Optional

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    """Get a list of games with optional filtering by publisher and category"""
    # Start with base query
    games_query = get_games_base_query()
    
    # Get filter parameters
    publisher_id = request.args.get('publisher_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    # Apply filters if provided
    if publisher_id:
        games_query = games_query.filter(Game.publisher_id == publisher_id)
    if category_id:
        games_query = games_query.filter(Game.category_id == category_id)
    
    # Execute query and convert results
    games_list = [game.to_dict() for game in games_query.all()]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/publishers', methods=['GET'])
def get_publishers() -> Response:
    """Get a list of all publishers for filtering"""
    publishers = db.session.query(Publisher).order_by(Publisher.name).all()
    return jsonify([{'id': p.id, 'name': p.name} for p in publishers])

@games_bp.route('/api/categories', methods=['GET'])
def get_categories() -> Response:
    """Get a list of all categories for filtering"""
    categories = db.session.query(Category).order_by(Category.name).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])
