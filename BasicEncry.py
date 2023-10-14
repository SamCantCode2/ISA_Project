try:
    addr = r"" #insert path
    key = int(input("Enter a numeric key: "))

    f = open(addr, 'rb')
    img = f.read()
    f.close()

    img = bytearray(img)
    print("Byte array before encryption:", img[0:10])
    for ind, val in enumerate(img):
        img[ind] = val ^ key
    print("Byte array after encryption:", img[0:10])
    f = open(addr, 'wb')
    f.write(img)
    f.close()
except Exception:
    print("Error detected, please check program (" + Exception.__name__ +")")

