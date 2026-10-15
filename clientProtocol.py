def unpack(data):
    """
    unpacks the package
    :param data: the package to unpack
    :return: tuple (opcode, params)
    """
    opcode = data[0:1].decode()
    if opcode in ["4", "I"]:
        params = data[1:].split(b"#!#", 1)
    else:
        params = data[1:].decode().split("#!#")
    return (opcode, params)
