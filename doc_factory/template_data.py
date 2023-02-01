from dataclasses import dataclass
import hashlib
import time

def gen_doc_id() -> str:
    cur_time =  str(time.time())
    encoded_str =  cur_time.encode()
    hexdigest = hashlib.sha256(encoded_str).hexdigest()
    return hexdigest.rsplit(':', maxsplit=1)[-1].strip()

@dataclass
class DocumentTemplate:
    name: str = ''
    template_loc: str = ''



if __name__=='__main__':
    gen_doc_id()