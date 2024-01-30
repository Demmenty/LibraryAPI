class TestRegisterUser:

    def test_success(self, test_client):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123!",
        }
        response = test_client.post("/auth/register", json=user_data)
        created_user = response.json()

        assert response.status_code == 201
        assert created_user["username"] == user_data["username"]
        assert created_user["email"] == user_data["email"]
        assert created_user.get("password") is None

    def test_weak_password(self, test_client):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "weakpassword",
        }
        response = test_client.post("/auth/register", json=user_data)
        response_json = response.json()

        assert response.status_code == 422
        assert response_json["detail"][0]["loc"] == ["body", "password"]
        assert response_json["detail"][0]["msg"] == (
            "Value error, Password must contain at least "
            "one lower character, one upper character, digit or special symbol"
        )

    def test_invalid_email(self, test_client):
        user_data = {
            "username": "testuser",
            "email": "test",
            "password": "strongpassword123!",
        }
        response = test_client.post("/auth/register", json=user_data)
        response_json = response.json()

        assert response.status_code == 422
        assert response_json["detail"][0]["loc"] == ["body", "email"]
        assert response_json["detail"][0]["msg"] == (
            "value is not a valid email address: "
            "The email address is not valid. It must have exactly one @-sign."
        )
