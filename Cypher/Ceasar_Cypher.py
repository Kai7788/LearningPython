#Bounds : 33 to 126 allowed


def encode(text, shiftvalue):
    new_text_buffer = ""
    for char in text:
        char_val = ord(char) + shiftvalue
        if char_val > 126:
            #Example 133 => 133 - 126 => 7 + 32 => 39
            char_val = 32 + (char_val - 126)
            new_text_buffer += chr(char_val)
        elif char_val < 33:
            #Example 28 - 33 => -5 + 127 => 122
            char_val = (char_val - 33) + 127
            new_text_buffer += chr(char_val)
        else:
            new_text_buffer += chr(char_val)
    return new_text_buffer

def decode(text, shiftvalue):
    shiftvalue = shiftvalue * -1
    new_text_buffer = ""
    for char in text:
        char_val = ord(char) + shiftvalue
        if char_val > 126:
            #Example 133 => 133 - 126 => 7 + 32 => 39
            char_val = 32 + (char_val - 126)
            new_text_buffer += chr(char_val)
        elif char_val < 33:
            #Example 28 - 33 => -5 + 127 => 122
            char_val = (char_val - 33) + 127
            new_text_buffer += chr(char_val)
        else:
            new_text_buffer += chr(char_val)
    return new_text_buffer
    