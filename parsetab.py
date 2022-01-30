
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADDSUBleftMULDIVADD BEGIN BIG CHECK CLOSING_BR COMMA COMPASS DIV DO DOT END FIELD GO GR_EQ L_ASSIGNMENT L_EQ MUL NORMAL N_EQ OPEN_BR RETURN RL RR R_ASSIGNMENT SMALL SONAR SQ_CLOSING_BR SQ_OPEN_BR SUB S_NUMBER TINY UNTIL U_NUMBER VARIABLEprogram : fun_listfun_list : function fun_list\n                    | functionfunction : type VARIABLE SQ_OPEN_BR par_list SQ_CLOSING_BR BEGIN stmt_list END DOT\n                    | type VARIABLE SQ_OPEN_BR SQ_CLOSING_BR BEGIN stmt_list END DOTpar_list : parameter COMMA par_list\n                    | parameterparameter : type VARIABLEstmt_list : statement COMMA stmt_list\n                    | statement DOTstatement : declaration\n                    | assignment\n                    | arithm_operation\n                    | until\n                    | check\n                    | function_call\n                    | robot_operation\n                    | returndeclaration : type variable_list R_ASSIGNMENT literal\n                        | FIELD type type variable_list R_ASSIGNMENT literaltype : TINY\n                | SMALL\n                | NORMAL\n                | BIGvariable_list : VARIABLE variable_list\n                        | VARIABLEliteral : U_NUMBER\n                    | S_NUMBERassignment : arithm_operation R_ASSIGNMENT arithm_operation\n                        | arithm_operation R_ASSIGNMENT assignment\n                        | arithm_operation L_ASSIGNMENT arithm_operation\n                        | arithm_operation L_ASSIGNMENT assignmentarithm_operation : OPEN_BR arithm_operation CLOSING_BR\n                            | ADD arithm_operation\n                            | SUB arithm_operation\n                            | arithm_operation MUL arithm_operation\n                            | arithm_operation DIV arithm_operation\n                            | arithm_operation ADD arithm_operation\n                            | arithm_operation SUB arithm_operationarithm_operation : varlitvarlit : VARIABLE\n                    | literalcomparison : arithm_operation N_EQ arithm_operation\n                        | arithm_operation L_EQ arithm_operation\n                        | arithm_operation GR_EQ arithm_operation\n                        | arithm_operation N_EQ varlit\n                        | arithm_operation L_EQ varlit\n                        | arithm_operation GR_EQ varlit\n                        | varlit N_EQ arithm_operation\n                        | varlit L_EQ arithm_operation\n                        | varlit GR_EQ arithm_operation\n                        | varlit N_EQ varlit\n                        | varlit L_EQ varlit\n                        | varlit GR_EQ varlituntil : UNTIL comparison DO stmt_listcheck : CHECK comparison DO stmt_listfunction_call : VARIABLE OPEN_BR variable_list CLOSING_BRrobot_operation : GO\n                            | RL\n                            | RR\n                            | SONAR\n                            | COMPASSreturn : RETURN varlit'
    
_lr_action_items = {'TINY':([0,3,5,6,7,8,11,18,19,20,34,55,63,77,89,96,97,],[5,5,-21,-22,-23,-24,5,5,5,5,5,5,5,-5,5,5,-4,]),'SMALL':([0,3,5,6,7,8,11,18,19,20,34,55,63,77,89,96,97,],[6,6,-21,-22,-23,-24,6,6,6,6,6,6,6,-5,6,6,-4,]),'NORMAL':([0,3,5,6,7,8,11,18,19,20,34,55,63,77,89,96,97,],[7,7,-21,-22,-23,-24,7,7,7,7,7,7,7,-5,7,7,-4,]),'BIG':([0,3,5,6,7,8,11,18,19,20,34,55,63,77,89,96,97,],[8,8,-21,-22,-23,-24,8,8,8,8,8,8,8,-5,8,8,-4,]),'$end':([1,2,3,9,77,97,],[0,-1,-3,-2,-5,-4,]),'VARIABLE':([4,5,6,7,8,12,18,20,21,35,36,37,39,40,46,52,53,55,57,58,59,60,61,62,87,89,90,91,92,93,94,95,96,],[10,-21,-22,-23,-24,16,22,22,52,65,65,65,65,65,65,52,52,22,65,65,65,65,65,65,52,22,65,65,65,65,65,65,22,]),'SQ_OPEN_BR':([10,],[11,]),'SQ_CLOSING_BR':([11,13,15,16,49,],[14,17,-7,-8,-6,]),'BEGIN':([14,17,],[18,20,]),'COMMA':([15,16,22,24,25,26,27,28,29,30,31,32,33,38,41,42,43,44,45,47,48,56,65,66,67,72,78,79,80,81,82,83,84,85,86,88,98,99,101,114,116,],[19,-8,-41,55,-11,-12,-13,-14,-15,-16,-17,-18,-42,-40,-58,-59,-60,-61,-62,-27,-28,-10,-41,-34,-35,-63,-9,-29,-30,-31,-32,-36,-37,-38,-39,-33,-19,-57,-55,-56,-20,]),'FIELD':([18,20,55,89,96,],[34,34,34,34,34,]),'OPEN_BR':([18,20,22,35,36,37,39,40,55,57,58,59,60,61,62,89,90,91,92,93,94,95,96,],[35,35,53,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'ADD':([18,20,22,27,33,35,36,37,38,39,40,47,48,55,57,58,59,60,61,62,64,65,66,67,69,70,79,81,83,84,85,86,88,89,90,91,92,93,94,95,96,102,103,104,105,106,107,108,109,110,111,112,113,],[36,36,-41,61,-42,36,36,36,-40,36,36,-27,-28,36,36,36,36,36,36,36,61,-41,-34,-35,61,-40,61,61,-36,-37,-38,-39,-33,36,36,36,36,36,36,36,36,61,-40,61,-40,61,-40,-40,61,-40,61,-40,61,]),'SUB':([18,20,22,27,33,35,36,37,38,39,40,47,48,55,57,58,59,60,61,62,64,65,66,67,69,70,79,81,83,84,85,86,88,89,90,91,92,93,94,95,96,102,103,104,105,106,107,108,109,110,111,112,113,],[37,37,-41,62,-42,37,37,37,-40,37,37,-27,-28,37,37,37,37,37,37,37,62,-41,-34,-35,62,-40,62,62,-36,-37,-38,-39,-33,37,37,37,37,37,37,37,37,62,-40,62,-40,62,-40,-40,62,-40,62,-40,62,]),'UNTIL':([18,20,55,89,96,],[39,39,39,39,39,]),'CHECK':([18,20,55,89,96,],[40,40,40,40,40,]),'GO':([18,20,55,89,96,],[41,41,41,41,41,]),'RL':([18,20,55,89,96,],[42,42,42,42,42,]),'RR':([18,20,55,89,96,],[43,43,43,43,43,]),'SONAR':([18,20,55,89,96,],[44,44,44,44,44,]),'COMPASS':([18,20,55,89,96,],[45,45,45,45,45,]),'RETURN':([18,20,55,89,96,],[46,46,46,46,46,]),'U_NUMBER':([18,20,35,36,37,39,40,46,55,57,58,59,60,61,62,74,89,90,91,92,93,94,95,96,115,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'S_NUMBER':([18,20,35,36,37,39,40,46,55,57,58,59,60,61,62,74,89,90,91,92,93,94,95,96,115,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'R_ASSIGNMENT':([22,27,33,38,47,48,51,52,65,66,67,75,79,81,83,84,85,86,88,100,],[-41,57,-42,-40,-27,-28,74,-26,-41,-34,-35,-25,57,57,-36,-37,-38,-39,-33,115,]),'L_ASSIGNMENT':([22,27,33,38,47,48,65,66,67,79,81,83,84,85,86,88,],[-41,58,-42,-40,-27,-28,-41,-34,-35,58,58,-36,-37,-38,-39,-33,]),'MUL':([22,27,33,38,47,48,64,65,66,67,69,70,79,81,83,84,85,86,88,102,103,104,105,106,107,108,109,110,111,112,113,],[-41,59,-42,-40,-27,-28,59,-41,59,59,59,-40,59,59,-36,-37,59,59,-33,59,-40,59,-40,59,-40,-40,59,-40,59,-40,59,]),'DIV':([22,27,33,38,47,48,64,65,66,67,69,70,79,81,83,84,85,86,88,102,103,104,105,106,107,108,109,110,111,112,113,],[-41,60,-42,-40,-27,-28,60,-41,60,60,60,-40,60,60,-36,-37,60,60,-33,60,-40,60,-40,60,-40,-40,60,-40,60,-40,60,]),'DOT':([22,24,25,26,27,28,29,30,31,32,33,38,41,42,43,44,45,47,48,54,56,65,66,67,72,73,78,79,80,81,82,83,84,85,86,88,98,99,101,114,116,],[-41,56,-11,-12,-13,-14,-15,-16,-17,-18,-42,-40,-58,-59,-60,-61,-62,-27,-28,77,-10,-41,-34,-35,-63,97,-9,-29,-30,-31,-32,-36,-37,-38,-39,-33,-19,-57,-55,-56,-20,]),'END':([23,50,56,78,],[54,73,-10,-9,]),'CLOSING_BR':([33,38,47,48,52,64,65,66,67,75,76,83,84,85,86,88,],[-42,-40,-27,-28,-26,88,-41,-34,-35,-25,99,-36,-37,-38,-39,-33,]),'N_EQ':([33,38,47,48,65,66,67,69,70,83,84,85,86,88,],[-42,-40,-27,-28,-41,-34,-35,90,93,-36,-37,-38,-39,-33,]),'L_EQ':([33,38,47,48,65,66,67,69,70,83,84,85,86,88,],[-42,-40,-27,-28,-41,-34,-35,91,94,-36,-37,-38,-39,-33,]),'GR_EQ':([33,38,47,48,65,66,67,69,70,83,84,85,86,88,],[-42,-40,-27,-28,-41,-34,-35,92,95,-36,-37,-38,-39,-33,]),'DO':([33,38,47,48,65,66,67,68,71,83,84,85,86,88,102,103,104,105,106,107,108,109,110,111,112,113,],[-42,-40,-27,-28,-41,-34,-35,89,96,-36,-37,-38,-39,-33,-43,-40,-44,-40,-45,-40,-40,-49,-40,-50,-40,-51,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'fun_list':([0,3,],[2,9,]),'function':([0,3,],[3,3,]),'type':([0,3,11,18,19,20,34,55,63,89,96,],[4,4,12,21,12,21,63,21,87,21,21,]),'par_list':([11,19,],[13,49,]),'parameter':([11,19,],[15,15,]),'stmt_list':([18,20,55,89,96,],[23,50,78,101,114,]),'statement':([18,20,55,89,96,],[24,24,24,24,24,]),'declaration':([18,20,55,89,96,],[25,25,25,25,25,]),'assignment':([18,20,55,57,58,89,96,],[26,26,26,80,82,26,26,]),'arithm_operation':([18,20,35,36,37,39,40,55,57,58,59,60,61,62,89,90,91,92,93,94,95,96,],[27,27,64,66,67,69,69,27,79,81,83,84,85,86,27,102,104,106,109,111,113,27,]),'until':([18,20,55,89,96,],[28,28,28,28,28,]),'check':([18,20,55,89,96,],[29,29,29,29,29,]),'function_call':([18,20,55,89,96,],[30,30,30,30,30,]),'robot_operation':([18,20,55,89,96,],[31,31,31,31,31,]),'return':([18,20,55,89,96,],[32,32,32,32,32,]),'literal':([18,20,35,36,37,39,40,46,55,57,58,59,60,61,62,74,89,90,91,92,93,94,95,96,115,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,98,33,33,33,33,33,33,33,33,116,]),'varlit':([18,20,35,36,37,39,40,46,55,57,58,59,60,61,62,89,90,91,92,93,94,95,96,],[38,38,38,38,38,70,70,72,38,38,38,38,38,38,38,38,103,105,107,108,110,112,38,]),'variable_list':([21,52,53,87,],[51,75,76,100,]),'comparison':([39,40,],[68,71,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> fun_list','program',1,'p_program','Parser.py',40),
  ('fun_list -> function fun_list','fun_list',2,'p_fun_list','Parser.py',44),
  ('fun_list -> function','fun_list',1,'p_fun_list','Parser.py',45),
  ('function -> type VARIABLE SQ_OPEN_BR par_list SQ_CLOSING_BR BEGIN stmt_list END DOT','function',9,'p_function','Parser.py',52),
  ('function -> type VARIABLE SQ_OPEN_BR SQ_CLOSING_BR BEGIN stmt_list END DOT','function',8,'p_function','Parser.py',53),
  ('par_list -> parameter COMMA par_list','par_list',3,'p_par_list','Parser.py',89),
  ('par_list -> parameter','par_list',1,'p_par_list','Parser.py',90),
  ('parameter -> type VARIABLE','parameter',2,'p_parameter','Parser.py',97),
  ('stmt_list -> statement COMMA stmt_list','stmt_list',3,'p_stmt_list','Parser.py',111),
  ('stmt_list -> statement DOT','stmt_list',2,'p_stmt_list','Parser.py',112),
  ('statement -> declaration','statement',1,'p_statement','Parser.py',120),
  ('statement -> assignment','statement',1,'p_statement','Parser.py',121),
  ('statement -> arithm_operation','statement',1,'p_statement','Parser.py',122),
  ('statement -> until','statement',1,'p_statement','Parser.py',123),
  ('statement -> check','statement',1,'p_statement','Parser.py',124),
  ('statement -> function_call','statement',1,'p_statement','Parser.py',125),
  ('statement -> robot_operation','statement',1,'p_statement','Parser.py',126),
  ('statement -> return','statement',1,'p_statement','Parser.py',127),
  ('declaration -> type variable_list R_ASSIGNMENT literal','declaration',4,'p_declaration','Parser.py',136),
  ('declaration -> FIELD type type variable_list R_ASSIGNMENT literal','declaration',6,'p_declaration','Parser.py',137),
  ('type -> TINY','type',1,'p_type','Parser.py',152),
  ('type -> SMALL','type',1,'p_type','Parser.py',153),
  ('type -> NORMAL','type',1,'p_type','Parser.py',154),
  ('type -> BIG','type',1,'p_type','Parser.py',155),
  ('variable_list -> VARIABLE variable_list','variable_list',2,'p_variable_list','Parser.py',159),
  ('variable_list -> VARIABLE','variable_list',1,'p_variable_list','Parser.py',160),
  ('literal -> U_NUMBER','literal',1,'p_literal','Parser.py',175),
  ('literal -> S_NUMBER','literal',1,'p_literal','Parser.py',176),
  ('assignment -> arithm_operation R_ASSIGNMENT arithm_operation','assignment',3,'p_assignment','Parser.py',186),
  ('assignment -> arithm_operation R_ASSIGNMENT assignment','assignment',3,'p_assignment','Parser.py',187),
  ('assignment -> arithm_operation L_ASSIGNMENT arithm_operation','assignment',3,'p_assignment','Parser.py',188),
  ('assignment -> arithm_operation L_ASSIGNMENT assignment','assignment',3,'p_assignment','Parser.py',189),
  ('arithm_operation -> OPEN_BR arithm_operation CLOSING_BR','arithm_operation',3,'p_arithm_operation','Parser.py',222),
  ('arithm_operation -> ADD arithm_operation','arithm_operation',2,'p_arithm_operation','Parser.py',223),
  ('arithm_operation -> SUB arithm_operation','arithm_operation',2,'p_arithm_operation','Parser.py',224),
  ('arithm_operation -> arithm_operation MUL arithm_operation','arithm_operation',3,'p_arithm_operation','Parser.py',225),
  ('arithm_operation -> arithm_operation DIV arithm_operation','arithm_operation',3,'p_arithm_operation','Parser.py',226),
  ('arithm_operation -> arithm_operation ADD arithm_operation','arithm_operation',3,'p_arithm_operation','Parser.py',227),
  ('arithm_operation -> arithm_operation SUB arithm_operation','arithm_operation',3,'p_arithm_operation','Parser.py',228),
  ('arithm_operation -> varlit','arithm_operation',1,'p_arithm_operation_endpoints','Parser.py',259),
  ('varlit -> VARIABLE','varlit',1,'p_varlit','Parser.py',273),
  ('varlit -> literal','varlit',1,'p_varlit','Parser.py',274),
  ('comparison -> arithm_operation N_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',281),
  ('comparison -> arithm_operation L_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',282),
  ('comparison -> arithm_operation GR_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',283),
  ('comparison -> arithm_operation N_EQ varlit','comparison',3,'p_comparison','Parser.py',284),
  ('comparison -> arithm_operation L_EQ varlit','comparison',3,'p_comparison','Parser.py',285),
  ('comparison -> arithm_operation GR_EQ varlit','comparison',3,'p_comparison','Parser.py',286),
  ('comparison -> varlit N_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',287),
  ('comparison -> varlit L_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',288),
  ('comparison -> varlit GR_EQ arithm_operation','comparison',3,'p_comparison','Parser.py',289),
  ('comparison -> varlit N_EQ varlit','comparison',3,'p_comparison','Parser.py',290),
  ('comparison -> varlit L_EQ varlit','comparison',3,'p_comparison','Parser.py',291),
  ('comparison -> varlit GR_EQ varlit','comparison',3,'p_comparison','Parser.py',292),
  ('until -> UNTIL comparison DO stmt_list','until',4,'p_until','Parser.py',302),
  ('check -> CHECK comparison DO stmt_list','check',4,'p_check','Parser.py',311),
  ('function_call -> VARIABLE OPEN_BR variable_list CLOSING_BR','function_call',4,'p_function_call','Parser.py',320),
  ('robot_operation -> GO','robot_operation',1,'p_robot_operation','Parser.py',328),
  ('robot_operation -> RL','robot_operation',1,'p_robot_operation','Parser.py',329),
  ('robot_operation -> RR','robot_operation',1,'p_robot_operation','Parser.py',330),
  ('robot_operation -> SONAR','robot_operation',1,'p_robot_operation','Parser.py',331),
  ('robot_operation -> COMPASS','robot_operation',1,'p_robot_operation','Parser.py',332),
  ('return -> RETURN varlit','return',2,'p_return','Parser.py',339),
]