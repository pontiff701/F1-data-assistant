import driverInfo
import raceInfo
import personalAnalysis
import team
import guess

def main():
    print("Welcome to your Formula 1 assistant!")
    print("1. Get annual results")
    print("2. Get races' results")
    print("3. Driver's Analysis")
    print("4. Get team historical data")
    print("5. Guess the team!")
    print("6. Exit")

    while True:
        choice = input("Please pick a feature:")
        if choice == '1':
            return driverInfo.main()   
        if choice == '2':
            return raceInfo.main()
        if choice == '3':
            return personalAnalysis.main()
        if choice == '4':
            return team.main()
        if choice == '5':
            return guess.main()
        if choice == '6':
            return False
        else:
            print("Please enter an integer from 1 to 6.")
            main()
main()
