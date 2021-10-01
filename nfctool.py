import nfc
import ndef
import sys


class NFCtool:
    def __init__(self, device):
        print("Place the NFC Card on the device.")
        self.clf = nfc.ContactlessFrontend(device)
        self.tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})

    def read_nfc(self):
        records = self.tag.ndef
        print("Readable: " + records.is_readable())
        print("Writeable: " + records.is_writeable())
        # data = records.text.split('\n')
        self.clf.close()
        return records

    def write_nfc(self):
        record = ndef.UriRecord("https://zaba.dev/")
        print(record.iri)
        print(record.uri)
        formatting = self.tag.format()
        print(formatting)
        test = b''.join(ndef.message_encoder([record]))
        self.clf.close()
        return "Data written."


if __name__ == '__main__':
    if not isinstance(sys.argv[1], str):
        raise Exception("Missing argument")
    nfct = NFCtool(sys.argv[1])
    # print(nfct.read_nfc())
    print(nfct.write_nfc())
