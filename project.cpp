#include <iostream>
#include <sstream>
#include <fstream>
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

  const bool debug = false;

void execute_369();
data_type get_stream_368();
data_type get_stream_364();
data_type get_stream_363();
data_type get_stream_365();
data_type get_stream_367();
void execute_366();

//asserter
void execute_369()
{
  data_type data = get_stream_368();
  if (!data.stalled)
  {
    assert(data.value);
  }
}

//binary
data_type data_1_368 = {0, true};
data_type data_2_368 = {0, true};
data_type get_stream_368()
{
  data_type data;
  if (data_1_368.stalled)
    data_1_368 = get_stream_365();
  if (data_2_368.stalled)
    data_2_368 = get_stream_367();
  if(!data_1_368.stalled && !data_2_368.stalled)
  {
    data_1_368.stalled = true;
    data_2_368.stalled = true;
  }
  data.value = -resize((data_1_368.value == data_2_368.value), 1);
  data.stalled = data_1_368.stalled || data_2_368.stalled;
  if(debug){
   cerr << 368 << " binary " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//lookup table
int lookup_364[3] = 
{
49,48,10
};
data_type get_stream_364()
{
  data_type data = get_stream_363();
  data.value = lookup_364[data.value];
  data.stalled = false;
  if(debug){
   cerr << 364 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_363 = 0;
data_type get_stream_363()
{
  data_type data;
  data.stalled = false;
  data.value = count_363;
  count_363 += 1;
  if (count_363 > 2) count_363 = 0;
  if(debug){
   cerr << 363 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_365 = {0, true};
data_type get_stream_365()
{
  data_type data = output_365;
  output_365.stalled = true;
  if(debug){
   cerr << 365 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//repeater
data_type get_stream_367()
{
  data_type data =
  {
    10,
    false
  };
  if(debug){
   cerr << 367 << " repeater " << data.value << " " << data.stalled << endl;
  }
  return data;
}

const int OP_DIV_366 = 0;
const int OP_MOD_366 = 1;
const int OP_MUL_366 = 2;
const int OP_ADD_366 = 3;
const int OP_SUB_366 = 4;
const int OP_BAND_366 = 5;
const int OP_BOR_366 = 6;
const int OP_BXOR_366 = 7;
const int OP_SL_366 = 8;
const int OP_SR_366 = 9;
const int OP_EQ_366 = 10;
const int OP_NE_366 = 11;
const int OP_GE_366 = 12;
const int OP_GT_366 = 13;
const int OP_WAIT_US_366 = 14;
const int OP_JMP_366 = 15;
const int OP_JMPF_366 = 16;
const int OP_MOVE_366 = 17;
const int OP_IMM_366 = 18;
const int OP_READ_364_366 = 19;
const int OP_WRITE_365_366 = 20;
struct instruction_type_366 
{
  int operation;
  int srca;
  int srcb;
  int immediate;
};

instruction_type_366 instructions_366 [54] = 
{
  {OP_IMM_366, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_IMM_366, 2, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 149
  {OP_IMM_366, 3, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 173
  {OP_READ_364_366, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/streams.py line: 283
  {OP_IMM_366, 4, 0, 48}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_MOVE_366, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_GT_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 137
  {OP_MOVE_366, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_IMM_366, 6, 0, 57}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_GT_366, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 135
  {OP_BOR_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 129
  {OP_IMM_366, 5, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_EQ_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 133
  {OP_JMPF_366, 4, 0, 16}, //file: None line: None
  {OP_JMP_366, 0, 0, 18}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 63
  {OP_JMP_366, 0, 0, 16}, //file: None line: None
  {OP_READ_364_366, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/streams.py line: 283
  {OP_JMP_366, 0, 0, 4}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 64
  {OP_MOVE_366, 4, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_IMM_366, 5, 0, 15}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_BAND_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 128
  {OP_MOVE_366, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 273
  {OP_READ_364_366, 1, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/streams.py line: 283
  {OP_MOVE_366, 4, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_IMM_366, 5, 0, 48}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_GE_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 136
  {OP_IMM_366, 5, 0, 57}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_MOVE_366, 6, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_GE_366, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 138
  {OP_BAND_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 128
  {OP_JMPF_366, 4, 0, 42}, //file: None line: None
  {OP_MOVE_366, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 149
  {OP_IMM_366, 5, 0, 10}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_MUL_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 125
  {OP_MOVE_366, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 273
  {OP_MOVE_366, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 149
  {OP_MOVE_366, 5, 1, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 148
  {OP_IMM_366, 6, 0, 15}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_BAND_366, 5, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 128
  {OP_ADD_366, 4, 5, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 123
  {OP_MOVE_366, 2, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 273
  {OP_JMP_366, 0, 0, 46}, //file: None line: None
  {OP_IMM_366, 4, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 118
  {OP_JMPF_366, 4, 0, 46}, //file: None line: None
  {OP_JMP_366, 0, 0, 47}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 166
  {OP_JMP_366, 0, 0, 46}, //file: None line: None
  {OP_JMP_366, 0, 0, 22}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 166
  {OP_MOVE_366, 4, 2, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 149
  {OP_MOVE_366, 3, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/instruction.py line: 273
  {OP_MOVE_366, 4, 3, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 173
  {OP_WRITE_365_366, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/chips/streams.py line: 592
  {OP_JMP_366, 0, 0, 3}, //file: /usr/local/lib/python2.6/dist-packages/chips/__init__.py line: 178
  {OP_JMP_366, 0, 0, 52}, //file: None line: None
  {OP_JMP_366, 0, 0, 0} //file: None line: None
};

//Process

int pc_366 = 0;
int registers_366[8];

void execute_366()
{
    instruction_type_366 instruction = instructions_366[pc_366];
    data_type data;
    int result = 0;
    int rega = registers_366[instruction.srca];
    int regb = registers_366[instruction.srcb];
    switch(instruction.operation)
    {
        case OP_DIV_366:
            result = resize(rega/regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_MOD_366:
            result = resize(rega%regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_MUL_366:
            result = resize(rega*regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_ADD_366:
            result = resize(rega+regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_SUB_366:
            result = resize(rega-regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_BAND_366:
            result = resize(rega&regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_BOR_366:
            result = resize(rega|regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_BXOR_366:
            result = resize(rega^regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_SL_366:
            result = resize(rega<<regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_SR_366:
            result = resize(rega>>regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_EQ_366:
            result = -resize(rega==regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_NE_366:
            result = -resize(rega!=regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_GE_366:
            result = -resize(rega>=regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_GT_366:
            result = -resize(rega>regb, 8); 
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_WAIT_US_366:
            break;
        case OP_JMP_366:
            pc_366 = instruction.immediate;
            break;
        case OP_JMPF_366:
            if (rega==0)
            {
              pc_366 = instruction.immediate;
            }
            else
            {
              pc_366++;
            }
            registers_366[instruction.srca] = result;
            break;
        case OP_MOVE_366:
            result = regb;
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
        case OP_IMM_366:
            result = instruction.immediate;
            pc_366++;
            registers_366[instruction.srca] = result;
            break;
          case OP_READ_364_366:
            data = get_stream_364();
            if (!data.stalled)
            {
              registers_366[instruction.srca] = data.value;
              pc_366++;
            }
            break;
          case OP_WRITE_365_366:
            if (output_365.stalled)
            {
              output_365.stalled = false;
              output_365.value = rega;
              pc_366++;
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
  execute_369();
execute_366();
    }
  }
}