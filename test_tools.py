from tools import (
    calculate_hashes, convert_timestamp, extract_iocs,
    check_file_signature, search_notes,
)

print(calculate_hashes.invoke({"text": "evidence01"}))
print()
print(convert_timestamp.invoke({"value": "1700000000"}))
print(convert_timestamp.invoke({"value": "133000000000000000"}))
print()
print(extract_iocs.invoke({"text": "Beacon to 185.220.101.4 and http://evil-site.ru/a.exe, contact bad@evil-site.ru"}))
print()
print(check_file_signature.invoke({"hex_bytes": "25 50 44 46 2D 31"}))
print()
print(search_notes.invoke({"query": "chain of custody"})[:300])