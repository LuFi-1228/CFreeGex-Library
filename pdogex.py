from parser import convert_expression_in_PA

class pdogex:
    def __init__(self):
        self.automata = None
        self.postfix = None
        self.memo = {}

    def compile(self, expression):
        self.postfix, self.automata = convert_expression_in_PA(expression, "./expressao.jflap")
        self.memo.clear()

    def _accepts(self, substring):
        if substring in self.memo:
            return self.memo[substring]
        result = self.automata.execute(substring)
        self.memo[substring] = result
        return result

    def fullmatch(self, string):
        return self._accepts(string)

    def match(self, string):
        for i in range(len(string)):
            for j in range(i+1, len(string)+1):
                if self._accepts(string[i:j]):
                    return i
        return -1

    def find(self, string):
        n = len(string)
        for i in range(n):
            for j in range(i + 1, n + 1):
                if self._accepts(string[i:j]):
                    return (i, j)
        return None

    def find_all(self, string):
        results = []
        n = len(string)
        for i in range(n):
            for j in range(i + 1, n + 1):
                if self._accepts(string[i:j]):
                    results.append(string[i:j])
        return results

    def replace(self, string, replace):
        pos = self.find(string)
        if not pos:
            return string
        i, j = pos
        return string[:i] + replace + string[j:]

    def replace_all(self, string, replace):
        n = len(string)
        out = []
        pos = 0
        while pos < n:
            found = None
            for start in range(pos, n):
                for end in range(start + 1, n + 1):
                    if self._accepts(string[start:end]):
                        found = (start, end)
                        break
                if found:
                    break
            if not found:
                out.append(string[pos:])
                break
            s, e = found
            if s > pos:
                out.append(string[pos:s])
            out.append(replace)
            pos = e
        return ''.join(out)
    
    def search(self, string):
        n = len(string)
        for i in range(n):
            for j in range(i+1, n+1):
                if self._accepts(string[i:j]):
                    return (i, j)
        return None

    def search_all(self, string):
        n = len(string)
        results = []
        for i in range(n):
            for j in range(i+1, n+1):
                if self._accepts(string[i:j]):
                    results.append((i, j))
        return results

    def finditer(self, string):
        it = []
        for i in range(len(string)):
            for j in range(i + 1, len(string) + 1):
                if self._accepts(string[i:j]):
                    it.append({
                        "span": (i, j),
                        "match": string[i:j]
                    })
        return it

    def split(self, string):
        result = []
        last_end = 0
        while True:
            pos = self.search(string[last_end:])
            if not pos:
                result.append(string[last_end:])
                return result
            i, j = pos
            i += last_end
            j += last_end
            result.append(string[last_end:i])
            last_end = j

    def subn(self, string, replace):
        out = []
        pos = 0
        count = 0
        n = len(string)

        while pos < n:
            found = None
            
            for j in range(pos + 1, n + 1):
                if self._accepts(string[pos:j]):
                    found = (pos, j)
                    break

            if not found:
                out.append(string[pos])
                pos += 1
                continue

            s, e = found
            out.append(replace)
            count += 1
            pos = e

        return ''.join(out), count
