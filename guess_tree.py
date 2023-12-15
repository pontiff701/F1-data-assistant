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
    '''
    Saves given tree in specified file.

    Parameters
    ----------
    tree [List]: the question tree
    treeFile [txt file]: the txt file with  

    Returns
    -------
    none
    '''
    text, left, right = tree
    if left is None and right is None:
        print('Leaf', file = treeFile)
        print(text, file = treeFile)
        
    else:
        print('Internal Node', file = treeFile)
        print(text, file = treeFile)
        saveTree(left, treeFile)
        saveTree(right, treeFile)

def loadTree(treeFile):
    '''
    load the tree from a txt file.

    Parameters
    ----------
    treeFile [txt file]: the txt file with  

    Returns
    -------
    loaded [list]: tree
    '''
    inputFile = treeFile.readlines()
    cleanList = [lines.strip('\n') for lines in inputFile]
    info = []

    for i in range(0, len(cleanList), 2):
        info.append((cleanList[i], cleanList[i+1]))
    for i in range(len(info)):
        if info[i][0] == "Leaf":
            info[i] = (info[i][1], None, None)
    
    isTrue = True
    while isTrue:
        popList = []
        for i in range(len(info)-1, -1, -1):
            if len(info[i]) == 2 and info[i][0] == 'Internal Node':
                info[i] = (info[i][1], info[i+1], info[i+2])
                popList.append(i+1)
                popList.append(i+2)
                break
    
        for i in reversed(popList):
            info.pop(i)
            
        count = 0
        for i in range(len(info)):
            if info[i][0] == 'Internal Node':
                count += 1
        
        if count == 0:
            isTrue = False
            
    loaded = info[0]
    
    return loaded