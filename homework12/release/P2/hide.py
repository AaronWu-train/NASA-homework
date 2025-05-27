from PIL import Image

# Credits: NASA 2023 HW5

image_file = "mygo.png"
data = "NOT_REAL_FLAG"

# Open image
img = Image.open(image_file)

# Get pixels' values
pixels = list(img.getdata())


# Modify pixels' values to store binary data
for i in range(len(data)):
    if (i * 3 + 2 >= len(pixels)):
        raise ValueError("image size is too small")
    colors = list(pixels[i * 3]) + list(pixels[i * 3 + 1]) + list(pixels[i * 3 + 2])

    binary = format(ord(data[i]), "08b")

    for j in range(len(binary)):
        b = binary[j]
        colors[j] = 2 * (colors[j] // 2) + 1 if b == "1" else 2 * (colors[j] // 2)

    pixels[i * 3], pixels[i * 3 + 1], pixels[i * 3 + 2] = tuple(colors[:3]), tuple(colors[3:6]), tuple(colors[6:])

# Save modified image
img.putdata(pixels)
img.save("secret_mygo.png")
