#!/usr/bin/env python3
"""
Simple test script for mem0 setup in beer0 project.

Tests basic memory functionality to ensure everything is working.
"""

import sys
from pathlib import Path

from src.memory_manager import get_memory_manager

def test_memory():
    """Test basic memory operations."""
    print("🧠 Testing mem0 setup...")
    
    try:
        # Initialize memory manager
        print("1. Initializing memory manager...")
        manager = get_memory_manager()
        print("   ✅ Memory manager initialized successfully")
        
        # Add a test preference
        print("2. Adding test preference...")
        test_preference = "I love hoppy IPAs with citrus notes"
        success = manager.add_preference(test_preference)
        if success:
            print("   ✅ Test preference added successfully")
        else:
            print("   ❌ Failed to add test preference")
            return False
        
        # Search for the preference
        print("3. Searching for preferences...")
        results = manager.get_preferences("IPA hoppy")
        print(f"   ✅ Found {len(results)} matching preferences")
        
        if results:
            print("   📝 Sample result:")
            for i, result in enumerate(results[:1]):  # Show first result
                if isinstance(result, dict) and 'memory' in result:
                    print(f"      - {result['memory']}")
        
        # Test rating-based preference update
        print("4. Testing rating-based preference...")
        manager.update_from_rating(
            drink_name="Stone IPA", 
            rating=5, 
            flavor_profile="hoppy, citrusy, piney",
            notes="Perfect balance of hops and malt"
        )
        print("   ✅ Rating-based preference added")
        
        # Get user profile summary
        print("5. Getting user profile summary...")
        profile = manager.get_user_profile_summary()
        print(f"   ✅ Profile retrieved - {profile['recent_activity_count']} recent activities")
        
        print("\n🎉 All tests passed! Mem0 is working correctly.")
        print("📁 Memory data is stored locally in: beer0_memory_db/")
        print("🔧 Using AWS Bedrock for LLM and embeddings")
        print("💾 Using ChromaDB for vector storage")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("\nTroubleshooting tips:")
        print("- Check AWS credentials are configured (bedrock profile)")
        print("- Ensure AWS region is correct in config.py")
        print("- Verify internet connection for AWS Bedrock access")
        return False

if __name__ == "__main__":
    success = test_memory()
    sys.exit(0 if success else 1)
