forfattere = ["Andersen", "Madsen", "Jensen", "Klaussen", "Laurssen"]

for x in forfattere:
    print(x)

print(" ")

forfattere.append("Jensen")

for x in forfattere:
    print(x)

print(" ")

forfattere.pop(1)

for x in forfattere:
    print(x)


arrayLength = len(forfattere)
print(arrayLength)

forfattere.reverse()

for x in forfattere:
    print(x)