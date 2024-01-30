from app.auth.exceptions import AccessTokenRequired
from app.books.exceptions import NotValidISBN


class TestGetBookByISBN:

    def test_not_valid_isbn(self, test_client):
        isbn = "12345678"
        response = test_client.get(f"books/by-isbn/{isbn}", headers={"Authorization": "Bearer token"})

        assert response.status_code == 422
        assert response.json()["detail"] == NotValidISBN.DETAIL

    def test_no_access_token(self, test_client):
        isbn = "0704334801"
        response = test_client.get(f"books/by-isbn/{isbn}")
        response_json = response.json()

        assert response.status_code == 403
        assert response_json["detail"] == AccessTokenRequired.DETAIL
