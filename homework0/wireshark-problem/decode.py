hex_data = "33393538646339652d373132662d343337372d383565392d666563346236613634343261"
ascii_string = bytes.fromhex(hex_data).decode()
print(ascii_string)

