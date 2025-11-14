"""
Advanced Search Service
=======================
Full-text search with fuzzy matching using Whoosh
"""

import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.analysis import StemmingAnalyzer
from datetime import datetime, timezone
from typing import List, Dict, Any

# Search index directory
INDEX_DIR = os.path.join(os.path.dirname(__file__), '..', 'search_index')

# Schema for search index
search_schema = Schema(
    id=ID(stored=True, unique=True),
    type=KEYWORD(stored=True),  # 'faq', 'portfolio', 'review', 'blog'
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    tags=KEYWORD(stored=True, commas=True),
    language=KEYWORD(stored=True),  # 'pl', 'en', 'de'
    created_at=DATETIME(stored=True)
)

class AdvancedSearchService:
    """Full-text search with fuzzy matching"""
    
    def __init__(self):
        # Create index directory if not exists
        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)
        
        # Create or open index
        if not exists_in(INDEX_DIR):
            self.ix = create_in(INDEX_DIR, search_schema)
            print("✅ Search index created")
        else:
            self.ix = open_dir(INDEX_DIR)
            print("✅ Search index opened")
    
    def index_document(
        self,
        doc_id: str,
        doc_type: str,
        title: str,
        content: str,
        tags: List[str] = None,
        language: str = 'pl'
    ):
        """
        Add document to search index
        
        Args:
            doc_id: Unique document ID
            doc_type: Type ('faq', 'portfolio', 'review', 'blog')
            title: Document title
            content: Document content
            tags: List of tags
            language: Language code
        """
        writer = self.ix.writer()
        
        tags_str = ','.join(tags) if tags else ''
        
        writer.add_document(
            id=doc_id,
            type=doc_type,
            title=title,
            content=content,
            tags=tags_str,
            language=language,
            created_at=datetime.now(timezone.utc)
        )
        
        writer.commit()
        print(f"✅ Indexed: {doc_type} - {title}")
    
    def update_document(
        self,
        doc_id: str,
        doc_type: str,
        title: str,
        content: str,
        tags: List[str] = None,
        language: str = 'pl'
    ):
        """Update existing document"""
        writer = self.ix.writer()
        
        tags_str = ','.join(tags) if tags else ''
        
        writer.update_document(
            id=doc_id,
            type=doc_type,
            title=title,
            content=content,
            tags=tags_str,
            language=language,
            created_at=datetime.now(timezone.utc)
        )
        
        writer.commit()
        print(f"✅ Updated: {doc_type} - {title}")
    
    def delete_document(self, doc_id: str):
        """Delete document from index"""
        writer = self.ix.writer()
        writer.delete_by_term('id', doc_id)
        writer.commit()
        print(f"✅ Deleted: {doc_id}")
    
    def search(
        self,
        query_str: str,
        doc_type: str = None,
        language: str = None,
        limit: int = 10,
        fuzzy: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search documents
        
        Args:
            query_str: Search query
            doc_type: Filter by type
            language: Filter by language
            limit: Maximum results
            fuzzy: Enable fuzzy matching
        
        Returns:
            List of matching documents with scores
        """
        with self.ix.searcher() as searcher:
            # Parse query in title and content fields
            parser = MultifieldParser(['title', 'content'], schema=self.ix.schema)
            
            # Enable fuzzy matching
            if fuzzy:
                parser.add_plugin(FuzzyTermPlugin())
                # Add tilde for fuzzy search
                if '~' not in query_str:
                    query_str = f"{query_str}~2"  # Allow 2 character edits
            
            query = parser.parse(query_str)
            
            # Apply filters
            filter_query = None
            if doc_type:
                from whoosh.query import Term
                filter_query = Term('type', doc_type)
            
            if language:
                from whoosh.query import Term, And
                lang_filter = Term('language', language)
                if filter_query:
                    filter_query = And([filter_query, lang_filter])
                else:
                    filter_query = lang_filter
            
            # Execute search
            results = searcher.search(query, limit=limit, filter=filter_query)
            
            # Format results
            formatted_results = []
            for hit in results:
                formatted_results.append({
                    'id': hit['id'],
                    'type': hit['type'],
                    'title': hit['title'],
                    'content': hit['content'][:200] + '...' if len(hit['content']) > 200 else hit['content'],
                    'tags': hit['tags'].split(',') if hit['tags'] else [],
                    'language': hit['language'],
                    'score': hit.score,
                    'created_at': hit['created_at'].isoformat() if hit['created_at'] else None
                })
            
            return formatted_results
    
    def suggest(self, partial: str, field: str = 'title', limit: int = 5) -> List[str]:
        """
        Get search suggestions (autocomplete)
        
        Args:
            partial: Partial search term
            field: Field to suggest from
            limit: Max suggestions
        """
        with self.ix.searcher() as searcher:
            suggestions = []
            
            # Get all terms starting with partial
            for term in searcher.lexicon(field):
                if term.decode('utf-8').lower().startswith(partial.lower()):
                    suggestions.append(term.decode('utf-8'))
                    if len(suggestions) >= limit:
                        break
            
            return suggestions
    
    def index_knowledge_base(self):
        """Index all knowledge base content"""
        try:
            from src.knowledge.novahouse_info import (
                FAQ, PORTFOLIO, CLIENT_REVIEWS, BLOG_ARTICLES, PROCESS_STEPS
            )
            
            # Index FAQ
            for i, faq in enumerate(FAQ):
                self.index_document(
                    doc_id=f"faq_{i}",
                    doc_type='faq',
                    title=faq['question'],
                    content=faq['answer'],
                    tags=['faq', 'question'],
                    language='pl'
                )
            
            # Index Portfolio
            for i, project in enumerate(PORTFOLIO):
                self.index_document(
                    doc_id=f"portfolio_{i}",
                    doc_type='portfolio',
                    title=project['title'],
                    content=f"{project['category']} - {project['area']} - {project['duration']}",
                    tags=['portfolio', 'project', project['package'].lower()],
                    language='pl'
                )
            
            # Index Reviews
            for i, review in enumerate(CLIENT_REVIEWS):
                self.index_document(
                    doc_id=f"review_{i}",
                    doc_type='review',
                    title=f"Opinia - {review['author']}",
                    content=review['text'],
                    tags=['review', 'opinion', f"rating_{review['rating']}"],
                    language='pl'
                )
            
            # Index Blog Articles
            for i, article in enumerate(BLOG_ARTICLES):
                self.index_document(
                    doc_id=f"blog_{i}",
                    doc_type='blog',
                    title=article['title'],
                    content=article['excerpt'],
                    tags=['blog', 'article'] + article.get('tags', []),
                    language='pl'
                )
            
            print(f"✅ Indexed {len(FAQ)} FAQs, {len(PORTFOLIO)} projects, {len(CLIENT_REVIEWS)} reviews, {len(BLOG_ARTICLES)} articles")
            
        except Exception as e:
            print(f"❌ Failed to index knowledge base: {e}")
    
    def get_stats(self) -> dict:
        """Get search index statistics"""
        with self.ix.searcher() as searcher:
            return {
                'total_documents': searcher.doc_count_all(),
                'unique_terms': len(list(searcher.lexicon('content'))),
                'index_size_bytes': os.path.getsize(os.path.join(INDEX_DIR, '_MAIN_1.toc')) if os.path.exists(os.path.join(INDEX_DIR, '_MAIN_1.toc')) else 0
            }

# Global instance
search_service = AdvancedSearchService()
