def unpack(data):
    """
    unpacks the package
    :param data: the package to unpack
    :return: tupale (opcode, params)
    """
    opcode = data[0:1]
    params = data[1:].split("#!#")
    return (opcode, params)
