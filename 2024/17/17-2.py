import tqdm, random

class Done(Exception):
    pass

class DoubleDone(Exception):
    pass
    
class Compy(object):
    a = 0
    b = 0
    c = 0
    pc = 0
    instrux = []

    def __init__(self, a=0, b=0, c=0, pc=0, instrux=[]):
        self.a, self.b, self.c, self.pc, self.instrux = a, b, c, pc, instrux
        
        self.mapping = { 0: self._divide_a, 1: self._xor_b_and_literal, 2: self._modulo_to_b, 3: self._jump_if_not_zero, 4: self._xor_b_and_c, 5: self._output, 6: self._divide_a_into_b, 7: self._divide_a_into_c}
        self.labels = { 0: "ADV", 1: "BXL", 2: "BST", 3: "JNZ", 4: "BXC", 5: "OUT", 6: "BDV", 7: "CDV" }
        self.labels_verbose = { 0: "Divide A by 2^combo operand storing to A", 1: "Xor B and literal, storing to B", 2: "Save last 3 bits of combo operand to B", 3: "Jump to PC operand if A is nonzero", 4: "Xor B and C to B, ignoring operand", 5: "Output combo operand", 6: "Divide A by 2^combo operand storing to B", 7: "Divide A by 2^combo operand storing to C" }
        
        # print("COMPY ONLNIEE!!!")
        
    def compute(self):
        if self.pc >= len(self.instrux) - 1:
            # print("We out of instrux")
            raise Done
        
        instruction, operand = self.instrux[self.pc:self.pc+2]
        # print("before", self.labels[instruction], operand, "A", self.a, "B", self.b, "C", self.c, "PC", self.pc)
        retval = self.mapping[instruction](operand)
        # print("after", self.labels[instruction], operand, "A", self.a, "B", self.b, "C", self.c, "PC", self.pc, "retval", retval)
        
        return retval
        
    def decompile(self):
        print("Starting registers: A", self.a, "B", self.b, "C", self.c, "PC", self.pc)
        for i in range(len(self.instrux) // 2):
            instruction = self.instrux[i*2]
            operand = self.instrux[i*2 + 1]
            lv =  self.labels_verbose[instruction]
            if instruction in (0, 2, 5, 6, 7):
                voperand = operand
                if operand == 4:
                    voperand = "A"
                if operand == 5:
                    voperand = "B"
                if operand == 6:
                    voperand = "C"
                if "combo operand" in lv:
                    lv = lv.replace("combo operand", "combo operand " + str(voperand))
            else:
                if "literal" in lv:
                    lv = lv.replace("literal", "literal " + str(operand))
           
                
                    
            print(i*2, self.labels[instruction], lv, "...", instruction, "-", operand)
            
    def _lookup_combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        if operand==4:
            return self.a
        if operand==5:
            return self.b
        if operand==6:
            return self.c
        if operand > 6:
            raise ValueError("Illegal combo operand", operand)
            
    def _divide_a(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.a = numerator // divisor
        self.pc += 2
        
        
    def _divide_a_into_b(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.b = numerator // divisor
        self.pc += 2
        
    def _divide_a_into_c(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.c = numerator // divisor
        self.pc += 2
    
    def _xor_b_and_literal(self, operand):
        self.b = self.b ^ operand
        self.pc += 2
        
    def _xor_b_and_c(self, operand):
        self.b = self.b ^ self.c
        self.pc += 2

    def _modulo_to_b(self, operand):
        self.b = self._lookup_combo_operand(operand) & 7
        self.pc += 2
        
    def _jump_if_not_zero(self, operand):
        if self.a == 0:
            self.pc += 2
        else:
            self.pc = operand
    
    def _output(self, operand):
        self.pc += 2
        return self._lookup_combo_operand(operand) & 7
        
desired_instrux = []

with open("input", "r") as fh:
    for line in fh:
        if "Register A: " in line:
            init_a = int(line.strip().split("Register A: ")[1])
        elif "Register B: " in line:
            init_b = int(line.strip().split("Register B: ")[1])
        elif "Register C: " in line:
            init_c = int(line.strip().split("Register C: ")[1])
        elif "Program: " in line:
            desired_instrux = [int(i) for i in line.strip().split("Program: ")[1].split(",") ] 
            

compy = Compy(init_a, init_b, init_c, 0, desired_instrux.copy())
compy.decompile()
desired_length = len(desired_instrux)

a = 2
yuge = 9999999999999999999999
increments = {}
known_good_minimums = {}
for i in range(desired_length):
    increments[i] = pow(10, i)
    known_good_minimums[i] = yuge
prev_best = desired_length + 1

try:
    while True:
        if a < 0:
            a = 2
        print("trying", a)
        outputs = []
        compy = Compy(a, init_b, init_c, 0, desired_instrux.copy())
            
        try:
            while True:
                output = compy.compute()
                if output is not None:
                    outputs.append(output)
                # print (",".join([str(i) for i in outputs]))
                    
        except Done:
            if len(outputs) < desired_length :
                increments[len(outputs)] = min(a, increments[len(outputs)])
                a = max(a+1, int(a*1.1))
            elif len(outputs) > desired_length:
                print("too long")
                if (prev_best < desired_length) and (known_good_minimums[prev_best] != yuge) and (random.random() > 0.5):
                    print("reset to known_good_minimum", known_good_minimums[prev_best])
                    a = known_good_minimums[prev_best]
                else:
                    a = int(a * random.random())
            else:
                for i in reversed(range(desired_length)):
                    
                    if outputs[i] != desired_instrux[i]:
                        # if i > prev_best:
                            # val = int(known_good_minimums[prev_best] + ( increments[prev_best + 1] * (0.5 - random.random())))
                            # print("bad at", i, "reset to prev known best", prev_best,  val)
                            # a = val
                        # else:
                        amount = max(int((random.random()) * 1.0 * increments[max(0, i-1)]), 1)
                        
                        print("add increment stage", i, "amount", amount)
                        a += amount
                        break
                            
                    else:
                        if a < known_good_minimums[i]:
                            known_good_minimums[i] = a
                        if i < prev_best:
                            prev_best = i
            if outputs == desired_instrux:
                print(a)
                raise DoubleDone
                
                
            print(increments)
            print(known_good_minimums)
            print(outputs)
            print(desired_instrux)
        
        prev_a = a
        
except DoubleDone:
    pass
    
# for i in tqdm.trange(999999999999): 
        # a = (pow(2, i) * mega) + mini
    # a = i + (35184372085000)
    # a = i + (265054779860000)
    # a = i*1000000 + (265000000000000)
    # print(a)
    # outputs = []
    # compy = Compy(a, init_b, init_c, 0, desired_instrux.copy())
    
    # try:
        # while True:
            # output = compy.compute()
            # if output is not None:
                # outputs.append(output)
            # print (",".join([str(i) for i in outputs]))
                
    # except Done:
        # if outputs==desired_instrux or outputs[-7:] == [7, 4, 1, 5, 5, 3, 0]:
            # print(a)
            # raise DoubleDone 
        # else:
            # print(outputs[-7:])
            # print(desired_instrux)
