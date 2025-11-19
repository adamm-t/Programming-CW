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

