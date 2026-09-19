#Python program that accepts the length of three sides of a triangle as inputs. 
def is_right_angled(a, b, c):
    # sort sides to get hypotenuse as largest
    sides = sorted([a, b, c])
    # check pythagoras theorem
    return sides[0]**2 + sides[1]**2 == sides[2]**2

def main():
    print("=== Assignment 3: Right Angled Triangle Check ===\n")
    a = int(input("Enter side 1: "))
    b = int(input("Enter side 2: "))
    c = int(input("Enter side 3: "))

    if is_right_angled(a, b, c):
        print(f"\nTriangle with sides {a},{b},{c} IS a Right Angled Triangle.")
    else:
        print(f"\nTriangle with sides {a},{b},{c} is NOT a Right Angled Triangle.")

if __name__ == "__main__":
    main()


OUTPUT:
=== Assignment 3: Right Angled Triangle Check ===

Enter side 1: 34
Enter side 2: 23
Enter side 3: 47

Triangle with sides 34,23,47 is NOT a Right Angled Triangle.
