#Intro to Programming CW
#Adam Tamer 202400705

#we will define the constants first
terminator = "00000000"
header_size = 54


#now we will make each function

#first we have the function that converts our string characters into 8 bit binary and adds the terminator at the end of it
def text_to_binary(text):
    bits = ""
    for char in text:
        bits += format(ord(char), "08b")
    return bits + terminator

#now we make a function that converts from binary (8 bits at a time) to text  which will be used in decoding
def binary_to_text(bits):
    text = ""
    for i in range(0, len(bits),8):
        byte = bits[i:i+8]
        text = chr(int(byte, 2))
    return text

#now we make the function that does the actual encoding process
def encode_message():
    print("\n--- ENCODING ---")
    bmp_name = input("Enter BMP file name to encode into: ")

#now we attempt to read the BMP file and make sure a message is entered for the encoding process to work
    try:
        with open(bmp_name, "rb") as f:
            bmp_bytes = bytearray(f.read())
    except:
        print("Error: File not found.")
        return
    
    message = input("Enter the secret message to hide: ")
    if message == "":
        print("Error: please input a message to hide")
        return
    
#here we convert the message into binary using the function we made and store it into a variable
    message_bits = text_to_binary(message)

#check if message will fit inside the image by comparing number of bits needed for message and number of bits available in image after subtracting header pixels
    if len(message_bits) > len(bmp_bytes) - header_size:
        print("Error: message is too long for this image.")
        return
    
    pixel_index = header_size

#now we replace the LSB of each byte with the bits from our message using bitwise operations AND to clear the LSB and then OR to write the LSB
    for bit in message_bits:
        bmp_bytes[pixel_index] &= 0b11111110
        bmp_bytes[pixel_index] |= int(bit)
        pixel_index += 1
    
#here we save our new image which contains the message as a new file with a different name   
    output_name = "new_image_" + bmp_name
    with open(output_name, "wb") as f:
        f.write(bmp_bytes)

    print(f"Message encoded successfully into: {output_name}")

#encoding function is done so now we make the decoder
def decode_message():
    print("\n--- DECODING ---")
    bmp_name = input("Enter BMP file name to decode message from: ")

#here we will attempt to read from the BMP file all the bits
    try:
        with open(bmp_name, "rb") as f:
            bmp_bytes = f.read()
    except:
        print("Error: File not found.")
        return

#we make sure to set our constants like the header size and an empty string that will contain the bits from our message    
    pixel_index = header_size
    bits_collected = ""

#now we have a loop that increments through each pixel and adds our bit to the string until it finds the terminator and stops
    while True:
        lsb = bmp_bytes[pixel_index] & 1
        bits_collected += str(lsb)
        pixel_index += 1

        if bits_collected.endswith(terminator):
            break

#check if we reached the end of the file and still didnt find the terminator so an error has occured
        if pixel_index >= len(bmp_bytes):
            print("Error: No terminator found, file may be corrupted.")
            return

#here we slice our bits and remove the terminator so it doesnt affect the message       
    bits_collected = bits_collected[:-8]

#call the function that converts our bits to text and store it in a variable and print it for the user to see
    hidden_message = binary_to_text(bits_collected)
    print(f"Your secret message is {hidden_message}")




