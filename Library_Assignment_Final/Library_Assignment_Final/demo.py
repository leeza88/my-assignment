# demo.py - Interactive Library Management System

import operations

def menu():
    print("\n--- Mini Library Management System ---")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Search Books")
    print("4. Update Book")
    print("5. Update Member")
    print("6. Delete Book")
    print("7. Delete Member")
    print("8. Borrow Book")
    print("9. Return Book")
    print("10. Display All Books")
    print("11. Display All Members")
    print("12. Exit")

def display_all_books():
    """Display all books in the system"""
    books = operations.get_all_books()
    if not books:
        print("No books in the system.")
        return
    
    print("\n--- All Books ---")
    for isbn, book in books.items():
        print(f"ISBN: {isbn}")
        print(f"  Title: {book['title']}")
        print(f"  Author: {book['author']}")
        print(f"  Genre: {book['genre']}")
        print(f"  Copies: {book['available_copies']}/{book['total_copies']} available")
        print()

def display_all_members():
    """Display all members in the system"""
    members = operations.get_all_members()
    if not members:
        print("No members in the system.")
        return
    
    print("\n--- All Members ---")
    for member in members:
        print(f"ID: {member['member_id']}")
        print(f"  Name: {member['name']}")
        print(f"  Email: {member['email']}")
        print(f"  Borrowed Books: {len(member['borrowed_books'])}")
        if member['borrowed_books']:
            for isbn in member['borrowed_books']:
                book_title = operations.books[isbn]['title'] if isbn in operations.books else "Unknown Book"
                print(f"    - {isbn}: {book_title}")
        print()

while True:
    menu()
    choice = input("Select an option: ")

    if choice == "1":
        print("\n--- Add New Book ---")
        isbn = input("Enter ISBN: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        print(f"Available genres: {operations.genres}")
        genre = input("Enter Genre: ")
        total = int(input("Enter Total Copies: "))
        success, message = operations.add_book(isbn, title, author, genre, total)
        print(f"Result: {message}")

    elif choice == "2":
        print("\n--- Add New Member ---")
        member_id = input("Enter Member ID: ")
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        success, message = operations.add_member(member_id, name, email)
        print(f"Result: {message}")

    elif choice == "3":
        print("\n--- Search Books ---")
        keyword = input("Enter search keyword (title or author): ")
        results = operations.search_books(keyword)
        if results:
            print(f"\nFound {len(results)} book(s):")
            for book in results:
                print(f"ISBN: {book['isbn']}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print(f"Genre: {book['genre']}")
                print(f"Available: {book['available_copies']}/{book['total_copies']}")
                print()
        else:
            print("No books found.")

    elif choice == "4":
        print("\n--- Update Book ---")
        isbn = input("Enter ISBN of book to update: ")
        
        # Check if book exists
        if isbn not in operations.books:
            print("Book not found!")
            continue
            
        current_book = operations.books[isbn]
        print(f"Current details: {current_book}")
        
        print("\nEnter new values (press Enter to keep current):")
        title = input(f"Title [{current_book['title']}]: ").strip()
        author = input(f"Author [{current_book['author']}]: ").strip()
        genre = input(f"Genre [{current_book['genre']}]: ").strip()
        copies = input(f"Total Copies [{current_book['total_copies']}]: ").strip()
        
        updates = {}
        if title: updates['title'] = title
        if author: updates['author'] = author
        if genre: updates['genre'] = genre
        if copies: 
            try:
                updates['total_copies'] = int(copies)
            except ValueError:
                print("Error: Copies must be a number")
                continue
        
        if updates:
            success, message = operations.update_book(isbn, **updates)
            print(f"Result: {message}")
        else:
            print("No changes made.")

    elif choice == "5":
        print("\n--- Update Member ---")
        member_id = input("Enter Member ID to update: ")
        
        # Find member
        member = None
        for m in operations.members:
            if m['member_id'] == member_id:
                member = m
                break
                
        if not member:
            print("Member not found!")
            continue
            
        print(f"Current details: {member}")
        
        print("\nEnter new values (press Enter to keep current):")
        name = input(f"Name [{member['name']}]: ").strip()
        email = input(f"Email [{member['email']}]: ").strip()
        
        updates = {}
        if name: updates['name'] = name
        if email: updates['email'] = email
        
        if updates:
            success, message = operations.update_member(member_id, **updates)
            print(f"Result: {message}")
        else:
            print("No changes made.")

    elif choice == "6":
        print("\n--- Delete Book ---")
        isbn = input("Enter ISBN of book to delete: ")
        
        # Show book details before deletion
        if isbn in operations.books:
            book = operations.books[isbn]
            print(f"Book to delete: {book['title']} by {book['author']}")
            confirm = input("Are you sure? (y/N): ").strip().lower()
            if confirm == 'y':
                success, message = operations.delete_book(isbn)
                print(f"Result: {message}")
            else:
                print("Deletion cancelled.")
        else:
            print("Book not found!")

    elif choice == "7":
        print("\n--- Delete Member ---")
        member_id = input("Enter Member ID to delete: ")
        
        # Find member
        member = None
        for m in operations.members:
            if m['member_id'] == member_id:
                member = m
                break
                
        if not member:
            print("Member not found!")
            continue
            
        print(f"Member to delete: {member['name']} ({member['email']})")
        print(f"Borrowed books: {len(member['borrowed_books'])}")
        
        confirm = input("Are you sure? (y/N): ").strip().lower()
        if confirm == 'y':
            success, message = operations.delete_member(member_id)
            print(f"Result: {message}")
        else:
            print("Deletion cancelled.")

    elif choice == "8":
        print("\n--- Borrow Book ---")
        member_id = input("Enter Member ID: ")
        isbn = input("Enter ISBN: ")
        success, message = operations.borrow_book(member_id, isbn)
        print(f"Result: {message}")

    elif choice == "9":
        print("\n--- Return Book ---")
        member_id = input("Enter Member ID: ")
        isbn = input("Enter ISBN: ")
        success, message = operations.return_book(member_id, isbn)
        print(f"Result: {message}")

    elif choice == "10":
        display_all_books()

    elif choice == "11":
        display_all_members()

    elif choice == "12":
        print("Exiting system. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")