# freesound-python

A Python client for the [Freesound](https://freesound.org) API v2.

## Features

- Simple and intuitive Python interface to the Freesound API
- Supports both token-based and OAuth2 authentication
- Search sounds using text queries, content-based queries, or combined searches
- Retrieve sound information, analysis, and similar sounds
- Access user profiles and sound packs
- Download sound previews and full-quality files (with appropriate authentication)
- Automatic conversion of API responses to Python objects
- Access to raw JSON data when needed
- Customizable HTTP session for advanced use cases (proxies, rate limiting, etc.)

## Installation

### From source

Clone the repository and install:

```bash
git clone https://github.com/bounceaudio/freesound.git
cd freesound
python setup.py install
```

### Using pip

You can also install directly from GitHub:

```bash
pip install git+https://github.com/bounceaudio/freesound.git
```

## Quick Start

Before using the client, you need to obtain an API key from [Freesound](https://freesound.org/apiv2/apply/).

```python
import freesound

# Create a client instance
client = freesound.FreesoundClient()

# Set your API key
client.set_token("YOUR_API_KEY")

# Search for sounds
results = client.text_search(query="rain", fields="id,name,previews")

# Iterate through results
for sound in results:
    print(f"{sound.name} by {sound.username}")
    # Download preview
    sound.retrieve_preview(".", sound.name + ".mp3")
```

## Usage Examples

### Search for Sounds

```python
# Simple text search
results = client.text_search(query="ocean waves")

# Search with filters
results = client.text_search(
    query="piano",
    filter="tag:jazz duration:[1 TO 10]",
    sort="rating_desc",
    fields="id,name,tags,duration,username"
)

# Content-based search (by audio features)
results = client.content_based_search(
    target="lowlevel.pitch.mean:220",
    descriptors_filter="lowlevel.pitch_instantaneous_confidence.mean:[0.8 TO 1]",
    fields="id,name,url"
)

# Combined search (text + content)
results = client.combined_search(
    query="instrument",
    target="lowlevel.pitch.mean:440",
    filter="single-note"
)
```

### Get Sound Information

```python
# Get sound by ID
sound = client.get_sound(96541)

print(f"Name: {sound.name}")
print(f"Description: {sound.description}")
print(f"Tags: {', '.join(sound.tags)}")
print(f"Duration: {sound.duration} seconds")
print(f"License: {sound.license}")

# Get specific fields
sound = client.get_sound(
    96541,
    fields="id,name,username,duration",
    descriptors="lowlevel.spectral_centroid",
    normalized=1
)

# Get sound analysis
analysis = sound.get_analysis()
mfcc = analysis.lowlevel.mfcc.mean
```

### Download Sounds

```python
# Download preview (no authentication needed for previews)
sound = client.get_sound(96541)
sound.retrieve_preview("./downloads", "my_sound.mp3")

# Download full quality (requires OAuth2)
# After setting up OAuth2 authentication:
sound.retrieve("./downloads", "full_quality.wav")
```

### Users and Packs

```python
# Get user information
user = client.get_user("username")
print(f"User: {user.username}")
print(f"Sounds: {user.num_sounds}")

# Get user's sounds
sounds = user.get_sounds()

# Get pack information
pack = client.get_pack(3416)
print(f"Pack: {pack.name}")
print(f"Sounds: {pack.num_sounds}")

# Get sounds in pack
sounds = pack.get_sounds()
```

### Working with Results

```python
# Iterate through paginated results
results = client.text_search(query="drums")

for sound in results:
    print(sound.name)

# Access result count
print(f"Total results: {results.count}")

# Access raw JSON data
json_data = sound.as_dict()
```

## Advanced Usage

### Custom Request Session

You can customize the HTTP session used by the client for advanced scenarios:

```python
import freesound

client = freesound.FreesoundClient()
client.set_token("YOUR_API_KEY")

# Add proxy support
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}
client.session.proxies.update(proxies)

# Add rate limiting
from requests_ratelimiter import LimiterSession
client.session = LimiterSession(per_minute=59)
```

### OAuth2 Authentication

For downloading full-quality sounds and other write operations, you need OAuth2 authentication:

```python
from requests_oauthlib import OAuth2Session
import freesound

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# OAuth2 flow
oauth = OAuth2Session(client_id)
authorization_url, state = oauth.authorization_url(
    "https://freesound.org/apiv2/oauth2/authorize/"
)

print(f"Please visit: {authorization_url}")
authorization_code = input("Enter authorization code: ")

oauth_token = oauth.fetch_token(
    "https://freesound.org/apiv2/oauth2/access_token/",
    authorization_code,
    client_secret=client_secret,
)

# Use OAuth2 token
client = freesound.FreesoundClient()
client.set_token(oauth_token["access_token"], "oauth")
```

## API Documentation

For detailed information about the Freesound API, visit:
- [Freesound API Documentation](https://freesound.org/docs/api/)
- [API Resources](https://freesound.org/docs/api/resources_apiv2.html)
- [Authentication Guide](https://freesound.org/docs/api/authentication.html)

## Requirements

- Python >= 3.6
- requests >= 2.27

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

- Report issues on [GitHub Issues](https://github.com/bounceaudio/freesound/issues)
- For API-related questions, visit [Freesound Forums](https://freesound.org/forum/)

## Credits

This client is based on the official [freesound-python](https://github.com/MTG/freesound-python) client by the Music Technology Group at Universitat Pompeu Fabra, Barcelona.
