""" This is ment to be used to handle gui and cli input, by switching functions around. This is """
#
def reciveFileCli(filename, filesize):
    # as if user want toa get file
    while 1:
        answer = raw_input("Getting file %s, with size %d, y to get n to discard " % (filename, filesize))
        if answer is 'y':
            return True
        if answer is 'n':
            return False


def reciveFileGui(filename, filesize):
    # as if user want toa get file
    return False


