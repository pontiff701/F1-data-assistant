def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")

def YorN(question):
    '''
    decide the user's input is 'yes' or 'no'
    
    Parameters
    ----------
    question [string]: the question with the yes/no answer

    Returns
    -------
    True [bool]: the input is yes
    False [bool]: the input is no
    '''
    boolean = input(question)
    if boolean.lower() == "yes":
        return True
    elif boolean.lower() == "no":
        return False
    else:
        print("please enter 'yes' or 'no'.")
        return YorN(question)

def saveTree(tree, treeFile):
    """
    Save the tree to a file, differentiating between internal nodes and leaf nodes.
    """
    if isinstance(tree, tuple):
        # Check if the tree node has the correct number of elements
        if len(tree) == 3:
            text, left, right = tree

            # Check if the node is a leaf node
            if left is None and right is None:
                print(f"Leaf: {text}", file=treeFile)
            else:
                print(f"Internal Node: {text}", file=treeFile)
                if left is not None:
                    saveTree(left, treeFile)
                if right is not None:
                    saveTree(right, treeFile)
        elif len(tree) == 2:
            # Handle nodes with only 2 elements (possible data inconsistency)
            text, child = tree
            print(f"Internal Node: {text}", file=treeFile)
            if child is not None:
                saveTree(child, treeFile)
        else:
            # Handle nodes with unexpected formats
            print(f"Unexpected Node Format: {tree}", file=treeFile)
    else:
        # Handle leaf nodes or other unexpected formats
        print(f"Leaf or Unexpected Format: {tree}", file=treeFile)



def loadTree(treeFile):
    '''
    Load the tree from a txt file.

    Parameters
    ----------
    treeFile [txt file]: the txt file

    Returns
    -------
    loaded [list]: tree
    '''
    with open(treeFile, 'r') as file:
        lines = file.readlines()

    # Clean and parse the lines
    nodes = []
    for line in lines:
        if line.startswith("Internal Node:"):
            text = line.strip().split("Internal Node: ")[1]
            nodes.append((text, None, None))  # Placeholder for children
        elif line.startswith("Leaf:"):
            text = line.strip().split("Leaf: ")[1]
            nodes.append((text, None, None))  # Leaf node

    # Function to recursively build the tree
    def build_tree(index=0):
        if index >= len(nodes):
            return None

        node = nodes[index]
        if node[1] is None and node[2] is None:  # If children are not set
            if lines[index].startswith("Internal Node:"):
                left_child = build_tree(index * 2 + 1)
                right_child = build_tree(index * 2 + 2)
                return (node[0], left_child, right_child)
            else:
                # Leaf node
                return node

    return build_tree()
