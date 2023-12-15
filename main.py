import driverInfo
import raceInfo
import personalAnalysis
import guess
def main():
    print("Welcome to your Formula 1 assistant!")
    print("1. Get annual results")
    print("2. Get races' results")
    print("3. Driver's Analysis")
    print("4. Guess the team!")

    while True:
        choice = input("Please pick a feature:")
        if choice == '1':
            return driverInfo.main()   
        if choice == '2':
            return raceInfo.main()
        if choice == '3':
            return personalAnalysis.main()
        if choice == '4':
            return guess.main()
main()
print("Thanks, bye!")

