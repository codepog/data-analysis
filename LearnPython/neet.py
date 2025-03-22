print("hello world",3)

data = {"neet" : "code", "NEET" : "code"} #hashmap or dictionary
data["neet"] = "dog"
print(data)

for key, val in data.items():
    print(key + '=' + val)

for i in range(10):
    print(i)

def get_sum(a, b):
    return a + b

print(get_sum(1,2))