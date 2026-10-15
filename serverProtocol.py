def unpack(data):
    """
    unpacks the package
    :param data: the package to unpack
    :return: tupale (opcode, params)
    """
    opcode = data[0:1]
    params = data.split("#!#")[1:]
    return (opcode, params)


def pack_range_to_check(start, end):
    """

    :param start:
    :param end:
    :return:
    """
    return f"1#!#{start}#!#{end}"