def hex_to_binary(hex_string):
    binary_string = bin(int(hex_string, 16))[2:]
    return binary_string.zfill(len(hex_string) * 4)


#INPUT YOUR HEX VALUE HERE
#########################
hex_value = "C1DA1AFB"
#########################



hex_pairs = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]

binary_values = [hex_to_binary(pair) for pair in hex_pairs]
binary_result = ''.join(binary_values)

# Extracting the first bit, next 8 bits, and the rest
first_bit = int(binary_result[0])
next_eight_bits = int(binary_result[1:9], 2)
the_rest = int(binary_result[9:], 2)

# Calculate the result of the equation
result = (-1) ** first_bit * 2 ** (next_eight_bits - 127) * (1 + the_rest * 2 ** -23)

print("Result of the equation:", result)
