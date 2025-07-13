#!/usr/bin/env python3
"""
Zotero Connection Test Script
Run this first to verify your Zotero API credentials work correctly.
"""

import os
import sys
import asyncio
import json

def check_environment():
    """Check if environment variables are set"""
    print("=== Environment Check ===")
    
    api_key = os.getenv("ZOTERO_API_KEY")
    user_id = os.getenv("ZOTERO_USER_ID")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    
    print(f"✓ ZOTERO_API_KEY: {'Set' if api_key else '❌ Missing'}")
    print(f"✓ ZOTERO_USER_ID: {'Set' if user_id else '❌ Missing'}")
    print(f"✓ ZOTERO_LIBRARY_TYPE: {library_type}")
    
    if not api_key or not user_id:
        print("\n❌ Missing required environment variables!")
        print("\nTo fix this:")
        print("1. Get your API key from: https://www.zotero.org/settings/keys")
        print("2. Set environment variables:")
        print("   export ZOTERO_API_KEY='your_api_key_here'")
        print("   export ZOTERO_USER_ID='your_user_id_here'")
        return False
    
    return True, api_key, user_id, library_type

def check_packages():
    """Check if required packages are installed"""
    print("\n=== Package Check ===")
    
    try:
        import httpx
        print("✓ httpx: installed")
    except ImportError:
        print("❌ httpx: missing - run 'pip install httpx'")
        return False
    
    try:
        import mcp
        print("✓ mcp: installed")
    except ImportError:
        print("❌ mcp: missing - run 'pip install mcp'")
        return False
    
    return True

async def test_zotero_api(api_key, user_id, library_type):
    """Test direct connection to Zotero API"""
    print("\n=== Zotero API Test ===")
    
    import httpx
    
    base_url = f"https://api.zotero.org/{library_type}s/{user_id}"
    headers = {"Zotero-API-Key": api_key}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Test 1: Get collections
            print("Testing collections endpoint...")
            response = await client.get(f"{base_url}/collections?limit=5", headers=headers)
            
            if response.status_code == 200:
                collections = response.json()
                print(f"✓ Collections: Found {len(collections)} collections")
                if collections:
                    print(f"  Example: {collections[0].get('data', {}).get('name', 'Unnamed')}")
            elif response.status_code == 403:
                print("❌ Authentication failed - check your API key")
                return False
            elif response.status_code == 404:
                print("❌ User/library not found - check your user ID and library type")
                return False
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
            # Test 2: Get items
            print("Testing items endpoint...")
            response = await client.get(f"{base_url}/items?limit=5", headers=headers)
            
            if response.status_code == 200:
                items = response.json()
                print(f"✓ Items: Found {len(items)} items")
                if items:
                    item_title = items[0].get('data', {}).get('title', 'Untitled')
                    print(f"  Example: {item_title}")
            else:
                print(f"❌ Items request failed: {response.status_code}")
                return False
            
            print("✓ Zotero API connection successful!")
            return True
            
        except httpx.RequestError as e:
            print(f"❌ Network error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

def test_mcp_imports():
    """Test MCP imports"""
    print("\n=== MCP Import Test ===")
    
    try:
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        from mcp.types import Resource, Tool, TextContent
        print("✓ All MCP imports successful")
        return True
    except ImportError as e:
        print(f"❌ MCP import failed: {e}")
        print("Try: pip install --upgrade mcp")
        return False

async def main():
    """Run all tests"""
    print("Zotero MCP Server - Connection Test")
    print("=" * 40)
    
    # Check environment
    env_check = check_environment()
    if not env_check:
        return 1
    
    _, api_key, user_id, library_type = env_check
    
    # Check packages
    if not check_packages():
        return 1
    
    # Test MCP imports
    if not test_mcp_imports():
        return 1
    
    # Test Zotero API
    if not await test_zotero_api(api_key, user_id, library_type):
        return 1
    
    print("\n" + "=" * 40)
    print("✓ All tests passed! Your Zotero MCP server should work.")
    print("\nNext steps:")
    print("1. Run the debug version of the MCP server")
    print("2. Check the logs for any additional issues")
    print("3. Test the connection using the 'test_connection' tool")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)