import nfc
import argparse
import ndef


class NFCtool:
    def __init__(self):
        self.clf = nfc.ContactlessFrontend('usb')
        self.tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})

    def read_nfc(self):
        records = self.tag
        return records


if __name__ == '__main__':
    nfct = NFCtool()
    print(nfct.read_nfc())
    nfct.clf.close()
