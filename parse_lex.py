import pygments
from pygments.formatters.terminal import TerminalFormatter
from OCLLexer import OCLLexer
import json

lexer = OCLLexer()
formatter = TerminalFormatter()

text = "context Car inv self.stuff->forAll(p1, p2|p1 <> p2 implies p1.ID <> p2.id)"

print(pygments.highlight(text, lexer, formatter))
print(list(pygments.lex(text, lexer)))
exit()
expressions = json.load(open("parsed_expressions_v2.json"))
expressions = json.load(open("DejavuMonoSans/matches.json"))

for expression in expressions:
    num_errors = 0
    print(pygments.highlight(expression['gt_expression'], lexer, formatter))
    print(pygments.highlight(expression['recognized_expression'], lexer, formatter))
    recognized_expression_tokens = list(pygments.lex(expression['recognized_expression'], lexer))
    gt_expression_tokens = list(pygments.lex(expression['gt_expression'], lexer))
    print("Num tokens. GT: %d, Rec: %d" % (len(gt_expression_tokens), len(recognized_expression_tokens)))
    j = 0
    i = 0
    while i < len(gt_expression_tokens) and j < len(recognized_expression_tokens):
        gt_token_type, gt_token = gt_expression_tokens[i]
        rec_token_type, rec_token = recognized_expression_tokens[j]
        if gt_token_type == rec_token_type:
            j += 1
            i += 1
        elif len(recognized_expression_tokens) - j >= len(gt_expression_tokens) - i:
            if gt_token in rec_token:
                print("Missing space?")
            print("Error in tokens. GT: %s, Rec: %s" % (gt_token, rec_token))
            j += 1
            num_errors += 1
        else:
            if gt_token in rec_token:
                print("Missing space?")
            print("Error in tokens. GT: %s, Rec: %s" % (gt_token, rec_token))
            i += 1
            num_errors += 1
    """
    for i, (token_type, token) in enumerate(gt_expression_tokens):
        #print(recognized_expression_tokens[i])
        #print(token_type, token)
        if token_type == recognized_expression_tokens[j][0]:
            j += 1
        else:
            print("Error in tokens. GT: %s, Rec: %s" % (token, recognized_expression_tokens[j][1]))
    """
    print("Identified %d %s" % (num_errors, "error" if num_errors == 1 else "errors"))
    print("\n----------------------\n")