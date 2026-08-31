import sys
import os
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def handler(event, context):
    """
    Vercel serverless function handler for Python
    """
    try:
        # Parse the Vercel event
        method = event.get('method', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        if body:
            try:
                body = json.loads(body)
            except:
                body = {}
        
        # Import backend services
        from backend.app.database import test_connection
        from backend.app.services.auth_service import ensure_users_table
        
        # Test database connection
        try:
            db_ok = test_connection()
            if db_ok:
                ensure_users_table()
        except Exception as db_error:
            print(f"Database error: {db_error}")
        
        # Simple routing
        if path == '/api/auth/login' and method == 'POST':
            email = body.get('email')
            password = body.get('password')
            
            # Simple mock response for now
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'access_token': 'mock_token',
                    'token_type': 'bearer',
                    'user': {'email': email}
                })
            }
        elif path == '/api/auth/signup' and method == 'POST':
            email = body.get('email')
            password = body.get('password')
            full_name = body.get('full_name', '')
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'User created successfully',
                    'email': email
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

