from browser_use.browser.kawaii import KawaiiRyugagotokuClass

OPEN_AI_TOKEN = 0
ES_PASS = 1
MDB_PASS = 2

ENCRYPTED_CREDENTIAL = {
    OPEN_AI_TOKEN: "",
    ES_PASS: "",
    MDB_PASS: "",
}

DECRYPTED_CREDENTIAL = KawaiiRyugagotokuClass.descrypt_dict(ENCRYPTED_CREDENTIAL)