#! /usr/bin/env python
# encoding: utf-8

# Export gnome keyring passwords as json

import gnomekeyring as gk
import json
import codecs

class Exporter:
    def __init__(self):
        pass
    
    def check_exists(self, keyring):
        return keyring in gk.list_keyring_names_sync()
    
    def get_passwords(self, keyring):
        keys = gk.list_item_ids_sync(keyring)
        result = list()
        for key in keys:
            try:
                item_info = gk.item_get_info_sync(keyring, key)
            except gk.IOError:
                return "Keyring is locked"
            result.append((key, item_info.get_display_name(), item_info.get_secret()))
        return result
    
    def export_json(self, keyring, outfilename):
        with codecs.open(outfilename, 'w', 'utf-8') as out:
            data = self.get_passwords(keyring)
            outp = json.dumps(data, sort_keys=True, indent=4)
            out.write(outp)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print "Usage: %s keyring outputfile" % sys.argv[0]
        exit(1)
    keyring = sys.argv[1]
    outfilename = sys.argv[2]
    e = Exporter()
    if e.check_exists(keyring):
        e.export_json(keyring, outfilename)
