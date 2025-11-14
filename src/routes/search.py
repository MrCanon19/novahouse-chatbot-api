"""
Advanced Search API Routes
===========================
Full-text search with fuzzy matching
"""

from flask import Blueprint, jsonify, request

search_routes = Blueprint('search_routes', __name__)

@search_routes.route('/api/search', methods=['GET'])
def search():
    """
    Search knowledge base
    
    Query params:
        q: Search query
        type: Filter by type (faq, portfolio, review, blog)
        lang: Filter by language (pl, en, de)
        limit: Max results (default: 10)
        fuzzy: Enable fuzzy matching (default: true)
    
    Returns:
        JSON with search results
    """
    try:
        from src.services.search_service import search_service
        
        query = request.args.get('q', '')
        doc_type = request.args.get('type')
        language = request.args.get('lang')
        limit = int(request.args.get('limit', 10))
        fuzzy = request.args.get('fuzzy', 'true').lower() == 'true'
        
        if not query:
            return jsonify({'success': False, 'error': 'Query parameter "q" required'}), 400
        
        # Perform search
        results = search_service.search(
            query_str=query,
            doc_type=doc_type,
            language=language,
            limit=limit,
            fuzzy=fuzzy
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@search_routes.route('/api/search/suggest', methods=['GET'])
def search_suggestions():
    """
    Get search suggestions (autocomplete)
    
    Query params:
        q: Partial search term
        limit: Max suggestions (default: 5)
    
    Returns:
        JSON with suggestions
    """
    try:
        from src.services.search_service import search_service
        
        partial = request.args.get('q', '')
        limit = int(request.args.get('limit', 5))
        
        if not partial or len(partial) < 2:
            return jsonify({'success': True, 'suggestions': []})
        
        # Get suggestions
        suggestions = search_service.suggest(partial=partial, limit=limit)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@search_routes.route('/api/search/stats', methods=['GET'])
def search_stats():
    """
    Get search index statistics
    
    Returns:
        JSON with index stats
    """
    try:
        from src.services.search_service import search_service
        
        stats = search_service.get_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@search_routes.route('/api/search/reindex', methods=['POST'])
def reindex_knowledge_base():
    """
    Rebuild search index from knowledge base
    
    Returns:
        JSON with reindex status
    """
    try:
        from src.services.search_service import search_service
        
        # Rebuild index
        search_service.index_knowledge_base()
        
        stats = search_service.get_stats()
        
        return jsonify({
            'success': True,
            'message': 'Search index rebuilt successfully',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
