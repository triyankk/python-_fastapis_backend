DESCRIPTIONS = {
    "auth_register": {
        "summary": "Register new user",
        "description": """
        Register a new user with the system.
        
        The user will be created in an inactive state and needs to verify their email.
        
        Required fields:
        - username: unique username
        - email: valid email address
        - password: minimum 8 characters
        """,
        "response_description": "Registration successful"
    },
    "auth_login": {
        "summary": "User login",
        "description": """
        Authenticate a user and return access and refresh tokens.
        
        The tokens will be:
        - Stored in HTTP-only cookies
        - Returned in the response body
        
        Access token expires in 1 minute.
        Refresh token expires in 7 days.
        """,
        "response_description": "Login successful"
    },
    "user_me": {
        "summary": "Get current user",
        "description": """
        Get details of currently authenticated user.
        
        Requires a valid access token in the Authorization header.
        """,
        "response_description": "User details retrieved successfully"
    }
}
