class TestToken:
    def test_token(self, client, session):
        # Arrange: Create account
        name = "For test_token 01"
        email = "token01@gmail.com"
        password = "token01_s1cret"

        response = client.post(
            "/accounts/", json={"name": name, "email": email, "password": password}
        )
        assert response.status_code == 200

        # Arrange: Save the account info
        account = response.json()

        # Act: Create token
        response = client.post(
            "/token/", data={"username": email, "password": password}
        )
        token = response.json()["access_token"]

        # Assert: Test if the protected endpoint works
        me_response = client.get(
            "/accounts/me/", headers={"Authorization": f"Bearer {token}"}
        )

        assert me_response.status_code == 200
        account_from_token = me_response.json()

        assert account["id"] == account_from_token["id"]
