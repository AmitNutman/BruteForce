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
    pack range msg
    :param start: the first number to check on this range
    :param end: the last number to check on this range
    :return: str - range to check
    """
    return f"1#!#{start}#!#{end}"



def pack_answer_found():
    """
    packs the msg that tells all clients that the answer was found
    :return: str
    """
    return "2"