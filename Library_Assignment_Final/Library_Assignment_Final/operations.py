# operations.py - Core Library Operations

books = {}
members = []
genres = ("Fiction", "Non-Fiction", "Sci-Fi", "History", "Biography")

def add_book(isbn, title, author, genre, total_copies):
    if isbn in books:
        return False, "Book already exists."
    if genre not in genres:
        return False, "Invalid genre."
    books[isbn] = {
        "title": title, 
        "author": author, 
        "genre": genre, 
        "total_copies": total_copies, 
        "available_copies": total_copies
    }
    return True, "Book added successfully."

def add_member(member_id, name, email):
    for m in members:
        if m["member_id"] == member_id:
            return False, "Member already exists."
    members.append({
        "member_id": member_id, 
        "name": name, 
        "email": email, 
        "borrowed_books": []
    })
    return True, "Member added successfully."

def search_books(keyword):
    results = []
    for isbn, book in books.items():
        if (keyword.lower() in book["title"].lower() or 
            keyword.lower() in book["author"].lower()):
            results.append({
                "isbn": isbn,
                "title": book["title"],
                "author": book["author"], 
                "genre": book["genre"],
                "total_copies": book["total_copies"],
                "available_copies": book["available_copies"]
            })
    return results

def update_book(isbn, **kwargs):
    if isbn not in books:
        return False, "Book not found."
    
    valid_fields = ['title', 'author', 'genre', 'total_copies']
    for field, value in kwargs.items():
        if field in valid_fields:
            if field == 'genre' and value not in genres:
                return False, "Invalid genre."
            
            if field == 'total_copies':
                # If increasing total copies, also increase available copies
                current_total = books[isbn]['total_copies']
                current_available = books[isbn]['available_copies']
                if value > current_total:
                    # Increase available copies by the difference
                    books[isbn]['available_copies'] += (value - current_total)
                elif value < current_total:
                    # Can't reduce total copies below currently borrowed count
                    borrowed_count = current_total - current_available
                    if value < borrowed_count:
                        return False, f"Cannot reduce total copies below currently borrowed count ({borrowed_count})"
                    books[isbn]['available_copies'] = value - borrowed_count
            
            books[isbn][field] = value
    
    return True, "Book updated successfully."

def update_member(member_id, **kwargs):
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if not member:
        return False, "Member not found."
    
    valid_fields = ['name', 'email']
    for field, value in kwargs.items():
        if field in valid_fields:
            member[field] = value
    
    return True, "Member updated successfully."

def delete_book(isbn):
    if isbn not in books:
        return False, "Book not found."
    
    # Check if any copies are borrowed
    if books[isbn]["available_copies"] < books[isbn]["total_copies"]:
        return False, "Cannot delete book - copies are currently borrowed"
    
    del books[isbn]
    return True, "Book deleted successfully."

def delete_member(member_id):
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if not member:
        return False, "Member not found."
    
    # Check if member has borrowed books
    if member["borrowed_books"]:
        return False, "Cannot delete member - they have borrowed books"
    
    members.remove(member)
    return True, "Member deleted successfully."

def borrow_book(member_id, isbn):
    # Find member
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if not member:
        return False, "Member not found."
    
    # Check book exists
    if isbn not in books:
        return False, "Book not found."
    
    # Check borrow limit
    if len(member["borrowed_books"]) >= 3:
        return False, "Borrow limit reached."
    
    # Check availability
    if books[isbn]["available_copies"] <= 0:
        return False, "No copies available."
    
    # Check if already borrowed
    if isbn in member["borrowed_books"]:
        return False, "Member already has this book borrowed."
    
    # Process borrowing
    books[isbn]["available_copies"] -= 1
    member["borrowed_books"].append(isbn)
    return True, "Book borrowed successfully."

def return_book(member_id, isbn):
    # Find member
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if not member:
        return False, "Member not found."
    
    # Check book exists
    if isbn not in books:
        return False, "Book not found."
    
    # Check if book is borrowed by this member
    if isbn not in member["borrowed_books"]:
        return False, "Book not borrowed by this member."
    
    # Process return
    member["borrowed_books"].remove(isbn)
    books[isbn]["available_copies"] += 1
    return True, "Book returned successfully."

def get_all_books():
    """Utility function to get all books"""
    return books

def get_all_members():
    """Utility function to get all members"""
    return members

if __name__ == "__main__":
    print("Library operations module loaded successfully.")
    print("Run demo.py to use the full Library Management System.")