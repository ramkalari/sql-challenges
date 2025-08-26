#!/usr/bin/env python3

import sys
import os
sys.path.append('backend')

from challenge_container import challenge_manager

def test_empty_query():
    challenge_id = 18
    user_id = "test_user"
    
    # Test different empty/invalid queries
    queries = [
        ("Empty string", ""),
        ("Whitespace only", "   "),
        ("Just semicolon", ";"),
        ("Comment only", "-- this is a comment"),
    ]
    
    for desc, query in queries:
        print(f"\n=== Testing: {desc} ===")
        print(f"Query: '{query}'")
        
        try:
            result = challenge_manager.execute_challenge(challenge_id, user_id, query)
            print(f"Success: {result.get('success')}")
            print(f"Passed: {result.get('passed')}")
            print(f"Results: {result.get('results')}")
            print(f"Error: {result.get('error')}")
            
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_empty_query() 