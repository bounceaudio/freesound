"""
Example usage of the freesound-python client.

Before running this example, set your Freesound API key as an environment variable:
export FREESOUND_API_KEY="your_api_key_here"

You can get an API key from: https://freesound.org/apiv2/apply/
"""
import os
import sys

import freesound

# Get API key from environment variable
api_key = os.getenv('FREESOUND_API_KEY', None)
if api_key is None:
    print("You need to set your API key as an environment variable")
    print("named FREESOUND_API_KEY")
    print("\nGet your API key at: https://freesound.org/apiv2/apply/")
    sys.exit(-1)

# Create client and set authentication
freesound_client = freesound.FreesoundClient()
freesound_client.set_token(api_key)

print("=" * 60)
print("Freesound Python Client Examples")
print("=" * 60)
print()

# Example 1: Get sound info
print("1. Getting sound information by ID:")
print("-" * 60)
sound = freesound_client.get_sound(96541)
print(f"Sound name: {sound.name}")
print(f"URL: {sound.url}")
print(f"Description: {sound.description}")
print(f"Tags: {', '.join(sound.tags)}")
print(f"Duration: {sound.duration}s")
print(f"License: {sound.license}")
print()

# Example 2: Text search
print("2. Text search for 'rain' sounds:")
print("-" * 60)
results = freesound_client.text_search(
    query="rain",
    filter="duration:[1 TO 5]",
    fields="id,name,tags,duration,username"
)
print(f"Found {results.count} sounds (showing first page):")
for i, sound in enumerate(results[:5]):  # Show first 5 results
    print(f"  {i+1}. {sound.name} by {sound.username} ({sound.duration:.1f}s)")
print()

# Example 3: Get user information
print("3. Getting user information:")
print("-" * 60)
try:
    user = freesound_client.get_user("xserra")
    print(f"Username: {user.username}")
    print(f"About: {user.about}")
    print(f"Number of sounds: {user.num_sounds}")
    print()
except Exception as e:
    print(f"Error fetching user: {e}")
    print()

# Example 4: Get pack information
print("4. Getting pack information:")
print("-" * 60)
try:
    pack = freesound_client.get_pack(3416)
    print(f"Pack name: {pack.name}")
    print(f"Description: {pack.description[:100]}...")
    print(f"Number of sounds: {pack.num_sounds}")
    print()
except Exception as e:
    print(f"Error fetching pack: {e}")
    print()

# Example 5: Content-based search
print("5. Content-based search (finding sounds with similar pitch):")
print("-" * 60)
try:
    results = freesound_client.content_based_search(
        target="lowlevel.pitch.mean:220",
        fields="id,name,url"
    )
    print(f"Found {results.count} sounds with similar pitch:")
    for i, sound in enumerate(results[:3]):  # Show first 3 results
        print(f"  {i+1}. {sound.name}")
    print()
except Exception as e:
    print(f"Content search may require specific API access: {e}")
    print()

# Example 6: Combined search
print("6. Combined text and content search:")
print("-" * 60)
try:
    results = freesound_client.combined_search(
        query="note",
        target="lowlevel.pitch.mean:220",
        fields="id,name,username"
    )
    print(f"Found {results.count} sounds matching both criteria:")
    for i, sound in enumerate(results[:3]):
        print(f"  {i+1}. {sound.name} by {sound.username}")
    print()
except Exception as e:
    print(f"Combined search error: {e}")
    print()

print("=" * 60)
print("Examples completed!")
print("=" * 60)
print()
print("For more information, visit:")
print("  API Documentation: https://freesound.org/docs/api/")
print("  Get API Key: https://freesound.org/apiv2/apply/")
