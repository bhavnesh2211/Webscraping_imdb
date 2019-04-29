user1 = int(input("Enter your minimun number"))
user2 = int(input("Enter your maximun number"))
for i in range(user1, user2):
	if i > 1:
		for j in range(2,i):
			if i % j == 0:
				break
		else:
			print (i)