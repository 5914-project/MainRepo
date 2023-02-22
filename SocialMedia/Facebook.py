import facebook

# Obtain user access token
access_token = "YOUR_ACCESS_TOKEN"

# Create Facebook Graph API object
graph = facebook.GraphAPI(access_token)

# Make a post on the user's behalf
graph.put_object(parent_object='me', connection_name='feed', message='Hello, world!')