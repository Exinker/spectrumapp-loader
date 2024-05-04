from spectrumapp_loader.loaders import BinaryLoader


if __name__ == '__main__':
    filepath = r'C:\\Atom x64 3.3 (2023.06.01)\\External\\data\\ИСП-ИНХ-Co-Mn-Pb в MgCaNa\\dump.pkl'

    dump = BinaryLoader().load(filepath)

    print(dump.line)
    print(dump.active)
