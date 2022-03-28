"""
Tests For
- ping endpoint
- posts endpoint with different variables
"""


def test_ping_request(client):
    response = client.get("/api/ping")
    assert response.status_code == 200

def test_posts_requests_empty(client):
    response = client.get("/api/posts/")
    assert response.status_code == 400

def test_posts_requests_tags(client):
    response = client.get("/api/posts/health,random,tech")
    assert response.status_code == 200

def test_posts_requests_sort(client):
    response = client.get("/api/posts/health/popularity")
    assert response.status_code == 200
    response = client.get("/api/posts/health/likes")
    assert response.status_code == 200
    response = client.get("/api/posts/health/id")
    assert response.status_code == 200
    response = client.get("/api/posts/health/reads")
    assert response.status_code == 200
    response = client.get("/api/posts/health/bad")
    assert response.status_code == 400

def test_posts_requests_order(client):
    response = client.get("/api/posts/health,random,tech/likes/desc")
    assert response.status_code == 200
    response = client.get("/api/posts/health,random,tech/likes/asc")
    assert response.status_code == 200
    response = client.get("/api/posts/health,random,tech/likes/bad")
    assert response.status_code == 400