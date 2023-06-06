#A-M -> N-Z 65-77 -> 78-90
#N-Z -> A-M 78-90 -> 65-77
#a-m -> n-z 97-109 -> 110-122
#n-z -> a-m 110-122 -> 97 -> 109


def rot13(text):
    new_text_buffer = ""
    for char in text:
        char_val = ord(char)
        if char_val < 91: #Upper Case Letters
            if char_val < 78:
                new_text_buffer += chr(char_val + 12)
            else:
                new_text_buffer += chr(char_val - 12)
        elif char_val < 123:
            if char_val < 110:
                new_text_buffer += chr(char_val + 12)
            else:
                new_text_buffer += chr(char_val - 12)
        else:
            new_text_buffer += "?"
    return new_text_buffer

print(rot13("Hello"))
print(rot13("Tqxxc"))