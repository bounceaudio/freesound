#!/usr/bin/env python
"""
Verification script for freesound-python package.

This script verifies the package can be imported and used correctly
without requiring an actual API key.
"""

import sys


def test_import():
    """Test that the module can be imported."""
    print("Testing module import...")
    try:
        import freesound
        print("✓ Module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import module: {e}")
        return False


def test_client_creation():
    """Test that a client can be created."""
    print("\nTesting client creation...")
    try:
        import freesound
        client = freesound.FreesoundClient()
        print("✓ Client created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create client: {e}")
        return False


def test_token_setting():
    """Test that tokens can be set."""
    print("\nTesting token authentication...")
    try:
        import freesound
        client = freesound.FreesoundClient()
        
        # Test token auth
        client.set_token("test_token")
        if client.auth is None:
            print("✗ Token auth not set")
            return False
        print("✓ Token authentication set")
        
        # Test OAuth auth
        client.set_token("test_oauth_token", "oauth")
        if client.auth is None:
            print("✗ OAuth auth not set")
            return False
        print("✓ OAuth authentication set")
        
        return True
    except Exception as e:
        print(f"✗ Failed to set token: {e}")
        return False


def test_uri_generation():
    """Test URI generation."""
    print("\nTesting URI generation...")
    try:
        import freesound
        
        uri = freesound.URIS.uri(freesound.URIS.SOUND, 12345)
        expected = 'https://freesound.org/apiv2/sounds/12345/'
        
        if uri != expected:
            print(f"✗ Incorrect URI generated: {uri}")
            return False
        
        print(f"✓ URI generation works: {uri}")
        return True
    except Exception as e:
        print(f"✗ Failed to generate URI: {e}")
        return False


def test_classes_exist():
    """Test that all major classes exist."""
    print("\nTesting class existence...")
    try:
        import freesound
        
        classes = [
            'FreesoundClient',
            'FreesoundTokenAuth',
            'FreesoundObject',
            'Sound',
            'User',
            'Pack',
            'Pager',
            'URIS',
        ]
        
        missing_classes = []
        for cls_name in classes:
            if not hasattr(freesound, cls_name):
                missing_classes.append(cls_name)
        
        if missing_classes:
            print(f"✗ Missing classes: {', '.join(missing_classes)}")
            return False
        
        print(f"✓ All {len(classes)} major classes present")
        return True
    except Exception as e:
        print(f"✗ Failed to check classes: {e}")
        return False


def test_client_methods():
    """Test that client has expected methods."""
    print("\nTesting client methods...")
    try:
        import freesound
        client = freesound.FreesoundClient()
        
        methods = [
            'get_sound',
            'text_search',
            'content_based_search',
            'combined_search',
            'get_user',
            'get_pack',
            'set_token',
        ]
        
        missing_methods = []
        for method_name in methods:
            if not hasattr(client, method_name):
                missing_methods.append(method_name)
        
        if missing_methods:
            print(f"✗ Missing methods: {', '.join(missing_methods)}")
            return False
        
        print(f"✓ All {len(methods)} expected methods present")
        return True
    except Exception as e:
        print(f"✗ Failed to check methods: {e}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Freesound Python Package Verification")
    print("=" * 60)
    
    tests = [
        test_import,
        test_client_creation,
        test_token_setting,
        test_uri_generation,
        test_classes_exist,
        test_client_methods,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All verification tests passed!")
        return 0
    else:
        print("\n✗ Some verification tests failed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
