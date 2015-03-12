import re
import string
let = string.letters
dig = string.digits

errors = set([])

def prefix_hack(text):

#      text = re.sub(r"\r", r"", text)         # windows to posix
    text = re.sub(r"\.{3,}\n *", r" ", text)    # join "..."
    text = re.sub(r"[ \t]+", " ", text)         # spaces be reduced
    text = re.sub(r"((^|\n) | \n ?)+", r"\n", text)    # indenting be gone
    text = re.sub(r"(, ?;|; ?,)", ";", text)
    text = re.sub(r"{", r"\\{", text)
    text = re.sub(r"}", r"\\}", text)
    text = re.sub(r":(,|\))", r"::\1", text)

    text = re.sub(r"(^|\n)\%.*", "", text)      # no pure comment

    lines = (text+"\n").split("\n")

    codemode = True
    brace_count = 0
    for i in xrange(len(lines)):

        prefix = postfix = ""
        line = lines[i]
        j = -1

        if line[:8] == "function":
            prefix = prefix + "}\n"*brace_count
            line = line[:8]+"{"+line[8:]
            j += 2*brace_count
            brace_count = 1
            line = re.sub(r"([^=<>~]) ?= ?([^=<>])", r"\1 = \2", line)
        else:
            line = re.sub(r" ?= ?", r"=", line)

        if i == len(lines)-1:
            postfix = "\n}"*brace_count + postfix
            j += 2*brace_count
            brace_count = 0

        blockwords = ["for", "if", "while", "try", "switch"]
        for word in blockwords:
            l = len(word)
            if line[:l] == word and \
                    (len(line) == l or line[l] in " ("):
                if ";" in line:
                    if "; " in line:
                        line = "\n".join(line.split("; "))
                    else:
                        line = "\n".join(line.split(";"))
                line = line[:l]+"{"+line[l:]
                j += l+1
                brace_count += 1

        if "end" in line:

            b = [0]

            def ender(s):
                b[0] += 1
                return "\n"
            line = re.sub(r"(\nend ?;?|; ?end ?)", ender, line)
            postfix = "\n}"*b[0] + postfix
            brace_count -= b[0]

        if line[:3] == "end" and line[3:4] in ("", " ", ";", "%"):
            prefix = prefix + "}"
            line = line[4:]
            brace_count -= 1

        if line[:1] == "[":
            code = re.findall(r"^\[[^\]]*[().{}:][^\]]*\] ?=", line)
            if code:
                errors.add("'%s'\t\tmultiple set assignments" % code[0])
                line = re.sub(r"^\[([^\]]*[().{}:][^\]]*)\] ?=",
                            r"__multi_assign_error_", line)

            line = re.sub(r"^\[ ?([\w\d._]+) ?\] ?=", r"\1 =", line)

        if "[" in line:

            level = 0
            C = ["", ""]
            while True:

                j += 1
                if j >= len(line):
                    if level == 0:
                        break
                    lines[i] = ""
                    while j >= len(line) and i+1 < len(lines):
                        i += 1
                        line += ";"+lines[i]
                    if j >= len(lines):
                        break
                    continue

                linej = line[j]
                if codemode:

                    if linej == "[":
                        level += 1
                        if line[j+1:j+2] == " ":
                            line = line[:j+1]+line[j+2:]

                    elif linej == "%":
                        line = line[:j]
                        continue

                    elif linej == "-":
                        if line[j-1:j] == " ":
                            line = line[:j-1]+line[j:]
                            j -= 1
                        if line[j+1:j+2] == " ":
                            line = line[:j+1]+line[j+2:]

                        if linej == "-" and\
                                line[j-1:j] in dig+let+"_)]":
                            line = line[:j] + "+" + line[j:]

                    elif not level:
                        continue

                    elif linej in r"=,*/\&:^|+":
                        if line[j-1:j] == " ":
                            line = line[:j-1]+line[j:]

                    elif linej == "]":
                        level -= 1
                        if line[j-1:j] == " ":
                            line = line[:j-1]+line[j:]
                            j -= 1

                    elif linej == "," and level > 0:
                        # safe defined matrix
                        if "'" in line:
                            line = fix_quote(lines[i])
                        codemode = False
                        C = [level, "[", "]"]
                        level = 0

                    elif linej == "(":
                        codemode = False
                        C = [1, "(", ")"]

                    elif linej == "'":
                        line_ = line[max(j-2, 0):j+1]
                        line_ = fix_quote(line_)
                        if line_[-1] == '"':
                            line = line[:j] + '"' + line[j+1:]
                            codemode = False
                            C = [1, "'", "'"]

                    elif linej == " ":
                        if line[j+1:j+2] in let+dig+"_(['\"" and\
                                line[j-1:j] in let+dig+"_)]'\"":
                            line = line[:j]+","+line[j+1:]

                    elif linej == "@":
                        name = re.findall(r"@[\w\d_.]+", line[j:])[0]
                        errors.add(
            "'%s'\t\tfunction handle" % name)

                elif linej == C[-1]:
                    if C[0] == 1:
                        codemode = True
                        if linej == "'":
                            line = line[:j] + '"' + line[j+1:]
                        continue
                    else:
                        C[0] -= 1

                elif linej == C[1]:
                    C[0] += 1

                elif linej == "-":
                    if C[1] in "[(":
                        j_ = j-1
                        if line[j_] == " ":
                            j_ -= 1
                        if line[j_] in\
                                string.letters+string.digits+"_)]":
                            line = line[:j] + "+" + line[j:]

                elif C[-1] == "'" and linej in '"':
                    line = line[:j] + line[j+1:]
                elif C[-1] == "'" and linej in '{':
                    line = line[:j] + "(" + line[j+1:]
                elif C[-1] == "'" and linej in '}':
                    line = line[:j] + ")" + line[j+1:]

        elif "'" in line:
            line = fix_quote(line)
            if "-" in line:
                line = re.sub(r"([a-zA-Z0-9_)\]]) ?-", r"\1+-", line)

        elif "-" in line:
            line = re.sub(r"([a-zA-Z0-9_)\]]) ?-", r"\1+-", line)
            if "%" in line:
                line = line.split("%")[0]
            if "@" in line:
                name = re.findall(r"@[\w\d_.]*", line)[0]
                errors.add(
        "'%s'\t\tfunction handle" % name)

        elif "%" in line:
            line = line.split("%")[0]
            if "@" in line:
                name = re.findall(r"@[\w\d_.]+", line)[0]
                errors.add(
        "'%s'\t\tfunction handle" % name)
            line = line.split("%")[0]
        elif "@" in line:
            name = re.findall(r"@[\w\d_.]*", line)[0]
            errors.add(
        "'%s'\t\tfunction handle" % name)

        if "." in line:
            if ".(" in line or ". (" in line:
                code = re.findall(r"[\w\d.]+\. ?\(.*?\)", line)[0]
                errors.add("'%s'\t\tfield assignment" % code)
                line = re.sub(r"\. ?\((.+?)\) ?=", r"!\1!", line)
                line = re.sub(r"([a-zA-Z][a-zA-Z0-9_]*)"+\
                        " ?\. ?\(([a-zA-Z].*)\)(;|\n)",
                        r"\1?\2?\3", line)
            code = re.findall(r"[a-zA-Z][a-zA-Z0-9_]* ?\. ?[a-zA-Z]", line)
            if code:
                errors.add("'%s'\t\tdot-assignment/-retrieval" % code[0])

        lines[i] = prefix + line + postfix

    text = "\n".join(lines)

    # post process
    text = re.sub(r"\bend\b", r"$", text)
    text = re.sub(r"(\d\.?e)\+(-\d)", r"\1\2", text)
    text = re.sub(r"[,;]* ?\n+", r"\n", text)

    # temporary hacks
#      text = re.sub(r" ", "", text)
    text = re.sub(r"\[([ a-zA-Z0-9]+)\]", r"\1", text)
    text = re.sub(r"==", r"%%", text)

    return text, errors


def fix_quote(line):

    prefix = ""
    if line[:5] == "case ":
        prefix, line = line[:5], line[5:]
    codemode = True
    for j in xrange(len(line)):

        if codemode:

            if line[j] == "%":
                return prefix+line[:j]

            if line[j] not in "'":
                continue

            elif j == 0:
                line = '"' + line[1:]
                codemode = False
                continue

            if line[j] == "-":
                j_ = j-1
                if line[j_]:
                    j_ -= 1
                if line[j_] in let+dig+"_)]":
                    line = line[:j] + "+" + line[j:]

            j_ = j-1
            if line[j_] == ".":  # not string
                pass
            elif line[j_] == " ":
                j_ -= 1
            if line[j_] in "=+-*\\/,([|&:^":
                line = line[:j] + '"' + line[j+1:]
                codemode = False
            elif line[j_] == "@":
                errors.add("Function handle '@a'")
            elif line[j_] not in let+dig+"._)]":
                raise SyntaxError("undecifierable\n" +
                                  repr(line[:j_] + "@" + line[j_] +
                                       "@" + line[j_+1:]))

        else:
            if line[j] == "{":
                line = line[:j] + '(' + line[j+1:]
            elif line[j] == "}":
                line = line[:j] + ')' + line[j+1:]
            if line[j] == '"':
                line = line[:j] + line[j+1:]
            elif line[j] == "'":
                line = line[:j] + '"' + line[j+1:]
                codemode = True
    return prefix+line
