instructions = {
        0:('literal', 1),
        1:('add', 1),
        2:('literal', 2),
        3:('add', 2),
        4:('add', 1),
        5:('literal', 4),
        6:('literal', 5),
        7:('add', 4),
}

#instructions which write to a register regardless of its
#previous value
writers = ('literal')

#instructions which write to a register but the value written depends on
#a previous value
read_writers = ('add')

#instructions whch read from a register.
readers = ('add')

print instructions
#make a list of registers

registers = []
for pc, instruction in instructions.iteritems():
    operation, register = instruction
    if register not in registers:
        if operation in writers:
            registers.append(register)
print registers

born = {}
died = {}
lives = {}
life = 0
for register in registers:
    alive = False
    for pc, instruction in instructions.iteritems():
        operation, thisreg = instruction
        if register == thisreg:
            if alive:
                #the last time the register is used is when it died
                if operation in readers:
                    died[life]=pc
                if operation in read_writers:
                    died[life]=pc
                if operation in writers:
                    life += 1
                    born[life]=pc
                    died[life]=pc
                    lives[life]=register
            else:
                if operation in writers:
                    life += 1
                    alive = True
                    born[life]=pc
                    died[life]=pc
                    lives[life]=register
#new_lives = {}
#for life in lives:
#    if born[life]!=died[life]:
#        new_lives[life]=lives[life]
#lives = new_lives

for i in lives:
    print "life",
    print i,
    print "register",
    print lives[i]
    print "born",
    print born[i], 
    print "died",
    print died[i]

allocator = 0
allocated = []
unallocated = []
mapping = {}
for i in lives:
    #attempt to dealocate dead registers
    new_allocated = {}
    for j in allocated:
        print j
        if died[allocated[j]] >= born[i]:
            new_allocated[j] = allocated[j]
        else:
            unallocated.append(j)
    allocated = new_allocated        

    #if unallocated registers are available
    #allocate them to this life
    if unallocated:
        a = unallocated.pop()
        mapping[lives[i]] = a
        allocated[a] = i
    #otherwise create a new register
    else:
        a = allocator
        allocator += 1
        mapping[lives[i]] = a
        allocated[a] = i

#original register to new register mapping
print mapping

