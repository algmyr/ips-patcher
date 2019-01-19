import sys

class Reader:
    def __init__(self,S):
        self.i = 0
        self.S = S
    def read(self,n):
        s = self.S[self.i:self.i+n]
        self.i += n
        return s
    def peek(self,n):
        s = self.S[self.i:self.i+n]
        return s
    def skip(self,n):
        self.i += n
    def readint(self,n):
        b = self.read(n)
        return sum(a << (i*8) for i,a in enumerate(b[::-1]))

class IPSReader(Reader):
    def readrecord(self):
        off = ips.readint(3)
        size = ips.readint(2)
        if size == 0:
            # RLE
            size = ips.readint(2)
            value = ips.readint(1)
            data = [value]*size
        else:
            data = ips.read(size)
        return off,data
    @property
    def records(self):
        self.i = 0
        assert ips.read(5) == b'PATCH'
        while ips.peek(3) != b'EOF':
            yield ips.readrecord()

if len(sys.argv) != 4:
    print(f'Usage: {sys.argv[0]} [ips file] [in rom] [out rom]')
    sys.exit(1)

# Open patch and rom
with open(sys.argv[1], 'rb') as f:
    ips = IPSReader(f.read())
with open(sys.argv[2], 'rb') as f:
    rom = bytearray(f.read())

for off,data in ips.records:
    rom[off:off+len(data)] = data

with open(sys.argv[3], 'wb') as f: f.write(rom)
