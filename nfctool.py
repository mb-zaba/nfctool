import nfc
import ndef
import sys


class NFCtool:
    def __init__(self, device):
        self.clf = nfc.ContactlessFrontend(device)
        self.tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})

    def read_nfc(self):
        records = self.tag
        # data = records.text.split('\n')
        return records


if __name__ == '__main__':
    if not isinstance(sys.argv[1], str):
        raise Exception("Missing argument")
    nfct = NFCtool(sys.argv[1])
    print(nfct.read_nfc())
    # nfct.clf.close()
