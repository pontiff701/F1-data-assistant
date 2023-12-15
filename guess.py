from guess_tree import *

smallTree = \
    ("Is it bigger than a breadbox?",
        ("an elephant", None, None),
        ("a mouse", None, None))

mediumTree = \
    ("Has the team won a Constructors' Championship between 2018 and 2023?",
        ("Is the primary color of the car red?",
            ("Ferrari", None, None),
            ("Is the primary color of the car silver or black?",
                ("Mercedes", None, None),
                ("Red Bull Racing", None, None))),
        ("Is the team known for a notable driver like Fernando Alonso or Sebastian Vettel since 2018?",
            ("Is the team known for its British heritage?",
                ("Has the team been consistently in the top 5?",
                    ("McLaren", None, None),
                    ("Is the team known for a rich F1 history, but struggling in recent years?",
                        ("Williams", None, None),
                        ("Aston Martin", None, None)))),
            ("Is the team associated with a major car manufacturer?",
                    ("Is the team French?",
                        ("Alpine", None, None),
                        ("Is the team Italian?",
                            ("AlphaTauri", None, None),
                            ("Alfa Romeo", None, None))),
                    ("Is the team one of the newer additions to F1?",
                        ("Haas", None, None),
                        ("Is the team known for a distinct color like pink?",
                            ("Racing Point", None, None),
                            ("Other(enter 'no' to add your answer)", None, None))))))



def main():
    '''
    main function of the 20 questions game
    let user decided whether load a tree from file or not.
    let user decided whether save the tree to the file name he/she want.
    let user decided whether replay the game.

    Parameters
    ----------
    none

    Returns
    -------
    none

    '''
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    print("Welcome to 20 Questions!")
    whetherload = YorN("Would you like to load a tree from a file?")
    if whetherload == True:
        filename = input("What's the name of the file?")
        treeFile = open(filename, 'r')
        tree = loadTree(treeFile)
        treeFile.close()
    elif whetherload == False:
        tree = mediumTree
    
    whetherReplay = True
    while whetherReplay:
        tree = play(tree)
        whetherReplay = YorN("Would you like to play again?")
    whetherSave = YorN("Would you like to save this tree for later?")
    if whetherSave == True:
        filename = input("Please enter a file name: ")
        treeFile = open(filename, 'w')
        saveTree(tree, treeFile)
        treeFile.close()
        print("Thank you! The file has been saved.\nBye!")
    elif whetherSave == False:
        print("Bye!")

def simplePlay(tree):
    '''
    Plays the game once by using the tree to guide its questions. 
    Returns True if the correct answer is guessed.
    
    Parameters
    ----------
    tree [List]: the question tree

    Returns
    -------
    True [bool]: correct answer
    False [bool]: wrong answer
    '''
    text, left, right = tree
    if left is None and right is None:
        boolean = YorN(f"Is it {text}?")
        if boolean == True:
            print('I got it!')
            return True
        elif boolean == False:
            print("Drats! What was it?")
            return False
    else: 
        boolean = YorN(text)
        if boolean == True:
            simplePlay(left)
        elif boolean == False:
            simplePlay(right)
    
def play(tree):
    '''
    Plays the game once by using the tree to guide its questions. 
    Returns a new tree that is the result of playing the game on the 
    original tree and learning from the answers.
    
    Parameters
    ----------
    tree [List]: the question tree

    Returns
    -------
    newNode [tuple]: new question & answers
    (text, subTree, rightTree) [tuple]: next question
    '''
    text, left, right = tree
    if left is None and right is None:
        boolean = YorN(f"Is it {text}?")
        if boolean == True:
            print('I got it!')
            return tree
        elif boolean == False:
            item = input('Dart! What was it?')
            question = input(f"What's the question that distinguishes between {item} and {text}?")
            answer = YorN(f"And what's the answer for {item}?")
            if answer == True:
                newNode = (question, (item, None, None), (text, None, None))
                return newNode
            elif answer == False:
                newNode = (question, (text, None, None), (item, None, None))
                return newNode
    else:
        leftTree = left
        rightTree = right
        boolean = YorN(text)
        if boolean == True:
            subTree = play(left)
            return (text, subTree, rightTree)
        elif boolean == False:
            subTree = play(right)
            return (text, leftTree, subTree)
