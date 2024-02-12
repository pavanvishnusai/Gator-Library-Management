import sys
import time

class Books:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy, reservationHeap):
     # Initializing Books representing a book in the library with its attributes and status.
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservationHeap = reservationHeap
         # Additional attributes for a book node in a tree structure.
        self.color = 'black'
        self.parent = None
        self.left = None
        self.right = None

    
    def __repr__(self):
        # If the bookID is None, return "NIL Node"
        if self.bookID is None:
            return "NIL Node"
        # Return a formatted string with the node's attributes
        return (f"Node(bookID={self.bookID}, bookName='{self.bookName}', "
                f"authorName='{self.authorName}', availabilityStatus={self.availabilityStatus}, "
                f"borrowedBy={self.borrowedBy}, reservations={list(self.reservationHeap.heap)})")
    
class BinaryMinimumHeap:
    def __init__(self):
        self.heap = []
    def bubbleUP(self, index):
        parentIndex = (index - 1) // 2
        # Swap with the parent if necessary and continue bubbling up
        if index > 0 and self.heap[index] < self.heap[parentIndex]:
            self.heap[index], self.heap[parentIndex] = self.heap[parentIndex], self.heap[index]
            self.bubbleUP(parentIndex)

    def extractMinimum(self):
        if not self.heap:
            raise IndexError("Extracting from an empty heap is not allowed.")
        # Get the minimum value
        min_val = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self.minimumHeapify(0)
        else:
            self.heap.pop()
        return min_val
    
    def insert(self, k):
        self.heap.append(k)
        self.bubbleUP(len(self.heap) - 1)

    def minimumHeapify(self, index):
        minimum = index
         # Calculating the index of the left and right children.
        leftChild = 2 * index + 1
        rightChild = 2 * index + 2
        if leftChild < len(self.heap) and self.heap[leftChild] < self.heap[minimum]:
            minimum = leftChild
        if rightChild < len(self.heap) and self.heap[rightChild] < self.heap[minimum]:
            minimum = rightChild
        # If the minimum has changed, swap with the current index and heapify again.
        if minimum != index:
            self.heap[index], self.heap[minimum] = self.heap[minimum], self.heap[index]
            self.minimumHeapify(minimum)

   

class RedBlackTree:

    def minimum(self, node):
            while node.left != self.NIL:
                node = node.left
            return node
    
    # Initializing a Red-Black Tree
    def __init__(self):
         # Define NIL as a node with default values
        self.NIL = Books(None, None, None, None, None, BinaryMinimumHeap())
        self.NIL.color = 'black'
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL
        self.insertFixupCount = 0
        
    def delete(self, z):
            if z is None or z == self.NIL:
                return  
            y = z
            # Case where the left child is NIL
            yoriginalColor = y.color
            if z.left == self.NIL:
                x = z.right
                if x != self.NIL:  
                    self.transplant(z, z.right)
             # Case where the right child is NIL
            elif z.right == self.NIL:
                x = z.left
                if x != self.NIL:  
                    self.transplant(z, z.left)
             # Case where both children are present
            else:
                y = self.minimum(z.right)
                yoriginalColor = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    self.transplant(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self.transplant(z, y)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
                if x != self.NIL: 
                    x.parent = y
             # Fixing up the tree if a black node was removed
            if yoriginalColor == 'black':
                self.deleteFixup(x if x != self.NIL else self.root)

    def transplant(self, u, v):
        # If u is the root, set v as the new root
        if u.parent == None:
            self.root = v
        # If u is a left child, set v as the left child of u's parent
        elif u == u.parent.left:
            u.parent.left = v
        # If u is a right child, set v as the right child of u's parent
        else:
            u.parent.right = v
        v.parent = u.parent

    def deleteFixup(self, x):
            # Fixing the tree so that Red-Black properties are maintained after deletion
            while x != self.root and x.color == 'black':
                if x == x.parent.left:
                    w = x.parent.right
                    if w and w.color == 'red':
                        self.flipColor(w)  
                        self.flipColor(x.parent)  
                        self.leftRotate(x.parent)
                        w = x.parent.right
                     # Cases when both of w's children are black
                    if w and w.left.color == 'black' and w.right.color == 'black':
                        w.color = 'red'
                        # Count fix-up operations if color change occurs 
                        if w.color != 'red':
                            self.insertFixupCount += 1  
                        x = x.parent
                    else:
                        if w and w.right.color == 'black':
                            w.left.color = 'black' 
                            w.color = 'red' 
                            # Count fix-up operations if color change occurs
                            if w.left.color != 'black' or w.color != 'red':
                                self.insertFixupCount += 1  
                            self.rightRotate(w)
                            w = x.parent.right
                        w.color = x.parent.color
                        x.parent.color = 'black' 
                        w.right.color = 'black' 
                         # Count fix-up operations if color change occurs
                        if w.color != x.parent.color or x.parent.color != 'black' or w.right.color != 'black':
                            self.insertFixupCount += 2 
                        self.leftRotate(x.parent)
                        x = self.root
                else:
                    ...
            x.color = 'black'
            # Color flip if x is not black 
            if x.color != 'black':
                self.flipColor(x) 
        
    
    def flipColor(self, node):
            if node.color == 'black':
                node.color = 'red'
            else:
                node.color = 'black'
            self.insertFixupCount += 1
        


    def insert(self, node):
            y = None
            x = self.root
            # Traversing the tree to find the correct position for the new node.
            while x != self.NIL:
                y = x
                if node.bookID < x.bookID:
                    x = x.left
                else:
                    x = x.right
            node.parent = y
            if y is None:
                self.root = node
            elif node.bookID < y.bookID:
                y.left = node
            else:
                y.right = node
            # Initializing the new node's children as NIL (leaf nodes) and set its color to red.
            node.left = self.NIL
            node.right = self.NIL
            node.color = 'red'
            self.fixInsert(node)
      
        

    def fixInsert(self, node):
            # Corrects the Red-Black Tree properties after an insertion.
            while node != self.root and node.parent and node.parent.color == 'red':
                uncle = None
                if node.parent == node.parent.parent.left:
                    uncle = node.parent.parent.right
                    if uncle.color == 'red':
                        # Case when uncle is red: recolor and move up the tree.
                        node.parent.color = 'black'
                        uncle.color = 'black'
                        node.parent.parent.color = 'red'
                        self.insertFixupCount += 3  
                        node = node.parent.parent 
                    else:
                        # Cases when uncle is black.
                        if node == node.parent.right:
                            node = node.parent
                            self.leftRotate(node)
                        node.parent.color = 'black'
                        node.parent.parent.color = 'red'
                        self.rightRotate(node.parent.parent)
                        self.insertFixupCount += 2 
                else:
                     # Symmetric case when node's parent is the right child of the grandparent.
                    uncle = node.parent.parent.left
                    if uncle.color == 'red':
                        node.parent.color = 'black'
                        uncle.color = 'black'
                        node.parent.parent.color = 'red'
                        self.insertFixupCount += 3  
                        node = node.parent.parent
                    else:
                         # Symmetric cases when uncle is black.
                        if node == node.parent.left:
                            node = node.parent
                            self.rightRotate(node)
                        node.parent.color = 'black'
                        node.parent.parent.color = 'red'
                        self.leftRotate(node.parent.parent)
                        self.insertFixupCount += 2  
            self.root.color = 'black'
            if self.root.color == 'red':
                self.insertFixupCount += 1 
        

    def leftRotate(self, x):
            if x is None or x.right is None:
                return "Error: 'None' node encountered in leftRotate"
            y = x.right
            x.right = y.left
            if y.left is not None:
                y.left.parent = x
            y.parent = x.parent
            if x.parent is None:
                self.root = y
            elif x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
            y.left = x
            x.parent = y
            return "leftRotate executed successfully"
        

    def rightRotate(self, y):
            if y is None or y.left is None:
                return "Error: 'None' node encountered in rightRotate"
            x = y.left
            # Performing the rotation by adjusting pointers.
            y.left = x.right
            if x.right is not None:
                x.right.parent = y
            x.parent = y.parent
            if y.parent is None:
                self.root = x
            elif y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x
            x.right = y
            y.parent = x
            return "rightRotate executed successfully"
        

    
    def printBooksRange(self, bookID1, bookID2):
        bookDetailsList = []
        self._printBooksRange(self.root, bookID1, bookID2, bookDetailsList)
        return bookDetailsList
    
    def _printBooksRange(self, node, bookID1, bookID2, bookDetailsList):
            if node is not None and node != self.NIL:
                if bookID1 < node.bookID:
                    self._printBooksRange(node.left, bookID1, bookID2, bookDetailsList)
                if bookID1 <= node.bookID <= bookID2:
                    reservations = [str(res[2]) for res in node.reservationHeap.heap] if node.reservationHeap.heap else []
                    bookDetails = (
                        f"BookID = {node.bookID}\n"
                        f"Title = \"{node.bookName}\"\n"
                        f"Author = \"{node.authorName}\"\n"
                        f"Availability = {'Yes' if node.availabilityStatus else 'No'}\n"
                        f"BorrowedBy = {node.borrowedBy if node.borrowedBy else 'None'}\n"
                        f"Reservations = [{', '.join(reservations)}]\n"
                    )
                    bookDetailsList.append(bookDetails)
                if bookID2 > node.bookID:
                    self._printBooksRange(node.right, bookID1, bookID2, bookDetailsList)
        


    def search(self, node, bookID):
            if node is None or node == self.NIL or bookID == node.bookID:
                return node
            if bookID < node.bookID:
                return self.search(node.left, bookID)
            else:
                return self.search(node.right, bookID)
        


class GatorLibrary:

    def __init__(self):
        self.RBTree = RedBlackTree()
        self.colorFlipCount = 0  

    def incrementColorFlipCount(self):
        self.colorFlipCount += 1
        
    def readCommandsFromFile(self, inputFilename):
            with open(inputFilename, 'r') as file:
                commands = file.readlines()
            return commands


    def writeOutputToFile(self, outputFilename, outputLines):
        with open(outputFilename, 'w') as file:
            for line in outputLines:
                file.write(line + '\n')

    def runCommand(self, command):
        try:
            parts = command.strip().replace(')', '(').split('(')
            cmdType = parts[0].strip()
            args = [arg.strip().strip('"') for arg in parts[1].split(',') if arg]

            if cmdType == 'InsertBook':
                args = parts[1].split(',', 3) 
                args = [arg.strip().strip('"') for arg in args]
                try:
                    bookID = int(args[0])
                    bookName = args[1]
                    authorName = args[2]
                    availabilityStatus = args[3] == 'Yes'
                except (ValueError, IndexError) as e:
                    return f"Error in InsertBook arguments: {e}", True
                return self.insertBook(bookID, bookName, authorName, availabilityStatus), True

            elif cmdType == 'PrintBook':
                bookID = int(args[0])
                return self.printBook(bookID), True
            
            elif cmdType == 'BorrowBook':
                patronID = int(args[0])
                bookID = int(args[1])
                patronPriority = int(args[2])
                return self.borrowBook(patronID, bookID, patronPriority), True
            
            elif cmdType == 'PrintBooks':
                bookID1 = int(args[0].strip())
                bookID2 = int(args[1].strip())
                return self.printBooks(bookID1, bookID2), True

            elif cmdType == 'ReturnBook':
                args = [arg.strip().strip('"') for arg in parts[1].split(',')]
                if len(args) < 2:
                    return "Error: Not enough arguments for ReturnBook", True
                try:
                    patronID = int(args[0].strip())
                    bookID = int(args[1].strip())
                except ValueError as e:
                    return f"Error in ReturnBook arguments: {e}", True
                return self.returnBook(patronID, bookID), True
                
            elif cmdType == 'FindClosestBook':
                targetIDStr = command.split('(')[1].split(')')[0].strip()
                try:
                    targetID = int(targetIDStr)
                    targetID = int(targetIDStr)
                except (ValueError, IndexError) as e:
                    return f"Error parsing target ID for FindClosestBook: {e}", True
                return self.findClosestBook(targetID), True
            
            elif cmdType == 'DeleteBook':
                bookID = int(args[0])
                return self.deleteBook(bookID), True
            
            elif cmdType == 'ColorFlipCount':
                return f"Colour Flip Count: {self.colorFlipCount}", True
                
            elif cmdType == 'Quit':
                return "Program Terminated!!", False  
            else:
                return f"Unknown command: {cmdType}", True  
        
        except Exception as e:
            return f"", True  



    def insertBook(self, bookID, bookName, authorName, availabilityStatus):
            newBook = Books(bookID, bookName, authorName, availabilityStatus, None, BinaryMinimumHeap())
            self.RBTree.insert(newBook)
            self.colorFlipCount += self.RBTree.insertFixupCount  
            self.RBTree.insertFixupCount = 0  
            return ""

    def printBook(self, bookID):
            node = self.RBTree.search(self.RBTree.root, bookID)
            if node and node != self.RBTree.NIL:
                reservations = [str(reservation[2]) for reservation in node.reservationHeap.heap] 
                formattedReservations = f"[{', '.join(reservations)}]" if reservations else "[]"
                bookDetails = [
                    f"BookID = {node.bookID}",
                    f"Title = \"{node.bookName}\"",
                    f"Author = \"{node.authorName}\"",
                    f"Availability = {'Yes' if node.availabilityStatus else 'No'}",
                    f"BorrowedBy = {node.borrowedBy if node.borrowedBy else 'None'}",
                    f"Reservations = {formattedReservations}\n" 
                ]
                return '\n'.join(bookDetails)
            else:
                return "BookID not found in the Library\n"
       
        
    def printBooks(self, bookID1, bookID2):
        if bookID1 > bookID2:
            return "Invalid range: Starting ID is greater than ending ID.\n"
        bookDetailsList = self.RBTree.printBooksRange(bookID1, bookID2)

        outputStr = "\n".join(bookDetailsList)
       
        return outputStr


    def borrowBook(self, patronID, bookID, patronPriority):
        node = self.RBTree.search(self.RBTree.root, bookID)
        if not node:
            return "BookID not found in the Library\n"
        # Check if the same patron has already borrowed the book
        if node.borrowedBy == patronID:
            return f"Book {bookID} Already Borrowed by Patron {patronID}\n"

        if node.availabilityStatus:
            node.availabilityStatus = False
            node.borrowedBy = patronID
            return f"Book {bookID} Borrowed by Patron {patronID}\n"

        # If the reservation list is full, deny further reservations
        if len(node.reservationHeap.heap) >= 20:
            return f"Unable to reserve book {bookID} for Patron {patronID}; reservation limit reached.\n"
        timestamp = time.time()  
        node.reservationHeap.insert((patronPriority, timestamp, patronID))
        return f"Book {bookID} Reserved by Patron {patronID}\n"
        

    def returnBook(self, patronID, bookID):
        node = self.RBTree.search(self.RBTree.root, bookID)
        if not node or node == self.RBTree.NIL:
            return "BookID not found in the Library\n"
        # Process the return if the book is currently borrowed by the same patron
        if not node.availabilityStatus and node.borrowedBy == patronID:
            if node.reservationHeap.heap:
                nextPatronInfo = node.reservationHeap.extractMinimum()
                nextPatron = nextPatronInfo[2]
                node.borrowedBy = nextPatron
                return f"Book {bookID} returned by Patron {patronID}\nBook {bookID} allotted to Patron {nextPatron}.\n"
            else:
                node.availabilityStatus = True
                node.borrowedBy = None
                return f"Book {bookID} returned by Patron {patronID} and is now available.\n"
        else:
            return "Return operation failed. Either the book is not borrowed or it is borrowed by another patron.\n"
        

            
    def findClosestBook(self, targetID):
        closestBooks = self._findClosestBook(self.RBTree.root, targetID, [])
        if closestBooks:
            closestBooks.sort(key=lambda book: book.bookID)
            return "\n".join([self.printBook(book.bookID) for book in closestBooks])
        else:
            return "No books available in the library\n"
        

    def _findClosestBook(self, node, targetID, closestBooks):
        
        if node is None or node == self.RBTree.NIL:
            return closestBooks

        if not closestBooks:
            closestBooks.append(node)
        else:
            currentDistance = abs(targetID - node.bookID)
            closestDistance = abs(targetID - closestBooks[0].bookID)

            # Update the closest books list based on the distance comparison.
            if currentDistance < closestDistance:
                closestBooks = [node]
            elif currentDistance == closestDistance:
                closestBooks.append(node)

        if node.bookID < targetID:
            closestBooks = self._findClosestBook(node.right, targetID, closestBooks)
        else:
            closestBooks = self._findClosestBook(node.left, targetID, closestBooks)

        return closestBooks

    
    
    def deleteBook(self, bookID):
        # Search for the book in the Red-Black Tree using its ID.
        node = self.RBTree.search(self.RBTree.root, bookID)
        if node is not None and node != self.RBTree.NIL:
            if node.reservationHeap.heap:
                patronsToNotify = [str(heap_node[2]) for heap_node in node.reservationHeap.heap]
                node.reservationHeap.heap = []  
                self.RBTree.delete(node)
                self.colorFlipCount += self.RBTree.insertFixupCount
                self.RBTree.insertFixupCount = 0  
                return f"Book {bookID} is no longer available. Reservations made by Patrons {','.join(patronsToNotify)} have been cancelled!\n"
            
            else:
                # If there are no reservations, simply delete the book.
                self.RBTree.delete(node)
                self.colorFlipCount += self.RBTree.insertFixupCount
                self.RBTree.insertFixupCount = 0  
                return f"Book {bookID} is no longer available.\n"
        else:
            return "BookID not found in the Library.\n"
        
    def readCommandsFromFile(self, inputFilename):
        try:
            with open(inputFilename, 'r', encoding='utf-8') as file:
                commands = file.readlines()
            return commands
        except IOError as e:
            
            return []

    def writeOutputToFile(self, outputFilename, outputLines):
        with open(outputFilename, 'w') as file:
            for line in outputLines:
                file.write(line + '\n')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python gator_library.py <inputFilename>")
        sys.exit(1)

    inputFilename = sys.argv[1]
    # Create an output filename by appending '_output_file.txt' to the input filename's base name.
    outputFilename = inputFilename.split('.')[0] + "_output_file.txt"
    librarySystem = GatorLibrary()

    commands = librarySystem.readCommandsFromFile(inputFilename)
    outputLines = []

    for command in commands:
        result, continueExecution = librarySystem.runCommand(command.strip())
        if not continueExecution:
            outputLines.append(result)
            break
        outputLines.append(result)
    librarySystem.writeOutputToFile(outputFilename, outputLines)