#include <iostream>
#include <sstream>
#include <string>
using namespace std;
#include <assert.h>

struct data_type {
  int value;
  bool stalled;
};

int resize(int val, int bits)
{
    int mask = (1<<bits)-1;
    int sign_bit = 1<<(bits-1);
    val = val & mask;
    if (val & sign_bit) 
    {
        val = val|~mask;
    }
    return val;
}

  const bool debug = true;

void execute_322();
data_type get_stream_321();
data_type get_stream_317();
data_type get_stream_316();
data_type get_stream_318();
data_type get_stream_320();
void execute_319();

//asserter
void execute_322()
{
  data_type data = get_stream_321();
  if (!data.stalled)
  {
    assert(data.value);
  }
}

//binary
data_type data_1_321 = {0, true};
data_type data_2_321 = {0, true};
data_type get_stream_321()
{
  data_type data;
  if (data_1_321.stalled)
    data_1_321 = get_stream_318();
  if (data_2_321.stalled)
    data_2_321 = get_stream_320();
  if(!data_1_321.stalled && !data_2_321.stalled)
  {
    data_1_321.stalled = true;
    data_2_321.stalled = true;
  }
  data.value = -resize((data_1_321.value == data_2_321.value), 1);
  data.stalled = data_1_321.stalled || data_2_321.stalled;
  if(debug){
   cerr << 321 << " binary " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//lookup table
int lookup_317[3] = 
{
49,48,10
};
data_type get_stream_317()
{
  data_type data = get_stream_316();
  data.value = lookup_317[data.value];
  data.stalled = false;
  if(debug){
   cerr << 317 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_316 = 0;
data_type get_stream_316()
{
  data_type data;
  data.stalled = false;
  data.value = count_316;
  count_316 += 1;
  if (count_316 > 2) count_316 = 0;
  if(debug){
   cerr << 316 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_318 = {0, true};
data_type get_stream_318()
{
  data_type data = output_318;
  output_318.stalled = true;
  if(debug){
   cerr << 318 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//repeater
data_type get_stream_320()
{
  data_type data =
  {
    10,
    false
  };
  if(debug){
   cerr << 320 << " repeater " << data.value << " " << data.stalled << endl;
  }
  return data;
}

const int OP_DIV_319 = 0;
const int OP_MOD_319 = 1;
const int OP_MUL_319 = 2;
const int OP_ADD_319 = 3;
const int OP_SUB_319 = 4;
const int OP_BAND_319 = 5;
const int OP_BOR_319 = 6;
const int OP_BXOR_319 = 7;
const int OP_SL_319 = 8;
const int OP_SR_319 = 9;
const int OP_EQ_319 = 10;
const int OP_NE_319 = 11;
const int OP_GE_319 = 12;
const int OP_GT_319 = 13;
const int OP_WAIT_US_319 = 14;
const int OP_JMP_319 = 15;
const int OP_JMPF_319 = 16;
const int OP_MOVE_319 = 17;
const int OP_IMM_319 = 18;
const int OP_READ_317_319 = 19;
const int OP_WRITE_318_319 = 20;
struct instruction_type_319 
{
  int operation;
  int srca;
  int srcb;
  int immediate;
};

instruction_type_319 instructions_319 [54] = 
{
  {OP_IMM_319, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_IMM_319, 2, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 148
  {OP_IMM_319, 3, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 172
  {OP_READ_317_319, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 148
  {OP_IMM_319, 4, 0, 48}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_319, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_GT_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 138
  {OP_MOVE_319, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_IMM_319, 6, 0, 57}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_GT_319, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 136
  {OP_BOR_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 130
  {OP_IMM_319, 5, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_319, 4, 0, 16}, //file: None line: None
  {OP_JMP_319, 0, 0, 18}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_319, 0, 0, 16}, //file: None line: None
  {OP_READ_317_319, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 148
  {OP_JMP_319, 0, 0, 4}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_MOVE_319, 4, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_IMM_319, 5, 0, 15}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_BAND_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 129
  {OP_MOVE_319, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_READ_317_319, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 148
  {OP_MOVE_319, 4, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_IMM_319, 5, 0, 48}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_GE_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 137
  {OP_IMM_319, 5, 0, 57}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_319, 6, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_GE_319, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_BAND_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 129
  {OP_JMPF_319, 4, 0, 42}, //file: None line: None
  {OP_MOVE_319, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 148
  {OP_IMM_319, 5, 0, 10}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MUL_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_MOVE_319, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_319, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 148
  {OP_MOVE_319, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 147
  {OP_IMM_319, 6, 0, 15}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_BAND_319, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 129
  {OP_ADD_319, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_319, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_319, 0, 0, 46}, //file: None line: None
  {OP_IMM_319, 4, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_JMPF_319, 4, 0, 46}, //file: None line: None
  {OP_JMP_319, 0, 0, 47}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 165
  {OP_JMP_319, 0, 0, 46}, //file: None line: None
  {OP_JMP_319, 0, 0, 22}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 165
  {OP_MOVE_319, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 148
  {OP_MOVE_319, 3, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_319, 4, 3, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 172
  {OP_WRITE_318_319, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 371
  {OP_JMP_319, 0, 0, 3}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 177
  {OP_JMP_319, 0, 0, 52}, //file: None line: None
  {OP_JMP_319, 0, 0, 0} //file: None line: None
};

//Process

int pc_319 = 0;
int registers_319[8];

void execute_319()
{
    instruction_type_319 instruction = instructions_319[pc_319];
    data_type data;
    int result = 0;
    int rega = registers_319[instruction.srca];
    int regb = registers_319[instruction.srcb];
    switch(instruction.operation)
    {
        case OP_DIV_319:
            result = resize(rega/regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_MOD_319:
            result = resize(rega%regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_MUL_319:
            result = resize(rega*regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_ADD_319:
            result = resize(rega+regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_SUB_319:
            result = resize(rega-regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_BAND_319:
            result = resize(rega&regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_BOR_319:
            result = resize(rega|regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_BXOR_319:
            result = resize(rega^regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_SL_319:
            result = resize(rega<<regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_SR_319:
            result = resize(rega>>regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_EQ_319:
            result = -resize(rega==regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_NE_319:
            result = -resize(rega!=regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_GE_319:
            result = -resize(rega>=regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_GT_319:
            result = -resize(rega>regb, 8); 
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_WAIT_US_319:
            break;
        case OP_JMP_319:
            pc_319 = instruction.immediate;
            break;
        case OP_JMPF_319:
            if (rega==0)
            {
              pc_319 = instruction.immediate;
            }
            else
            {
              pc_319++;
            }
            registers_319[instruction.srca] = result;
            break;
        case OP_MOVE_319:
            result = regb;
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
        case OP_IMM_319:
            result = instruction.immediate;
            pc_319++;
            registers_319[instruction.srca] = result;
            break;
          case OP_READ_317_319:
            data = get_stream_317();
            if (!data.stalled)
            {
              registers_319[instruction.srca] = data.value;
              pc_319 = pc_319;
            }
            break;
          case OP_WRITE_318_319:
            if (output_318.stalled)
            {
              output_318.stalled = false;
              output_318.value = rega;
              pc_319 = pc_319;
            }
            break;
        default:
            break;
    }
}
//main body
int main(int argc, char **argv)
{
  istringstream is;
  string cycle_string;
  int cycles;
  if (argc > 0)
  {
    cycle_string = argv[1];
    is.str(cycle_string);
    is >> cycles;
    for(int i = 0; i < cycles; i++)
    {
      cerr << "cycle ......................" << i << endl;
  execute_322();
execute_319();
    }
  }
}