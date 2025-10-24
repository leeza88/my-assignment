# tests.py - Unit Tests for Library Management System

import operations

def run_tests():
    print("Running Library Management System Tests...")
    print("=" * 50)
    
    # Clear data before tests
    operations.books.clear()
    operations.members.clear()
    
    # Test 1: add_book()
    print("\n1. Testing add_book()...")
    success, message = operations.add_book("001", "Python 101", "John", "Fiction", 5)
    assert success == True
    assert message == "Book added successfully."
    print("✅ add_book() - Basic test passed")
    
    # Test duplicate ISBN
    success, message = operations.add_book("001", "Another Book", "Author", "Fiction", 3)
    assert success == False
    assert "already exists" in message
    print("✅ add_book() - Duplicate ISBN test passed")
    
    # Test invalid genre
    success, message = operations.add_book("002", "Test Book", "Author", "Invalid Genre", 2)
    assert success == False
    assert "Invalid genre" in message
    print("✅ add_book() - Invalid genre test passed")
    
    # Test 2: add_member()
    print("\n2. Testing add_member()...")
    success, message = operations.add_member("M001", "Alice", "alice@example.com")
    assert success == True
    assert message == "Member added successfully."
    print("✅ add_member() - Basic test passed")
    
    # Test duplicate member ID
    success, message = operations.add_member("M001", "Bob", "bob@example.com")
    assert success == False
    assert "already exists" in message
    print("✅ add_member() - Duplicate member ID test passed")
    
    # Test 3: search_books()
    print("\n3. Testing search_books()...")
    operations.add_book("003", "Advanced Python", "Jane Smith", "Non-Fiction", 3)
    
    # Search by title
    results = operations.search_books("Python")
    assert len(results) == 2
    print("✅ search_books() - Title search passed")
    
    # Search by author
    results = operations.search_books("Smith")
    assert len(results) == 1
    print("✅ search_books() - Author search passed")
    
    # Search non-existent
    results = operations.search_books("Nonexistent")
    assert len(results) == 0
    print("✅ search_books() - No results test passed")
    
    # Test 4: update_book()
    print("\n4. Testing update_book()...")
    success, message = operations.update_book("001", title="Python Basics")
    assert success == True
    assert operations.books["001"]["title"] == "Python Basics"
    print("✅ update_book() - Title update passed")
    
    success, message = operations.update_book("001", total_copies=10)
    assert success == True
    assert operations.books["001"]["total_copies"] == 10
    assert operations.books["001"]["available_copies"] == 10  # Available should also be 10
    print("✅ update_book() - Copies update passed")
    
    # Test update non-existent book
    success, message = operations.update_book("999", title="Test")
    assert success == False
    print("✅ update_book() - Non-existent book test passed")
    
    # Test 5: update_member()
    print("\n5. Testing update_member()...")
    success, message = operations.update_member("M001", name="Alice Johnson")
    assert success == True
    # Find the member and check name was updated
    member = next(m for m in operations.members if m["member_id"] == "M001")
    assert member["name"] == "Alice Johnson"
    print("✅ update_member() - Name update passed")
    
    # Test update non-existent member
    success, message = operations.update_member("M999", name="Test")
    assert success == False
    print("✅ update_member() - Non-existent member test passed")
    
    # Test 6: borrow_book()
    print("\n6. Testing borrow_book()...")
    success, message = operations.borrow_book("M001", "001")
    assert success == True
    assert operations.books["001"]["available_copies"] == 9  # 10 total - 1 borrowed
    print("✅ borrow_book() - Basic borrow test passed")
    
    # Test borrow non-existent member
    success, message = operations.borrow_book("M999", "001")
    assert success == False
    print("✅ borrow_book() - Non-existent member test passed")
    
    # Test borrow non-existent book
    success, message = operations.borrow_book("M001", "999")
    assert success == False
    print("✅ borrow_book() - Non-existent book test passed")
    
    # Test borrow same book twice
    success, message = operations.borrow_book("M001", "001")
    assert success == False
    assert "already has this book" in message
    print("✅ borrow_book() - Duplicate borrow test passed")
    
    # Test 7: return_book()
    print("\n7. Testing return_book()...")
    success, message = operations.return_book("M001", "001")
    assert success == True
    assert operations.books["001"]["available_copies"] == 10
    print("✅ return_book() - Basic return test passed")
    
    # Test return non-borrowed book
    success, message = operations.return_book("M001", "001")
    assert success == False
    assert "not borrowed" in message
    print("✅ return_book() - Non-borrowed book test passed")
    
    # Test 8: delete_book()
    print("\n8. Testing delete_book()...")
    # First add a book with no borrows
    operations.add_book("004", "Delete Test", "Author", "Fiction", 1)
    success, message = operations.delete_book("004")
    assert success == True
    assert "004" not in operations.books
    print("✅ delete_book() - Basic delete test passed")
    
    # Test delete book with borrowed copies
    operations.borrow_book("M001", "001")  # Borrow a copy first
    success, message = operations.delete_book("001")
    assert success == False
    assert "currently borrowed" in message
    print("✅ delete_book() - Borrowed book delete test passed")
    
    # Test 9: delete_member()
    print("\n9. Testing delete_member()...")
    # Add a member with no borrowed books
    operations.add_member("M002", "Bob", "bob@example.com")
    success, message = operations.delete_member("M002")
    assert success == True
    member_ids = [m["member_id"] for m in operations.members]
    assert "M002" not in member_ids
    print("✅ delete_member() - Basic delete test passed")
    
    # Test delete member with borrowed books
    success, message = operations.delete_member("M001")
    assert success == False
    assert "borrowed books" in message
    print("✅ delete_member() - Member with books delete test passed")
    
    # Test 10: borrow limit
    print("\n10. Testing borrow limit...")
    # Return the borrowed book first
    operations.return_book("M001", "001")
    
    # Add more books for testing limit
    operations.add_book("005", "Book 1", "Author", "Fiction", 1)
    operations.add_book("006", "Book 2", "Author", "Fiction", 1)
    operations.add_book("007", "Book 3", "Author", "Fiction", 1)
    operations.add_book("008", "Book 4", "Author", "Fiction", 1)
    
    # Borrow 3 books (limit)
    operations.borrow_book("M001", "005")
    operations.borrow_book("M001", "006") 
    operations.borrow_book("M001", "007")
    
    # Try to borrow 4th book
    success, message = operations.borrow_book("M001", "008")
    assert success == False
    assert "limit" in message
    print("✅ borrow_book() - Borrow limit test passed")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()