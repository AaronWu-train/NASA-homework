from PIL import Image

image_file = "secret_mygo.png"
data = ""
message_length = 100

# Open image
img = Image.open(image_file)

# Get pixels' values
pixels = list(img.getdata())

for i in range(message_length):
    if (i * 3 + 2 >= len(pixels)):
        break
    colors = list(pixels[i * 3]) + list(pixels[i * 3 + 1]) + list(pixels[i * 3 + 2])
    binary = ""

    for j in range(8):
        binary = binary + ("1" if colors[j] % 2 == 1 else "0")
    data += chr(int(binary, 2))
    
print(data)
