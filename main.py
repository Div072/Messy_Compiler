import sys
from lexer import  Lexer
from parser import Parser
from ass_generator import*
from generate_IR_code import parse_to_IR
from ass_traverser import*
def runFile(file_path):
    with open(file_path,'r') as file:
        source = file.read()
        lexer = Lexer(source)
        lexer.scan()
        parser = Parser(lexer.tokens)
        obj = parser.parse()
        ir_code = parse_to_IR()
        inter_med = ir_code.traverse(obj)
        assembly_obj = convert_ast_to_assembly(inter_med)
        second_pass_traverse(assembly_obj)
        third_pass_traverse(assembly_obj)
        generated_ass = Ass_Generator()
        generated_ass.generate_ass(assembly_obj)
        print("debug")
if __name__ == '__main__':
    debug_mode = True
    if debug_mode:
        source_path = "./main.c"
    else:
        source_path = sys.argv[1]
    runFile(source_path)