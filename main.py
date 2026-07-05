from utils.generate import generate

# print(generate("Write a short story about a robot learning to love."))
import json

with open("AR.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)

