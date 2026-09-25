import re

# Method 1: Simple using isalnum()
s = input("Enter string: ")
if s.isalnum():
    print("Valid - Only a-z, A-Z, 0-9")
else:
    print("Invalid - Contains special character")

# Method 2: Using Regex (As per Aim)
pattern = r'^[a-zA-Z0-9]+$'
if re.match(pattern, s):
    print("Valid String")
else:
    print("Invalid String")


OUTPUT:
Enter string: MITWPU123
Valid - Only a-z, A-Z, 0-9

Enter string: Hello@123
Invalid - Contains special character
