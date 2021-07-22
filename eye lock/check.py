def check(userInput):
	file = open("password.txt", "r")
	password = file.readline()
	password = '0' + password
	if userInput == password:
		return True
	else:
		return False


if __name__ == '__main__':
	userInput = input("Enter password : ")
	if check(userInput):
		print("1")
	else:
		print("0")