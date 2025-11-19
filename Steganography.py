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

#now we make a function that converts from binary back to text which will be used in decoding
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
    


