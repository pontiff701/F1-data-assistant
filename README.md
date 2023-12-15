# [SI507] F1 Assistant
This is a program that can help you to search some F1 information from the official website. It also have a small game that can guess the team according to your answer to the questions.
## Main Menu:
![Alt text](image-6.jpg)
* The file `main.py` is the main program of the project, click it to start.
* You will have 5 options:
    - Find the driver's annual performance
    - Fine the race results
    - Analyze the driver's performance
    - start the 20 questions game
    - quit the program

## Race Results
![Alt text](image-1.png)
* enter the year:
    - you can select only one year like 2023 
    - you can also select multiple years like 2020, 2023 (2020-2023)
* select the race you want to search:

    just enter the index showed below, "0" means all races.
* The program will save the results into a txt file "race_info.txt" with clear format.

## Driver & Team Info
![Alt text](image-3.png)
* enter the year:
    - you can select only one year like 2023 
    - you can also select multiple years like 2020, 2023 (2020-2023)
* The program will save the results into txt file "year_data.txt" and "team.txt" with clear format.

## Personal Analysis:
![Alt text](image.png)
* enter the driver's name, then the program will show his historical annual performace.

## 20 Questions Game:
![Alt text](image-5.png)
* First, you will be asked to load a existing tree from a file, you can enter yes or no.
* Then, the game begin, you can only enter yes or no for each question.
    - If the program don't know the answer, it will ask you to input the answeer and the related question.
    - If the program get the correct answer, it will let you know.
* After that, you will be asked to play again, you can enter yes or no.
* Last, the program will ask you if you want to save the current question tree for the future playing.
    - If yes, you need to enter the file name to finish the process.
    - If no, the program will be shutdown.