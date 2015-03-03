# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .MatlabListener import MatlabListener
else:
    from MatlabListener import MatlabListener
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"D\u01b3\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write(u"\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write(u"\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4")
        buf.write(u"\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write(u"\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t")
        buf.write(u"\35\4\36\t\36\4\37\t\37\3\2\5\2@\n\2\3\2\5\2C\n\2\3\2")
        buf.write(u"\5\2F\n\2\3\2\3\2\3\3\3\3\5\3L\n\3\3\3\3\3\5\3P\n\3\3")
        buf.write(u"\3\7\3S\n\3\f\3\16\3V\13\3\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write(u"\4\3\4\5\4`\n\4\3\5\3\5\7\5d\n\5\f\5\16\5g\13\5\3\5\5")
        buf.write(u"\5j\n\5\3\5\3\5\3\6\3\6\3\6\5\6q\n\6\3\6\3\6\5\6u\n\6")
        buf.write(u"\3\6\3\6\5\6y\n\6\3\7\3\7\3\7\3\7\3\7\5\7\u0080\n\7\3")
        buf.write(u"\7\3\7\5\7\u0084\n\7\3\b\3\b\5\b\u0088\n\b\3\b\3\b\5")
        buf.write(u"\b\u008c\n\b\3\b\3\b\5\b\u0090\n\b\3\t\3\t\3\n\3\n\3")
        buf.write(u"\n\7\n\u0097\n\n\f\n\16\n\u009a\13\n\3\n\5\n\u009d\n")
        buf.write(u"\n\3\n\3\n\3\13\3\13\3\13\3\13\5\13\u00a5\n\13\3\f\3")
        buf.write(u"\f\3\f\5\f\u00aa\n\f\3\r\3\r\5\r\u00ae\n\r\3\r\3\r\3")
        buf.write(u"\r\5\r\u00b3\n\r\3\r\3\r\3\r\5\r\u00b8\n\r\3\r\5\r\u00bb")
        buf.write(u"\n\r\3\r\3\r\3\16\3\16\3\16\3\16\7\16\u00c3\n\16\f\16")
        buf.write(u"\16\16\u00c6\13\16\3\16\3\16\5\16\u00ca\n\16\3\16\3\16")
        buf.write(u"\3\17\3\17\3\17\7\17\u00d1\n\17\f\17\16\17\u00d4\13\17")
        buf.write(u"\3\20\3\20\3\20\3\20\5\20\u00da\n\20\3\20\5\20\u00dd")
        buf.write(u"\n\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3")
        buf.write(u"\21\3\21\3\21\5\21\u00eb\n\21\3\22\3\22\3\22\3\22\3\22")
        buf.write(u"\3\22\5\22\u00f3\n\22\3\22\3\22\5\22\u00f7\n\22\3\22")
        buf.write(u"\5\22\u00fa\n\22\3\22\3\22\3\23\3\23\3\23\6\23\u0101")
        buf.write(u"\n\23\r\23\16\23\u0102\3\23\7\23\u0106\n\23\f\23\16\23")
        buf.write(u"\u0109\13\23\3\23\5\23\u010c\n\23\3\23\3\23\3\24\3\24")
        buf.write(u"\3\24\3\24\3\24\3\25\3\25\3\25\3\26\3\26\3\27\3\27\3")
        buf.write(u"\27\3\27\5\27\u011e\n\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write(u"\6\27\u0126\n\27\r\27\16\27\u0127\3\27\3\27\3\27\3\27")
        buf.write(u"\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write(u"\27\3\27\3\27\3\27\3\27\3\27\5\27\u013e\n\27\3\30\3\30")
        buf.write(u"\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3")
        buf.write(u"\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\5\32\u0155")
        buf.write(u"\n\32\3\32\3\32\3\32\3\32\5\32\u015b\n\32\3\32\3\32\3")
        buf.write(u"\32\3\32\5\32\u0161\n\32\3\32\3\32\5\32\u0165\n\32\3")
        buf.write(u"\32\3\32\3\32\3\32\3\32\7\32\u016c\n\32\f\32\16\32\u016f")
        buf.write(u"\13\32\3\33\3\33\3\34\3\34\3\34\5\34\u0176\n\34\3\34")
        buf.write(u"\3\34\3\34\7\34\u017b\n\34\f\34\16\34\u017e\13\34\3\35")
        buf.write(u"\3\35\3\35\5\35\u0183\n\35\3\35\5\35\u0186\n\35\3\35")
        buf.write(u"\3\35\3\36\3\36\3\36\3\36\3\36\5\36\u018f\n\36\3\36\6")
        buf.write(u"\36\u0192\n\36\r\36\16\36\u0193\3\36\3\36\5\36\u0198")
        buf.write(u"\n\36\3\36\7\36\u019b\n\36\f\36\16\36\u019e\13\36\5\36")
        buf.write(u"\u01a0\n\36\3\36\7\36\u01a3\n\36\f\36\16\36\u01a6\13")
        buf.write(u"\36\3\37\3\37\3\37\3\37\3\37\3\37\7\37\u01ae\n\37\f\37")
        buf.write(u"\16\37\u01b1\13\37\3\37\2\6\62\66:< \2\4\6\b\n\f\16\20")
        buf.write(u"\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<\2\3\4\2")
        buf.write(u"\3\3\7\7\u01e4\2?\3\2\2\2\4I\3\2\2\2\6_\3\2\2\2\ba\3")
        buf.write(u"\2\2\2\nm\3\2\2\2\fz\3\2\2\2\16\u0085\3\2\2\2\20\u0091")
        buf.write(u"\3\2\2\2\22\u0093\3\2\2\2\24\u00a0\3\2\2\2\26\u00a6\3")
        buf.write(u"\2\2\2\30\u00ab\3\2\2\2\32\u00c9\3\2\2\2\34\u00cd\3\2")
        buf.write(u"\2\2\36\u00d5\3\2\2\2 \u00ea\3\2\2\2\"\u00ec\3\2\2\2")
        buf.write(u"$\u00fd\3\2\2\2&\u010f\3\2\2\2(\u0114\3\2\2\2*\u0117")
        buf.write(u"\3\2\2\2,\u013d\3\2\2\2.\u013f\3\2\2\2\60\u0141\3\2\2")
        buf.write(u"\2\62\u0164\3\2\2\2\64\u0170\3\2\2\2\66\u0175\3\2\2\2")
        buf.write(u"8\u017f\3\2\2\2:\u0189\3\2\2\2<\u01a7\3\2\2\2>@\7\3\2")
        buf.write(u"\2?>\3\2\2\2?@\3\2\2\2@B\3\2\2\2AC\5\4\3\2BA\3\2\2\2")
        buf.write(u"BC\3\2\2\2CE\3\2\2\2DF\7\3\2\2ED\3\2\2\2EF\3\2\2\2FG")
        buf.write(u"\3\2\2\2GH\7\2\2\3H\3\3\2\2\2IT\5\6\4\2JL\7\4\2\2KJ\3")
        buf.write(u"\2\2\2KL\3\2\2\2LM\3\2\2\2MP\7\3\2\2NP\7\4\2\2OK\3\2")
        buf.write(u"\2\2ON\3\2\2\2PQ\3\2\2\2QS\5\6\4\2RO\3\2\2\2SV\3\2\2")
        buf.write(u"\2TR\3\2\2\2TU\3\2\2\2U\5\3\2\2\2VT\3\2\2\2W`\5\30\r")
        buf.write(u"\2X`\5,\27\2Y`\5\36\20\2Z`\5\"\22\2[`\5\b\5\2\\`\5\22")
        buf.write(u"\n\2]`\5$\23\2^`\5*\26\2_W\3\2\2\2_X\3\2\2\2_Y\3\2\2")
        buf.write(u"\2_Z\3\2\2\2_[\3\2\2\2_\\\3\2\2\2_]\3\2\2\2_^\3\2\2\2")
        buf.write(u"`\7\3\2\2\2ae\5\n\6\2bd\5\f\7\2cb\3\2\2\2dg\3\2\2\2e")
        buf.write(u"c\3\2\2\2ef\3\2\2\2fi\3\2\2\2ge\3\2\2\2hj\5\16\b\2ih")
        buf.write(u"\3\2\2\2ij\3\2\2\2jk\3\2\2\2kl\7\5\2\2l\t\3\2\2\2mn\7")
        buf.write(u"\6\2\2nx\5\20\t\2oq\7\7\2\2po\3\2\2\2pq\3\2\2\2qr\3\2")
        buf.write(u"\2\2ry\5\6\4\2su\7\7\2\2ts\3\2\2\2tu\3\2\2\2uv\3\2\2")
        buf.write(u"\2vw\7\3\2\2wy\5\4\3\2xp\3\2\2\2xt\3\2\2\2xy\3\2\2\2")
        buf.write(u"y\13\3\2\2\2z{\7\b\2\2{\u0083\5\20\t\2|}\7\7\2\2}\u0084")
        buf.write(u"\5\6\4\2~\u0080\7\7\2\2\177~\3\2\2\2\177\u0080\3\2\2")
        buf.write(u"\2\u0080\u0081\3\2\2\2\u0081\u0082\7\3\2\2\u0082\u0084")
        buf.write(u"\5\4\3\2\u0083|\3\2\2\2\u0083\177\3\2\2\2\u0083\u0084")
        buf.write(u"\3\2\2\2\u0084\r\3\2\2\2\u0085\u008f\7\t\2\2\u0086\u0088")
        buf.write(u"\7\7\2\2\u0087\u0086\3\2\2\2\u0087\u0088\3\2\2\2\u0088")
        buf.write(u"\u0089\3\2\2\2\u0089\u0090\5\6\4\2\u008a\u008c\7\7\2")
        buf.write(u"\2\u008b\u008a\3\2\2\2\u008b\u008c\3\2\2\2\u008c\u008d")
        buf.write(u"\3\2\2\2\u008d\u008e\7\3\2\2\u008e\u0090\5\4\3\2\u008f")
        buf.write(u"\u0087\3\2\2\2\u008f\u008b\3\2\2\2\u008f\u0090\3\2\2")
        buf.write(u"\2\u0090\17\3\2\2\2\u0091\u0092\5\60\31\2\u0092\21\3")
        buf.write(u"\2\2\2\u0093\u0094\7\n\2\2\u0094\u0098\5\60\31\2\u0095")
        buf.write(u"\u0097\5\24\13\2\u0096\u0095\3\2\2\2\u0097\u009a\3\2")
        buf.write(u"\2\2\u0098\u0096\3\2\2\2\u0098\u0099\3\2\2\2\u0099\u009c")
        buf.write(u"\3\2\2\2\u009a\u0098\3\2\2\2\u009b\u009d\5\26\f\2\u009c")
        buf.write(u"\u009b\3\2\2\2\u009c\u009d\3\2\2\2\u009d\u009e\3\2\2")
        buf.write(u"\2\u009e\u009f\7\5\2\2\u009f\23\3\2\2\2\u00a0\u00a1\7")
        buf.write(u"\13\2\2\u00a1\u00a4\5\60\31\2\u00a2\u00a3\7\3\2\2\u00a3")
        buf.write(u"\u00a5\5\4\3\2\u00a4\u00a2\3\2\2\2\u00a4\u00a5\3\2\2")
        buf.write(u"\2\u00a5\25\3\2\2\2\u00a6\u00a9\7\f\2\2\u00a7\u00a8\7")
        buf.write(u"\3\2\2\u00a8\u00aa\5\4\3\2\u00a9\u00a7\3\2\2\2\u00a9")
        buf.write(u"\u00aa\3\2\2\2\u00aa\27\3\2\2\2\u00ab\u00ad\7\r\2\2\u00ac")
        buf.write(u"\u00ae\5\32\16\2\u00ad\u00ac\3\2\2\2\u00ad\u00ae\3\2")
        buf.write(u"\2\2\u00ae\u00af\3\2\2\2\u00af\u00b0\7\"\2\2\u00b0\u00b2")
        buf.write(u"\7\16\2\2\u00b1\u00b3\5\34\17\2\u00b2\u00b1\3\2\2\2\u00b2")
        buf.write(u"\u00b3\3\2\2\2\u00b3\u00b4\3\2\2\2\u00b4\u00b5\7\17\2")
        buf.write(u"\2\u00b5\u00b7\t\2\2\2\u00b6\u00b8\5\4\3\2\u00b7\u00b6")
        buf.write(u"\3\2\2\2\u00b7\u00b8\3\2\2\2\u00b8\u00ba\3\2\2\2\u00b9")
        buf.write(u"\u00bb\7\4\2\2\u00ba\u00b9\3\2\2\2\u00ba\u00bb\3\2\2")
        buf.write(u"\2\u00bb\u00bc\3\2\2\2\u00bc\u00bd\7\5\2\2\u00bd\31\3")
        buf.write(u"\2\2\2\u00be\u00bf\7\20\2\2\u00bf\u00c4\7\"\2\2\u00c0")
        buf.write(u"\u00c1\7\7\2\2\u00c1\u00c3\7\"\2\2\u00c2\u00c0\3\2\2")
        buf.write(u"\2\u00c3\u00c6\3\2\2\2\u00c4\u00c2\3\2\2\2\u00c4\u00c5")
        buf.write(u"\3\2\2\2\u00c5\u00c7\3\2\2\2\u00c6\u00c4\3\2\2\2\u00c7")
        buf.write(u"\u00ca\7\21\2\2\u00c8\u00ca\7\"\2\2\u00c9\u00be\3\2\2")
        buf.write(u"\2\u00c9\u00c8\3\2\2\2\u00ca\u00cb\3\2\2\2\u00cb\u00cc")
        buf.write(u"\7@\2\2\u00cc\33\3\2\2\2\u00cd\u00d2\7\"\2\2\u00ce\u00cf")
        buf.write(u"\7\7\2\2\u00cf\u00d1\7\"\2\2\u00d0\u00ce\3\2\2\2\u00d1")
        buf.write(u"\u00d4\3\2\2\2\u00d2\u00d0\3\2\2\2\u00d2\u00d3\3\2\2")
        buf.write(u"\2\u00d3\35\3\2\2\2\u00d4\u00d2\3\2\2\2\u00d5\u00d6\7")
        buf.write(u"\22\2\2\u00d6\u00dc\5 \21\2\u00d7\u00dd\7\7\2\2\u00d8")
        buf.write(u"\u00da\7\7\2\2\u00d9\u00d8\3\2\2\2\u00d9\u00da\3\2\2")
        buf.write(u"\2\u00da\u00db\3\2\2\2\u00db\u00dd\7\3\2\2\u00dc\u00d7")
        buf.write(u"\3\2\2\2\u00dc\u00d9\3\2\2\2\u00dd\u00de\3\2\2\2\u00de")
        buf.write(u"\u00df\5\4\3\2\u00df\u00e0\7\5\2\2\u00e0\37\3\2\2\2\u00e1")
        buf.write(u"\u00e2\7\16\2\2\u00e2\u00e3\7\"\2\2\u00e3\u00e4\7@\2")
        buf.write(u"\2\u00e4\u00e5\5\60\31\2\u00e5\u00e6\7\17\2\2\u00e6\u00eb")
        buf.write(u"\3\2\2\2\u00e7\u00e8\7\"\2\2\u00e8\u00e9\7@\2\2\u00e9")
        buf.write(u"\u00eb\5\60\31\2\u00ea\u00e1\3\2\2\2\u00ea\u00e7\3\2")
        buf.write(u"\2\2\u00eb!\3\2\2\2\u00ec\u00f2\7\23\2\2\u00ed\u00ee")
        buf.write(u"\7\16\2\2\u00ee\u00ef\5\20\t\2\u00ef\u00f0\7\17\2\2\u00f0")
        buf.write(u"\u00f3\3\2\2\2\u00f1\u00f3\5\20\t\2\u00f2\u00ed\3\2\2")
        buf.write(u"\2\u00f2\u00f1\3\2\2\2\u00f3\u00f4\3\2\2\2\u00f4\u00f6")
        buf.write(u"\t\2\2\2\u00f5\u00f7\5\4\3\2\u00f6\u00f5\3\2\2\2\u00f6")
        buf.write(u"\u00f7\3\2\2\2\u00f7\u00f9\3\2\2\2\u00f8\u00fa\7\4\2")
        buf.write(u"\2\u00f9\u00f8\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa\u00fb")
        buf.write(u"\3\2\2\2\u00fb\u00fc\7\5\2\2\u00fc#\3\2\2\2\u00fd\u00fe")
        buf.write(u"\7\24\2\2\u00fe\u010b\5\4\3\2\u00ff\u0101\5&\24\2\u0100")
        buf.write(u"\u00ff\3\2\2\2\u0101\u0102\3\2\2\2\u0102\u0100\3\2\2")
        buf.write(u"\2\u0102\u0103\3\2\2\2\u0103\u010c\3\2\2\2\u0104\u0106")
        buf.write(u"\5&\24\2\u0105\u0104\3\2\2\2\u0106\u0109\3\2\2\2\u0107")
        buf.write(u"\u0105\3\2\2\2\u0107\u0108\3\2\2\2\u0108\u010a\3\2\2")
        buf.write(u"\2\u0109\u0107\3\2\2\2\u010a\u010c\5(\25\2\u010b\u0100")
        buf.write(u"\3\2\2\2\u010b\u0107\3\2\2\2\u010c\u010d\3\2\2\2\u010d")
        buf.write(u"\u010e\7\5\2\2\u010e%\3\2\2\2\u010f\u0110\7\25\2\2\u0110")
        buf.write(u"\u0111\7\"\2\2\u0111\u0112\7\3\2\2\u0112\u0113\5\4\3")
        buf.write(u"\2\u0113\'\3\2\2\2\u0114\u0115\7\26\2\2\u0115\u0116\5")
        buf.write(u"\4\3\2\u0116)\3\2\2\2\u0117\u0118\5\60\31\2\u0118+\3")
        buf.write(u"\2\2\2\u0119\u011a\7\20\2\2\u011a\u011b\7\"\2\2\u011b")
        buf.write(u"\u011e\7\21\2\2\u011c\u011e\7\"\2\2\u011d\u0119\3\2\2")
        buf.write(u"\2\u011d\u011c\3\2\2\2\u011e\u011f\3\2\2\2\u011f\u0120")
        buf.write(u"\7@\2\2\u0120\u013e\5\60\31\2\u0121\u0122\7\20\2\2\u0122")
        buf.write(u"\u0125\7\"\2\2\u0123\u0124\7\7\2\2\u0124\u0126\7\"\2")
        buf.write(u"\2\u0125\u0123\3\2\2\2\u0126\u0127\3\2\2\2\u0127\u0125")
        buf.write(u"\3\2\2\2\u0127\u0128\3\2\2\2\u0128\u0129\3\2\2\2\u0129")
        buf.write(u"\u012a\7\27\2\2\u012a\u013e\5\60\31\2\u012b\u012c\7\"")
        buf.write(u"\2\2\u012c\u012d\7\16\2\2\u012d\u012e\5.\30\2\u012e\u012f")
        buf.write(u"\7\30\2\2\u012f\u0130\5\60\31\2\u0130\u013e\3\2\2\2\u0131")
        buf.write(u"\u0132\7\"\2\2\u0132\u0133\7\31\2\2\u0133\u0134\5.\30")
        buf.write(u"\2\u0134\u0135\7\32\2\2\u0135\u0136\5\60\31\2\u0136\u013e")
        buf.write(u"\3\2\2\2\u0137\u0138\7\"\2\2\u0138\u0139\7\33\2\2\u0139")
        buf.write(u"\u013a\5.\30\2\u013a\u013b\7\33\2\2\u013b\u013c\5\60")
        buf.write(u"\31\2\u013c\u013e\3\2\2\2\u013d\u011d\3\2\2\2\u013d\u0121")
        buf.write(u"\3\2\2\2\u013d\u012b\3\2\2\2\u013d\u0131\3\2\2\2\u013d")
        buf.write(u"\u0137\3\2\2\2\u013e-\3\2\2\2\u013f\u0140\5\66\34\2\u0140")
        buf.write(u"/\3\2\2\2\u0141\u0142\5\62\32\2\u0142\61\3\2\2\2\u0143")
        buf.write(u"\u0144\b\32\1\2\u0144\u0145\7!\2\2\u0145\u0165\5\62\32")
        buf.write(u"\17\u0146\u0147\7\16\2\2\u0147\u0148\5\60\31\2\u0148")
        buf.write(u"\u0149\7\17\2\2\u0149\u0165\3\2\2\2\u014a\u0165\58\35")
        buf.write(u"\2\u014b\u0165\7%\2\2\u014c\u0165\7#\2\2\u014d\u0165")
        buf.write(u"\7&\2\2\u014e\u0165\7$\2\2\u014f\u0165\7\'\2\2\u0150")
        buf.write(u"\u0165\7(\2\2\u0151\u0152\7\"\2\2\u0152\u0154\7\16\2")
        buf.write(u"\2\u0153\u0155\5\64\33\2\u0154\u0153\3\2\2\2\u0154\u0155")
        buf.write(u"\3\2\2\2\u0155\u0156\3\2\2\2\u0156\u0165\7\17\2\2\u0157")
        buf.write(u"\u0158\7\"\2\2\u0158\u015a\7\34\2\2\u0159\u015b\5\64")
        buf.write(u"\33\2\u015a\u0159\3\2\2\2\u015a\u015b\3\2\2\2\u015b\u015c")
        buf.write(u"\3\2\2\2\u015c\u0165\7\34\2\2\u015d\u015e\7\"\2\2\u015e")
        buf.write(u"\u0160\7\31\2\2\u015f\u0161\5\64\33\2\u0160\u015f\3\2")
        buf.write(u"\2\2\u0160\u0161\3\2\2\2\u0161\u0162\3\2\2\2\u0162\u0165")
        buf.write(u"\7\35\2\2\u0163\u0165\7\"\2\2\u0164\u0143\3\2\2\2\u0164")
        buf.write(u"\u0146\3\2\2\2\u0164\u014a\3\2\2\2\u0164\u014b\3\2\2")
        buf.write(u"\2\u0164\u014c\3\2\2\2\u0164\u014d\3\2\2\2\u0164\u014e")
        buf.write(u"\3\2\2\2\u0164\u014f\3\2\2\2\u0164\u0150\3\2\2\2\u0164")
        buf.write(u"\u0151\3\2\2\2\u0164\u0157\3\2\2\2\u0164\u015d\3\2\2")
        buf.write(u"\2\u0164\u0163\3\2\2\2\u0165\u016d\3\2\2\2\u0166\u0167")
        buf.write(u"\f\16\2\2\u0167\u0168\7 \2\2\u0168\u016c\5\62\32\17\u0169")
        buf.write(u"\u016a\f\20\2\2\u016a\u016c\7)\2\2\u016b\u0166\3\2\2")
        buf.write(u"\2\u016b\u0169\3\2\2\2\u016c\u016f\3\2\2\2\u016d\u016b")
        buf.write(u"\3\2\2\2\u016d\u016e\3\2\2\2\u016e\63\3\2\2\2\u016f\u016d")
        buf.write(u"\3\2\2\2\u0170\u0171\5\66\34\2\u0171\65\3\2\2\2\u0172")
        buf.write(u"\u0173\b\34\1\2\u0173\u0176\7\36\2\2\u0174\u0176\5\60")
        buf.write(u"\31\2\u0175\u0172\3\2\2\2\u0175\u0174\3\2\2\2\u0176\u017c")
        buf.write(u"\3\2\2\2\u0177\u0178\f\5\2\2\u0178\u0179\7\7\2\2\u0179")
        buf.write(u"\u017b\5\66\34\6\u017a\u0177\3\2\2\2\u017b\u017e\3\2")
        buf.write(u"\2\2\u017c\u017a\3\2\2\2\u017c\u017d\3\2\2\2\u017d\67")
        buf.write(u"\3\2\2\2\u017e\u017c\3\2\2\2\u017f\u0180\7\20\2\2\u0180")
        buf.write(u"\u0182\5:\36\2\u0181\u0183\7\7\2\2\u0182\u0181\3\2\2")
        buf.write(u"\2\u0182\u0183\3\2\2\2\u0183\u0185\3\2\2\2\u0184\u0186")
        buf.write(u"\7\4\2\2\u0185\u0184\3\2\2\2\u0185\u0186\3\2\2\2\u0186")
        buf.write(u"\u0187\3\2\2\2\u0187\u0188\7\21\2\2\u01889\3\2\2\2\u0189")
        buf.write(u"\u018a\b\36\1\2\u018a\u018b\5<\37\2\u018b\u01a4\3\2\2")
        buf.write(u"\2\u018c\u019f\f\4\2\2\u018d\u018f\7\37\2\2\u018e\u018d")
        buf.write(u"\3\2\2\2\u018e\u018f\3\2\2\2\u018f\u0190\3\2\2\2\u0190")
        buf.write(u"\u0192\7\3\2\2\u0191\u018e\3\2\2\2\u0192\u0193\3\2\2")
        buf.write(u"\2\u0193\u0191\3\2\2\2\u0193\u0194\3\2\2\2\u0194\u01a0")
        buf.write(u"\3\2\2\2\u0195\u019c\7\4\2\2\u0196\u0198\7\37\2\2\u0197")
        buf.write(u"\u0196\3\2\2\2\u0197\u0198\3\2\2\2\u0198\u0199\3\2\2")
        buf.write(u"\2\u0199\u019b\7\3\2\2\u019a\u0197\3\2\2\2\u019b\u019e")
        buf.write(u"\3\2\2\2\u019c\u019a\3\2\2\2\u019c\u019d\3\2\2\2\u019d")
        buf.write(u"\u01a0\3\2\2\2\u019e\u019c\3\2\2\2\u019f\u0191\3\2\2")
        buf.write(u"\2\u019f\u0195\3\2\2\2\u01a0\u01a1\3\2\2\2\u01a1\u01a3")
        buf.write(u"\5:\36\5\u01a2\u018c\3\2\2\2\u01a3\u01a6\3\2\2\2\u01a4")
        buf.write(u"\u01a2\3\2\2\2\u01a4\u01a5\3\2\2\2\u01a5;\3\2\2\2\u01a6")
        buf.write(u"\u01a4\3\2\2\2\u01a7\u01a8\b\37\1\2\u01a8\u01a9\5\60")
        buf.write(u"\31\2\u01a9\u01af\3\2\2\2\u01aa\u01ab\f\4\2\2\u01ab\u01ac")
        buf.write(u"\7\7\2\2\u01ac\u01ae\5<\37\5\u01ad\u01aa\3\2\2\2\u01ae")
        buf.write(u"\u01b1\3\2\2\2\u01af\u01ad\3\2\2\2\u01af\u01b0\3\2\2")
        buf.write(u"\2\u01b0=\3\2\2\2\u01b1\u01af\3\2\2\2;?BEKOT_eiptx\177")
        buf.write(u"\u0083\u0087\u008b\u008f\u0098\u009c\u00a4\u00a9\u00ad")
        buf.write(u"\u00b2\u00b7\u00ba\u00c4\u00c9\u00d2\u00d9\u00dc\u00ea")
        buf.write(u"\u00f2\u00f6\u00f9\u0102\u0107\u010b\u011d\u0127\u013d")
        buf.write(u"\u0154\u015a\u0160\u0164\u016b\u016d\u0175\u017c\u0182")
        buf.write(u"\u0185\u018e\u0193\u0197\u019c\u019f\u01a4\u01af")
        return buf.getvalue()


class MatlabParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'\n'", u"';'", u"'\n}'", u"'if{'", 
                     u"','", u"'\nelseif'", u"'\nelse'", u"'switch{'", u"'\ncase'", 
                     u"'\notherwise'", u"'function{'", u"'('", u"')'", u"'['", 
                     u"']'", u"'for{'", u"'while{'", u"'try{\n'", u"'\ncatch'", 
                     u"'\ncatch\n'", u"']='", u"')='", u"'\\{'", u"'\\}='", 
                     u"'!'", u"'?'", u"'\\}'", u"'::'", u"'\r'", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"'$'", u"<INVALID>", 
                     u"'||'", u"'&&'", u"'|'", u"'&'", u"'%%'", u"'<='", 
                     u"'>='", u"'<>'", u"'<'", u"'>'", u"':'", u"'+'", u"'-'", 
                     u"'/'", u"'\\'", u"'*'", u"'./'", u"'.\\'", u"'.*'", 
                     u"'^'", u"'.^'", u"'~'", u"'='", u"'''", u"'.''" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"OPR", u"PRE", u"ID", 
                      u"INT", u"FLOAT", u"IINT", u"IFLOAT", u"STRING", u"END", 
                      u"POST", u"LOG_OR", u"LOG_AND", u"BIN_OR", u"BIN_AND", 
                      u"EQEQ", u"LSTE", u"GRTE", u"NEQ", u"LST", u"GRT", 
                      u"COLON", u"PLUS", u"MINUS", u"LEFTDIV", u"RIGHTDIV", 
                      u"TIMES", u"EL_LEFTDIV", u"EL_RIGHTDIV", u"EL_TIMES", 
                      u"EXP", u"EL_EXP", u"NEG", u"EQ", u"CCT", u"EL_CCT", 
                      u"WS", u"THREEDOTS" ]

    RULE_program = 0
    RULE_codeblock = 1
    RULE_codeline = 2
    RULE_branch = 3
    RULE_branch_if = 4
    RULE_branch_elif = 5
    RULE_branch_else = 6
    RULE_condition = 7
    RULE_switch_ = 8
    RULE_switch_case = 9
    RULE_switch_otherwise = 10
    RULE_function = 11
    RULE_function_returns = 12
    RULE_function_params = 13
    RULE_loop = 14
    RULE_loop_range = 15
    RULE_wloop = 16
    RULE_try_ = 17
    RULE_catchid = 18
    RULE_catch_ = 19
    RULE_statement = 20
    RULE_assignment = 21
    RULE_sets = 22
    RULE_expr = 23
    RULE_expr_ = 24
    RULE_llist = 25
    RULE_llist_ = 26
    RULE_matrix = 27
    RULE_matrix_ = 28
    RULE_vector = 29

    ruleNames =  [ u"program", u"codeblock", u"codeline", u"branch", u"branch_if", 
                   u"branch_elif", u"branch_else", u"condition", u"switch_", 
                   u"switch_case", u"switch_otherwise", u"function", u"function_returns", 
                   u"function_params", u"loop", u"loop_range", u"wloop", 
                   u"try_", u"catchid", u"catch_", u"statement", u"assignment", 
                   u"sets", u"expr", u"expr_", u"llist", u"llist_", u"matrix", 
                   u"matrix_", u"vector" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    OPR=30
    PRE=31
    ID=32
    INT=33
    FLOAT=34
    IINT=35
    IFLOAT=36
    STRING=37
    END=38
    POST=39
    LOG_OR=40
    LOG_AND=41
    BIN_OR=42
    BIN_AND=43
    EQEQ=44
    LSTE=45
    GRTE=46
    NEQ=47
    LST=48
    GRT=49
    COLON=50
    PLUS=51
    MINUS=52
    LEFTDIV=53
    RIGHTDIV=54
    TIMES=55
    EL_LEFTDIV=56
    EL_RIGHTDIV=57
    EL_TIMES=58
    EXP=59
    EL_EXP=60
    NEG=61
    EQ=62
    CCT=63
    EL_CCT=64
    WS=65
    THREEDOTS=66

    def __init__(self, input):
        super(MatlabParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MatlabParser.EOF, 0)

        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_program

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitProgram(self)




    def program(self):

        localctx = MatlabParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 60
                self.match(MatlabParser.T__0)


            self.state = 64
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__3) | (1 << MatlabParser.T__7) | (1 << MatlabParser.T__10) | (1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__15) | (1 << MatlabParser.T__16) | (1 << MatlabParser.T__17) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                self.state = 63
                self.codeblock()


            self.state = 67
            _la = self._input.LA(1)
            if _la==MatlabParser.T__0:
                self.state = 66
                self.match(MatlabParser.T__0)


            self.state = 69
            self.match(MatlabParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CodeblockContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.CodeblockContext, self).__init__(parent, invokingState)
            self.parser = parser

        def codeline(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.CodelineContext)
            else:
                return self.getTypedRuleContext(MatlabParser.CodelineContext,i)


        def getRuleIndex(self):
            return MatlabParser.RULE_codeblock

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterCodeblock(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitCodeblock(self)




    def codeblock(self):

        localctx = MatlabParser.CodeblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_codeblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.codeline()
            self.state = 82
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 77
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        self.state = 73
                        _la = self._input.LA(1)
                        if _la==MatlabParser.T__1:
                            self.state = 72
                            self.match(MatlabParser.T__1)


                        self.state = 75
                        self.match(MatlabParser.T__0)
                        pass

                    elif la_ == 2:
                        self.state = 76
                        self.match(MatlabParser.T__1)
                        pass


                    self.state = 79
                    self.codeline() 
                self.state = 84
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CodelineContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.CodelineContext, self).__init__(parent, invokingState)
            self.parser = parser

        def function(self):
            return self.getTypedRuleContext(MatlabParser.FunctionContext,0)


        def assignment(self):
            return self.getTypedRuleContext(MatlabParser.AssignmentContext,0)


        def loop(self):
            return self.getTypedRuleContext(MatlabParser.LoopContext,0)


        def wloop(self):
            return self.getTypedRuleContext(MatlabParser.WloopContext,0)


        def branch(self):
            return self.getTypedRuleContext(MatlabParser.BranchContext,0)


        def switch_(self):
            return self.getTypedRuleContext(MatlabParser.Switch_Context,0)


        def try_(self):
            return self.getTypedRuleContext(MatlabParser.Try_Context,0)


        def statement(self):
            return self.getTypedRuleContext(MatlabParser.StatementContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_codeline

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterCodeline(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitCodeline(self)




    def codeline(self):

        localctx = MatlabParser.CodelineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_codeline)
        try:
            self.state = 93
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 85
                self.function()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 86
                self.assignment()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 87
                self.loop()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 88
                self.wloop()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 89
                self.branch()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 90
                self.switch_()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 91
                self.try_()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 92
                self.statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BranchContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.BranchContext, self).__init__(parent, invokingState)
            self.parser = parser

        def branch_if(self):
            return self.getTypedRuleContext(MatlabParser.Branch_ifContext,0)


        def branch_elif(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.Branch_elifContext)
            else:
                return self.getTypedRuleContext(MatlabParser.Branch_elifContext,i)


        def branch_else(self):
            return self.getTypedRuleContext(MatlabParser.Branch_elseContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_branch

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterBranch(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitBranch(self)




    def branch(self):

        localctx = MatlabParser.BranchContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_branch)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.branch_if()
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==MatlabParser.T__5:
                self.state = 96
                self.branch_elif()
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 103
            _la = self._input.LA(1)
            if _la==MatlabParser.T__6:
                self.state = 102
                self.branch_else()


            self.state = 105
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Branch_ifContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Branch_ifContext, self).__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(MatlabParser.ConditionContext,0)


        def codeline(self):
            return self.getTypedRuleContext(MatlabParser.CodelineContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_branch_if

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterBranch_if(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitBranch_if(self)




    def branch_if(self):

        localctx = MatlabParser.Branch_ifContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_branch_if)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(MatlabParser.T__3)
            self.state = 108
            self.condition()
            self.state = 118
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 110
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 109
                    self.match(MatlabParser.T__4)


                self.state = 112
                self.codeline()

            elif la_ == 2:
                self.state = 114
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 113
                    self.match(MatlabParser.T__4)


                self.state = 116
                self.match(MatlabParser.T__0)
                self.state = 117
                self.codeblock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Branch_elifContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Branch_elifContext, self).__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(MatlabParser.ConditionContext,0)


        def codeline(self):
            return self.getTypedRuleContext(MatlabParser.CodelineContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_branch_elif

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterBranch_elif(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitBranch_elif(self)




    def branch_elif(self):

        localctx = MatlabParser.Branch_elifContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_branch_elif)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(MatlabParser.T__5)
            self.state = 121
            self.condition()
            self.state = 129
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 122
                self.match(MatlabParser.T__4)
                self.state = 123
                self.codeline()

            elif la_ == 2:
                self.state = 125
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 124
                    self.match(MatlabParser.T__4)


                self.state = 127
                self.match(MatlabParser.T__0)
                self.state = 128
                self.codeblock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Branch_elseContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Branch_elseContext, self).__init__(parent, invokingState)
            self.parser = parser

        def codeline(self):
            return self.getTypedRuleContext(MatlabParser.CodelineContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_branch_else

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterBranch_else(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitBranch_else(self)




    def branch_else(self):

        localctx = MatlabParser.Branch_elseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_branch_else)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(MatlabParser.T__6)
            self.state = 141
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.state = 133
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 132
                    self.match(MatlabParser.T__4)


                self.state = 135
                self.codeline()

            elif la_ == 2:
                self.state = 137
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 136
                    self.match(MatlabParser.T__4)


                self.state = 139
                self.match(MatlabParser.T__0)
                self.state = 140
                self.codeblock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConditionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.ConditionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_condition

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterCondition(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitCondition(self)




    def condition(self):

        localctx = MatlabParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Switch_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Switch_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def switch_case(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.Switch_caseContext)
            else:
                return self.getTypedRuleContext(MatlabParser.Switch_caseContext,i)


        def switch_otherwise(self):
            return self.getTypedRuleContext(MatlabParser.Switch_otherwiseContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_switch_

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSwitch_(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSwitch_(self)




    def switch_(self):

        localctx = MatlabParser.Switch_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_switch_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145
            self.match(MatlabParser.T__7)
            self.state = 146
            self.expr()
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==MatlabParser.T__8:
                self.state = 147
                self.switch_case()
                self.state = 152
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 154
            _la = self._input.LA(1)
            if _la==MatlabParser.T__9:
                self.state = 153
                self.switch_otherwise()


            self.state = 156
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Switch_caseContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Switch_caseContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_switch_case

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSwitch_case(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSwitch_case(self)




    def switch_case(self):

        localctx = MatlabParser.Switch_caseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_switch_case)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.match(MatlabParser.T__8)
            self.state = 159
            self.expr()
            self.state = 162
            _la = self._input.LA(1)
            if _la==MatlabParser.T__0:
                self.state = 160
                self.match(MatlabParser.T__0)
                self.state = 161
                self.codeblock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Switch_otherwiseContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Switch_otherwiseContext, self).__init__(parent, invokingState)
            self.parser = parser

        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_switch_otherwise

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSwitch_otherwise(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSwitch_otherwise(self)




    def switch_otherwise(self):

        localctx = MatlabParser.Switch_otherwiseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_switch_otherwise)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(MatlabParser.T__9)
            self.state = 167
            _la = self._input.LA(1)
            if _la==MatlabParser.T__0:
                self.state = 165
                self.match(MatlabParser.T__0)
                self.state = 166
                self.codeblock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FunctionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.FunctionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)

        def function_returns(self):
            return self.getTypedRuleContext(MatlabParser.Function_returnsContext,0)


        def function_params(self):
            return self.getTypedRuleContext(MatlabParser.Function_paramsContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_function

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterFunction(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitFunction(self)




    def function(self):

        localctx = MatlabParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.match(MatlabParser.T__10)
            self.state = 171
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 170
                self.function_returns()


            self.state = 173
            self.match(MatlabParser.ID)
            self.state = 174
            self.match(MatlabParser.T__11)
            self.state = 176
            _la = self._input.LA(1)
            if _la==MatlabParser.ID:
                self.state = 175
                self.function_params()


            self.state = 178
            self.match(MatlabParser.T__12)
            self.state = 179
            _la = self._input.LA(1)
            if not(_la==MatlabParser.T__0 or _la==MatlabParser.T__4):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
            self.state = 181
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__3) | (1 << MatlabParser.T__7) | (1 << MatlabParser.T__10) | (1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__15) | (1 << MatlabParser.T__16) | (1 << MatlabParser.T__17) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                self.state = 180
                self.codeblock()


            self.state = 184
            _la = self._input.LA(1)
            if _la==MatlabParser.T__1:
                self.state = 183
                self.match(MatlabParser.T__1)


            self.state = 186
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_returnsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Function_returnsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(MatlabParser.ID)
            else:
                return self.getToken(MatlabParser.ID, i)

        def getRuleIndex(self):
            return MatlabParser.RULE_function_returns

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterFunction_returns(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitFunction_returns(self)




    def function_returns(self):

        localctx = MatlabParser.Function_returnsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_function_returns)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            token = self._input.LA(1)
            if token in [MatlabParser.T__13]:
                self.state = 188
                self.match(MatlabParser.T__13)
                self.state = 189
                self.match(MatlabParser.ID)
                self.state = 194
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==MatlabParser.T__4:
                    self.state = 190
                    self.match(MatlabParser.T__4)
                    self.state = 191
                    self.match(MatlabParser.ID)
                    self.state = 196
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 197
                self.match(MatlabParser.T__14)

            elif token in [MatlabParser.ID]:
                self.state = 198
                self.match(MatlabParser.ID)

            else:
                raise NoViableAltException(self)

            self.state = 201
            self.match(MatlabParser.EQ)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_paramsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Function_paramsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(MatlabParser.ID)
            else:
                return self.getToken(MatlabParser.ID, i)

        def getRuleIndex(self):
            return MatlabParser.RULE_function_params

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterFunction_params(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitFunction_params(self)




    def function_params(self):

        localctx = MatlabParser.Function_paramsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_function_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.match(MatlabParser.ID)
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==MatlabParser.T__4:
                self.state = 204
                self.match(MatlabParser.T__4)
                self.state = 205
                self.match(MatlabParser.ID)
                self.state = 210
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LoopContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.LoopContext, self).__init__(parent, invokingState)
            self.parser = parser

        def loop_range(self):
            return self.getTypedRuleContext(MatlabParser.Loop_rangeContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_loop

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterLoop(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitLoop(self)




    def loop(self):

        localctx = MatlabParser.LoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_loop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self.match(MatlabParser.T__15)
            self.state = 212
            self.loop_range()
            self.state = 218
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.state = 213
                self.match(MatlabParser.T__4)
                pass

            elif la_ == 2:
                self.state = 215
                _la = self._input.LA(1)
                if _la==MatlabParser.T__4:
                    self.state = 214
                    self.match(MatlabParser.T__4)


                self.state = 217
                self.match(MatlabParser.T__0)
                pass


            self.state = 220
            self.codeblock()
            self.state = 221
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Loop_rangeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Loop_rangeContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)

        def EQ(self):
            return self.getToken(MatlabParser.EQ, 0)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_loop_range

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterLoop_range(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitLoop_range(self)




    def loop_range(self):

        localctx = MatlabParser.Loop_rangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_loop_range)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            token = self._input.LA(1)
            if token in [MatlabParser.T__11]:
                self.state = 223
                self.match(MatlabParser.T__11)
                self.state = 224
                self.match(MatlabParser.ID)
                self.state = 225
                self.match(MatlabParser.EQ)
                self.state = 226
                self.expr()
                self.state = 227
                self.match(MatlabParser.T__12)

            elif token in [MatlabParser.ID]:
                self.state = 229
                self.match(MatlabParser.ID)
                self.state = 230
                self.match(MatlabParser.EQ)
                self.state = 231
                self.expr()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class WloopContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.WloopContext, self).__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(MatlabParser.ConditionContext,0)


        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_wloop

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterWloop(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitWloop(self)




    def wloop(self):

        localctx = MatlabParser.WloopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_wloop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234
            self.match(MatlabParser.T__16)
            self.state = 240
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.state = 235
                self.match(MatlabParser.T__11)
                self.state = 236
                self.condition()
                self.state = 237
                self.match(MatlabParser.T__12)
                pass

            elif la_ == 2:
                self.state = 239
                self.condition()
                pass


            self.state = 242
            _la = self._input.LA(1)
            if not(_la==MatlabParser.T__0 or _la==MatlabParser.T__4):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
            self.state = 244
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__3) | (1 << MatlabParser.T__7) | (1 << MatlabParser.T__10) | (1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__15) | (1 << MatlabParser.T__16) | (1 << MatlabParser.T__17) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                self.state = 243
                self.codeblock()


            self.state = 247
            _la = self._input.LA(1)
            if _la==MatlabParser.T__1:
                self.state = 246
                self.match(MatlabParser.T__1)


            self.state = 249
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Try_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Try_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def catch_(self):
            return self.getTypedRuleContext(MatlabParser.Catch_Context,0)


        def catchid(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.CatchidContext)
            else:
                return self.getTypedRuleContext(MatlabParser.CatchidContext,i)


        def getRuleIndex(self):
            return MatlabParser.RULE_try_

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterTry_(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitTry_(self)




    def try_(self):

        localctx = MatlabParser.Try_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_try_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(MatlabParser.T__17)
            self.state = 252
            self.codeblock()
            self.state = 265
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.state = 254 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 253
                    self.catchid()
                    self.state = 256 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==MatlabParser.T__18):
                        break

                pass

            elif la_ == 2:
                self.state = 261
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==MatlabParser.T__18:
                    self.state = 258
                    self.catchid()
                    self.state = 263
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 264
                self.catch_()
                pass


            self.state = 267
            self.match(MatlabParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CatchidContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.CatchidContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)

        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_catchid

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterCatchid(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitCatchid(self)




    def catchid(self):

        localctx = MatlabParser.CatchidContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_catchid)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self.match(MatlabParser.T__18)
            self.state = 270
            self.match(MatlabParser.ID)
            self.state = 271
            self.match(MatlabParser.T__0)
            self.state = 272
            self.codeblock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Catch_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Catch_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def codeblock(self):
            return self.getTypedRuleContext(MatlabParser.CodeblockContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_catch_

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterCatch_(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitCatch_(self)




    def catch_(self):

        localctx = MatlabParser.Catch_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_catch_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            self.match(MatlabParser.T__19)
            self.state = 275
            self.codeblock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.StatementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_statement

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterStatement(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitStatement(self)




    def statement(self):

        localctx = MatlabParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 277
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AssignmentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.AssignmentContext, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MatlabParser.RULE_assignment

     
        def copyFrom(self, ctx):
            super(MatlabParser.AssignmentContext, self).copyFrom(ctx)



    class Set1Context(AssignmentContext):

        def __init__(self, parser, ctx): # actually a MatlabParser.AssignmentContext)
            super(MatlabParser.Set1Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def sets(self):
            return self.getTypedRuleContext(MatlabParser.SetsContext,0)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSet1(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSet1(self)


    class AssignContext(AssignmentContext):

        def __init__(self, parser, ctx): # actually a MatlabParser.AssignmentContext)
            super(MatlabParser.AssignContext, self).__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterAssign(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitAssign(self)


    class AssignsContext(AssignmentContext):

        def __init__(self, parser, ctx): # actually a MatlabParser.AssignmentContext)
            super(MatlabParser.AssignsContext, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self, i=None):
            if i is None:
                return self.getTokens(MatlabParser.ID)
            else:
                return self.getToken(MatlabParser.ID, i)
        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterAssigns(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitAssigns(self)


    class Set2Context(AssignmentContext):

        def __init__(self, parser, ctx): # actually a MatlabParser.AssignmentContext)
            super(MatlabParser.Set2Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def sets(self):
            return self.getTypedRuleContext(MatlabParser.SetsContext,0)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSet2(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSet2(self)


    class Set3Context(AssignmentContext):

        def __init__(self, parser, ctx): # actually a MatlabParser.AssignmentContext)
            super(MatlabParser.Set3Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def sets(self):
            return self.getTypedRuleContext(MatlabParser.SetsContext,0)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSet3(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSet3(self)



    def assignment(self):

        localctx = MatlabParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.state = 315
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                localctx = MatlabParser.AssignContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 283
                token = self._input.LA(1)
                if token in [MatlabParser.T__13]:
                    self.state = 279
                    self.match(MatlabParser.T__13)
                    self.state = 280
                    self.match(MatlabParser.ID)
                    self.state = 281
                    self.match(MatlabParser.T__14)

                elif token in [MatlabParser.ID]:
                    self.state = 282
                    self.match(MatlabParser.ID)

                else:
                    raise NoViableAltException(self)

                self.state = 285
                self.match(MatlabParser.EQ)
                self.state = 286
                self.expr()
                pass

            elif la_ == 2:
                localctx = MatlabParser.AssignsContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 287
                self.match(MatlabParser.T__13)
                self.state = 288
                self.match(MatlabParser.ID)
                self.state = 291 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 289
                    self.match(MatlabParser.T__4)
                    self.state = 290
                    self.match(MatlabParser.ID)
                    self.state = 293 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==MatlabParser.T__4):
                        break

                self.state = 295
                self.match(MatlabParser.T__20)
                self.state = 296
                self.expr()
                pass

            elif la_ == 3:
                localctx = MatlabParser.Set1Context(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 297
                self.match(MatlabParser.ID)
                self.state = 298
                self.match(MatlabParser.T__11)
                self.state = 299
                self.sets()
                self.state = 300
                self.match(MatlabParser.T__21)
                self.state = 301
                self.expr()
                pass

            elif la_ == 4:
                localctx = MatlabParser.Set2Context(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 303
                self.match(MatlabParser.ID)
                self.state = 304
                self.match(MatlabParser.T__22)
                self.state = 305
                self.sets()
                self.state = 306
                self.match(MatlabParser.T__23)
                self.state = 307
                self.expr()
                pass

            elif la_ == 5:
                localctx = MatlabParser.Set3Context(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 309
                self.match(MatlabParser.ID)
                self.state = 310
                self.match(MatlabParser.T__24)
                self.state = 311
                self.sets()
                self.state = 312
                self.match(MatlabParser.T__24)
                self.state = 313
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SetsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.SetsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def llist_(self):
            return self.getTypedRuleContext(MatlabParser.Llist_Context,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_sets

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterSets(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitSets(self)




    def sets(self):

        localctx = MatlabParser.SetsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_sets)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 317
            self.llist_(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.ExprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr_(self):
            return self.getTypedRuleContext(MatlabParser.Expr_Context,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_expr

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterExpr(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitExpr(self)




    def expr(self):

        localctx = MatlabParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 319
            self.expr_(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Expr_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Expr_Context, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MatlabParser.RULE_expr_

     
        def copyFrom(self, ctx):
            super(MatlabParser.Expr_Context, self).copyFrom(ctx)


    class IfloatContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.IfloatContext, self).__init__(parser)
            self.copyFrom(ctx)

        def IFLOAT(self):
            return self.getToken(MatlabParser.IFLOAT, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterIfloat(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitIfloat(self)


    class FloatContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.FloatContext, self).__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(MatlabParser.FLOAT, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterFloat(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitFloat(self)


    class EndContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.EndContext, self).__init__(parser)
            self.copyFrom(ctx)

        def END(self):
            return self.getToken(MatlabParser.END, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterEnd(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitEnd(self)


    class Get3Context(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.Get3Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def llist(self):
            return self.getTypedRuleContext(MatlabParser.LlistContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterGet3(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitGet3(self)


    class Get2Context(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.Get2Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def llist(self):
            return self.getTypedRuleContext(MatlabParser.LlistContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterGet2(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitGet2(self)


    class Get1Context(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.Get1Context, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)
        def llist(self):
            return self.getTypedRuleContext(MatlabParser.LlistContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterGet1(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitGet1(self)


    class InfixContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.InfixContext, self).__init__(parser)
            self.copyFrom(ctx)

        def expr_(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.Expr_Context)
            else:
                return self.getTypedRuleContext(MatlabParser.Expr_Context,i)

        def OPR(self):
            return self.getToken(MatlabParser.OPR, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterInfix(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitInfix(self)


    class PrefixContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.PrefixContext, self).__init__(parser)
            self.copyFrom(ctx)

        def PRE(self):
            return self.getToken(MatlabParser.PRE, 0)
        def expr_(self):
            return self.getTypedRuleContext(MatlabParser.Expr_Context,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterPrefix(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitPrefix(self)


    class ParenContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.ParenContext, self).__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterParen(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitParen(self)


    class IintContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.IintContext, self).__init__(parser)
            self.copyFrom(ctx)

        def IINT(self):
            return self.getToken(MatlabParser.IINT, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterIint(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitIint(self)


    class StringContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.StringContext, self).__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(MatlabParser.STRING, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterString(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitString(self)


    class IntContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.IntContext, self).__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(MatlabParser.INT, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterInt(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitInt(self)


    class VarContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.VarContext, self).__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MatlabParser.ID, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterVar(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitVar(self)


    class MatriContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.MatriContext, self).__init__(parser)
            self.copyFrom(ctx)

        def matrix(self):
            return self.getTypedRuleContext(MatlabParser.MatrixContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterMatri(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitMatri(self)


    class PostfixContext(Expr_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Expr_Context)
            super(MatlabParser.PostfixContext, self).__init__(parser)
            self.copyFrom(ctx)

        def expr_(self):
            return self.getTypedRuleContext(MatlabParser.Expr_Context,0)

        def POST(self):
            return self.getToken(MatlabParser.POST, 0)

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterPostfix(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitPostfix(self)



    def expr_(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MatlabParser.Expr_Context(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 48
        self.enterRecursionRule(localctx, 48, self.RULE_expr_, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 354
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                localctx = MatlabParser.PrefixContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 322
                self.match(MatlabParser.PRE)
                self.state = 323
                self.expr_(13)
                pass

            elif la_ == 2:
                localctx = MatlabParser.ParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 324
                self.match(MatlabParser.T__11)
                self.state = 325
                self.expr()
                self.state = 326
                self.match(MatlabParser.T__12)
                pass

            elif la_ == 3:
                localctx = MatlabParser.MatriContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 328
                self.matrix()
                pass

            elif la_ == 4:
                localctx = MatlabParser.IintContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 329
                self.match(MatlabParser.IINT)
                pass

            elif la_ == 5:
                localctx = MatlabParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 330
                self.match(MatlabParser.INT)
                pass

            elif la_ == 6:
                localctx = MatlabParser.IfloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 331
                self.match(MatlabParser.IFLOAT)
                pass

            elif la_ == 7:
                localctx = MatlabParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 332
                self.match(MatlabParser.FLOAT)
                pass

            elif la_ == 8:
                localctx = MatlabParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 333
                self.match(MatlabParser.STRING)
                pass

            elif la_ == 9:
                localctx = MatlabParser.EndContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 334
                self.match(MatlabParser.END)
                pass

            elif la_ == 10:
                localctx = MatlabParser.Get1Context(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 335
                self.match(MatlabParser.ID)
                self.state = 336
                self.match(MatlabParser.T__11)
                self.state = 338
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__27) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                    self.state = 337
                    self.llist()


                self.state = 340
                self.match(MatlabParser.T__12)
                pass

            elif la_ == 11:
                localctx = MatlabParser.Get2Context(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 341
                self.match(MatlabParser.ID)
                self.state = 342
                self.match(MatlabParser.T__25)
                self.state = 344
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__27) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                    self.state = 343
                    self.llist()


                self.state = 346
                self.match(MatlabParser.T__25)
                pass

            elif la_ == 12:
                localctx = MatlabParser.Get3Context(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 347
                self.match(MatlabParser.ID)
                self.state = 348
                self.match(MatlabParser.T__22)
                self.state = 350
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MatlabParser.T__11) | (1 << MatlabParser.T__13) | (1 << MatlabParser.T__27) | (1 << MatlabParser.PRE) | (1 << MatlabParser.ID) | (1 << MatlabParser.INT) | (1 << MatlabParser.FLOAT) | (1 << MatlabParser.IINT) | (1 << MatlabParser.IFLOAT) | (1 << MatlabParser.STRING) | (1 << MatlabParser.END))) != 0):
                    self.state = 349
                    self.llist()


                self.state = 352
                self.match(MatlabParser.T__26)
                pass

            elif la_ == 13:
                localctx = MatlabParser.VarContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 353
                self.match(MatlabParser.ID)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 363
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,45,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 361
                    la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
                    if la_ == 1:
                        localctx = MatlabParser.InfixContext(self, MatlabParser.Expr_Context(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_)
                        self.state = 356
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 357
                        self.match(MatlabParser.OPR)
                        self.state = 358
                        self.expr_(13)
                        pass

                    elif la_ == 2:
                        localctx = MatlabParser.PostfixContext(self, MatlabParser.Expr_Context(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr_)
                        self.state = 359
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 360
                        self.match(MatlabParser.POST)
                        pass

             
                self.state = 365
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,45,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class LlistContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.LlistContext, self).__init__(parent, invokingState)
            self.parser = parser

        def llist_(self):
            return self.getTypedRuleContext(MatlabParser.Llist_Context,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_llist

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterLlist(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitLlist(self)




    def llist(self):

        localctx = MatlabParser.LlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_llist)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 366
            self.llist_(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Llist_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Llist_Context, self).__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MatlabParser.RULE_llist_

     
        def copyFrom(self, ctx):
            super(MatlabParser.Llist_Context, self).copyFrom(ctx)


    class ListoneContext(Llist_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Llist_Context)
            super(MatlabParser.ListoneContext, self).__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterListone(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitListone(self)


    class ListallContext(Llist_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Llist_Context)
            super(MatlabParser.ListallContext, self).__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterListall(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitListall(self)


    class ListmoreContext(Llist_Context):

        def __init__(self, parser, ctx): # actually a MatlabParser.Llist_Context)
            super(MatlabParser.ListmoreContext, self).__init__(parser)
            self.copyFrom(ctx)

        def llist_(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.Llist_Context)
            else:
                return self.getTypedRuleContext(MatlabParser.Llist_Context,i)


        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterListmore(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitListmore(self)



    def llist_(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MatlabParser.Llist_Context(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 52
        self.enterRecursionRule(localctx, 52, self.RULE_llist_, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            token = self._input.LA(1)
            if token in [MatlabParser.T__27]:
                localctx = MatlabParser.ListallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 369
                self.match(MatlabParser.T__27)

            elif token in [MatlabParser.T__11, MatlabParser.T__13, MatlabParser.PRE, MatlabParser.ID, MatlabParser.INT, MatlabParser.FLOAT, MatlabParser.IINT, MatlabParser.IFLOAT, MatlabParser.STRING, MatlabParser.END]:
                localctx = MatlabParser.ListoneContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 370
                self.expr()

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 378
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,47,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = MatlabParser.ListmoreContext(self, MatlabParser.Llist_Context(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_llist_)
                    self.state = 373
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 374
                    self.match(MatlabParser.T__4)
                    self.state = 375
                    self.llist_(4) 
                self.state = 380
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,47,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class MatrixContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.MatrixContext, self).__init__(parent, invokingState)
            self.parser = parser

        def matrix_(self):
            return self.getTypedRuleContext(MatlabParser.Matrix_Context,0)


        def getRuleIndex(self):
            return MatlabParser.RULE_matrix

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterMatrix(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitMatrix(self)




    def matrix(self):

        localctx = MatlabParser.MatrixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_matrix)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.match(MatlabParser.T__13)
            self.state = 382
            self.matrix_(0)
            self.state = 384
            _la = self._input.LA(1)
            if _la==MatlabParser.T__4:
                self.state = 383
                self.match(MatlabParser.T__4)


            self.state = 387
            _la = self._input.LA(1)
            if _la==MatlabParser.T__1:
                self.state = 386
                self.match(MatlabParser.T__1)


            self.state = 389
            self.match(MatlabParser.T__14)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Matrix_Context(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.Matrix_Context, self).__init__(parent, invokingState)
            self.parser = parser

        def vector(self):
            return self.getTypedRuleContext(MatlabParser.VectorContext,0)


        def matrix_(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.Matrix_Context)
            else:
                return self.getTypedRuleContext(MatlabParser.Matrix_Context,i)


        def getRuleIndex(self):
            return MatlabParser.RULE_matrix_

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterMatrix_(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitMatrix_(self)



    def matrix_(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MatlabParser.Matrix_Context(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 56
        self.enterRecursionRule(localctx, 56, self.RULE_matrix_, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 392
            self.vector(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 418
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,55,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = MatlabParser.Matrix_Context(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_matrix_)
                    self.state = 394
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 413
                    token = self._input.LA(1)
                    if token in [MatlabParser.T__0, MatlabParser.T__28]:
                        self.state = 399 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while True:
                            self.state = 396
                            _la = self._input.LA(1)
                            if _la==MatlabParser.T__28:
                                self.state = 395
                                self.match(MatlabParser.T__28)


                            self.state = 398
                            self.match(MatlabParser.T__0)
                            self.state = 401 
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if not (_la==MatlabParser.T__0 or _la==MatlabParser.T__28):
                                break


                    elif token in [MatlabParser.T__1]:
                        self.state = 403
                        self.match(MatlabParser.T__1)
                        self.state = 410
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==MatlabParser.T__0 or _la==MatlabParser.T__28:
                            self.state = 405
                            _la = self._input.LA(1)
                            if _la==MatlabParser.T__28:
                                self.state = 404
                                self.match(MatlabParser.T__28)


                            self.state = 407
                            self.match(MatlabParser.T__0)
                            self.state = 412
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)


                    else:
                        raise NoViableAltException(self)

                    self.state = 415
                    self.matrix_(3) 
                self.state = 420
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,55,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class VectorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(MatlabParser.VectorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(MatlabParser.ExprContext,0)


        def vector(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(MatlabParser.VectorContext)
            else:
                return self.getTypedRuleContext(MatlabParser.VectorContext,i)


        def getRuleIndex(self):
            return MatlabParser.RULE_vector

        def enterRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.enterVector(self)

        def exitRule(self, listener):
            if isinstance( listener, MatlabListener ):
                listener.exitVector(self)



    def vector(self, _p=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MatlabParser.VectorContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 58
        self.enterRecursionRule(localctx, 58, self.RULE_vector, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 422
            self.expr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 429
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,56,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = MatlabParser.VectorContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_vector)
                    self.state = 424
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 425
                    self.match(MatlabParser.T__4)
                    self.state = 426
                    self.vector(3) 
                self.state = 431
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,56,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[24] = self.expr__sempred
        self._predicates[26] = self.llist__sempred
        self._predicates[28] = self.matrix__sempred
        self._predicates[29] = self.vector_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr__sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 14)
         

    def llist__sempred(self, localctx, predIndex):
            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

    def matrix__sempred(self, localctx, predIndex):
            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         

    def vector_sempred(self, localctx, predIndex):
            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         



