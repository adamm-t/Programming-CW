#Intro to Programming CW
#Adam Tamer 202400705

#we will define the constants first
terminator = "01111110"
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
        text += chr(int(byte, 2))
    return text

#now we make the function that does the actual encoding process
def encode_message():
    print("\n--- ENCODING ---")
    bmp_name = input("Enter BMP file name to encode into: ")

#now we attempt to read the BMP file and check that a BMP file is being used by looking for the BM signature in the first 2 bytes and return error if not found 
    try:
        with open(bmp_name, "rb") as f:
            bmp_bytes = bytearray(f.read())
            
        if bmp_bytes[0:2] != b"BM":
            print("Error: File is not a BMP image.")
            return
    except:
        print("Error: File not found.")
        return

#here we take the message from the user either as a direct input or read from a file (dual input method)
    print("\nHow would you like to input the secret message?")
    print("1 - Type the message manually")
    print("2 - Read the message from a text file")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        message = input("Enter the secret message to hide: ")
        if message == "":
            print("Error: please input a message to hide")
            return

    elif choice == "2":
        file_name = input("Enter the text file name: ")

        try:
            with open(file_name, "r", encoding="utf-8") as f:       #we open the file and read with utf-8 encoding which is the best option since it will read almost all possible characters that are used
                message = f.read().strip()                          #strip() will remove anything we dont need that is before or after the message like spaces
        except:
            print("Error: Could not read the text file.")
            return

        if message == "":
            print("Error: the text file is empty.")
            return

        print(f"Loaded message ({len(message)} characters) from file.") #print the length of the message for the user to see how long it is

    else:
        print("Invalid choice.")
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
    output_name = "modified_" + bmp_name
    with open(output_name, "wb") as f:
        f.write(bmp_bytes)

    print(f"Message encoded successfully into: {output_name}")

#encoding function is done so now we make the decoder
def decode_message():
    print("\n--- DECODING ---")
    bmp_name = input("Enter BMP file name to decode message from: ")

#here we will attempt to read from the BMP file all the bits and make sure to check for the same errors again
    try:
        with open(bmp_name, "rb") as f:
            bmp_bytes = f.read()

        if bmp_bytes[0:2] != b"BM":
            print("Error: File is not a BMP image.")
            return
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
    print(f"Your secret message is:\n{hidden_message}")


#lastly we will make our main menu that lets the user choose what mode they want to use in our program
def menu():
    while True:
        print("\n======== Adam's Steganography Program ========")
        print("1 - Encode message into a bitmap image")
        print("2 - decode message from a bitmap image")
        print("3 - Exit")
        print("==============================================")

        choice = input("Enter your selection: ")

        if choice == "1":
            encode_message()
        elif choice == "2":
            decode_message()
        elif choice == "3":
            print("Closing Program.")
            exit()
        else:
            print("Please choose a valid option.")

#here we call the menu function so that the program begins and lets the user choose their mode
menu()

