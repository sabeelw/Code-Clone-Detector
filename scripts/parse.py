import javalang

feature_map = {'FormalParameter': 1, 'CatchClause': 2, 'LocalVariableDeclaration': 3,
               'MemberReference': 4,
               'StatementExpression': 25, 'ArrayInitializer': 6,
               'SwitchStatement': 7, 'ArrayCreator': 8,
               'SynchronizedStatement': 9, 'DoStatement': 10,
               'AssertStatement': 0, 'ArraySelector': 22,
               'Annotation': 23, 'IfStatement': 7, 'BasicType': 12,
               'CatchClauseParameter': 13, 'VariableDeclarator': 14, 'TryResource': 15,
               'VariableDeclaration': 16, 'BlockStatement': 7, 'TryStatement': 18,
               'BinaryOperation': 19, 'ForStatement': 11,
               'Assignment': 20,
               'WhileStatement': 11, 'ReferenceType': 26, 'EnhancedForControl': 24,
               'MethodInvocation': 21, 'SwitchStatementCase': 7}

def iterateAST(root):
    q = [root]


def traverseAST(root, s):
    if type(root) in {list, tuple}:
        for i in root:
            traverseAST(i, s)
    if hasattr(root, "attrs"):
        s.append(root.__class__.__name__)
        # if name in feature_map:
        #     vec[feature_map[name]] += 1
        q = list(root.attrs)
        while q:
            traverseAST(root.__getattribute__(q.pop()), s)


def getVector(code):
    code = '''class clone{
    %s
    }''' % code
    s = []
    try:
        ast = javalang.parse.parse(code)
    except:
        return []
    traverseAST(ast, s)
    return s

#
# import time
#
# t1 = time.time()
# print(getVector(
#     '''class test{
#     public static void main(){
#       if(1==1){
#       System.out.Println("hello world");
#       }else{
#       System.out.Println("hello world");
#       }
#     }
#     }''')
#       )
# t2 = time.time()
#
# print(f"Time Taken: {t2 - t1}")
# with open("shakespeare.txt", "r") as file:
#     print(list(x.strfile.read().split("\n\n")))
