"""
Testy dla nowych funkcji bazy wiedzy
"""
import pytest
from src.knowledge.novahouse_info import (
    PORTFOLIO, PROCESS_STEPS, CLIENT_REVIEWS, PRODUCT_PARTNERS,
    WHY_CHOOSE_US, TEAM_INFO, COVERAGE_AREAS, COMPANY_STATS,
    get_process_overview, get_portfolio_list, get_client_reviews_summary,
    FAQ
)


class TestKnowledgeBase:
    """Testy bazy wiedzy"""
    
    def test_portfolio_exists(self):
        """Test czy portfolio ma realizacje"""
        assert len(PORTFOLIO) >= 4
        for key, project in PORTFOLIO.items():
            assert 'title' in project
            assert 'type' in project
            assert 'url' in project
    
    def test_process_steps(self):
        """Test czy proces ma 4 kroki"""
        assert len(PROCESS_STEPS) == 4
        for key, step in PROCESS_STEPS.items():
            assert 'title' in step
            assert 'description' in step
            assert 'duration' in step
            assert 'deliverables' in step
    
    def test_client_reviews(self):
        """Test czy są opinie klientów"""
        assert len(CLIENT_REVIEWS) >= 5
        for review in CLIENT_REVIEWS:
            assert 'author' in review
            assert 'rating' in review
            assert review['rating'] == 5  # Wszystkie 5 gwiazdek!
    
    def test_product_partners(self):
        """Test czy są partnerzy produktowi"""
        assert len(PRODUCT_PARTNERS) >= 17
        assert 'Laufen' in PRODUCT_PARTNERS
        assert 'Geberit' in PRODUCT_PARTNERS
        assert 'Hansgrohe' in PRODUCT_PARTNERS
    
    def test_company_stats(self):
        """Test statystyk firmy"""
        assert COMPANY_STATS['completed_projects'] == '30+'
        assert COMPANY_STATS['satisfied_clients'] == '95%'
        assert COMPANY_STATS['projects_before_deadline'] == '94%'
        assert COMPANY_STATS['warranty_years'] == 3
    
    def test_coverage_areas(self):
        """Test obszarów działania"""
        assert len(COVERAGE_AREAS['primary']) == 3
        assert any('Trójmiasto' in area for area in COVERAGE_AREAS['primary'])
        assert any('Warszawa' in area for area in COVERAGE_AREAS['primary'])
        assert any('Wrocław' in area for area in COVERAGE_AREAS['primary'])
    
    def test_why_choose_us(self):
        """Test USP"""
        assert len(WHY_CHOOSE_US) >= 7
        assert 'terminowosc' in WHY_CHOOSE_US
        assert 'ekipy' in WHY_CHOOSE_US
    
    def test_team_info(self):
        """Test info o zespole"""
        assert 'wiceprezes' in TEAM_INFO
        assert TEAM_INFO['wiceprezes']['name'] == 'Agnieszka Kubiak'
    
    def test_extended_faq(self):
        """Test rozszerzonego FAQ"""
        assert len(FAQ) >= 17  # Było 10, teraz 17+
        
        # Nowe pytania
        assert 'terminowosc' in FAQ
        assert 'ekipy' in FAQ
        assert 'zakres_uslug' in FAQ
        assert 'zabudowy_stolarskie' in FAQ
        assert 'gdzie_dzialamy' in FAQ
        assert 'cennik_dodatkowy' in FAQ
        assert 'po_odbiorze' in FAQ
        
        # Sprawdź że FAQ zawiera właściwe dane
        assert '94%' in FAQ['terminowosc']
        assert '36-miesięczną' in FAQ['gwarancja'] or '3-letniej' in FAQ['gwarancja']
        assert 'Trójmiasta' in FAQ['gdzie_dzialamy'] or 'Warszawa' in FAQ['gdzie_dzialamy']
    
    def test_helper_functions(self):
        """Test funkcji pomocniczych"""
        # get_process_overview
        overview = get_process_overview()
        assert 'PROCES REALIZACJI' in overview
        assert 'Wybór pakietu' in overview
        
        # get_portfolio_list
        portfolio = get_portfolio_list()
        assert 'REALIZACJE' in portfolio
        assert 'https://novahouse.pl/realizacje/' in portfolio
        
        # get_client_reviews_summary
        reviews = get_client_reviews_summary()
        assert 'CO MÓWIĄ KLIENCI' in reviews
        assert 'Alex Szymczak' in reviews or 'Magda Nowak' in reviews


class TestKnowledgeAPI:
    """Testy dla API endpoints bazy wiedzy"""
    
    @pytest.fixture
    def client(self):
        """Fixture Flask test client"""
        from src.main import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_portfolio_endpoint(self, client):
        """Test /api/knowledge/portfolio"""
        response = client.get('/api/knowledge/portfolio')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 4
        assert 'portfolio' in data
    
    def test_process_endpoint(self, client):
        """Test /api/knowledge/process"""
        response = client.get('/api/knowledge/process')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['total_steps'] == 4
        assert 'steps' in data
    
    def test_reviews_endpoint(self, client):
        """Test /api/knowledge/reviews"""
        response = client.get('/api/knowledge/reviews')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 5
        assert 'google_url' in data
    
    def test_partners_endpoint(self, client):
        """Test /api/knowledge/partners"""
        response = client.get('/api/knowledge/partners')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 17
    
    def test_stats_endpoint(self, client):
        """Test /api/knowledge/stats"""
        response = client.get('/api/knowledge/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'stats' in data
        assert 'coverage' in data
    
    def test_all_knowledge_endpoint(self, client):
        """Test /api/knowledge/all"""
        response = client.get('/api/knowledge/all')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'summary' in data
        assert data['summary']['portfolio_count'] >= 4
        assert data['summary']['reviews_count'] >= 5
