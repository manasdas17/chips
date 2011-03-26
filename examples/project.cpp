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

void execute_17();
data_type get_stream_1();
data_type get_stream_0();
data_type get_stream_5();
data_type get_stream_2();
data_type get_stream_3();
data_type get_stream_4();
data_type get_stream_9();
data_type get_stream_6();
data_type get_stream_7();
data_type get_stream_8();
data_type get_stream_11();
data_type get_stream_10();
data_type get_stream_13();
data_type get_stream_12();
data_type get_stream_14();
void execute_18();
data_type get_stream_15();
void execute_16();

//response
ofstream outfile_17("resp_17.txt");
void execute_17()
{
  data_type data = get_stream_14();
  if(!data.stalled)
  {
     outfile_17 << data.value << endl;
  }
}

//lookup table
int lookup_1[2048] = 
{
4096,0,4076,0,4017,0,3920,0,3784,0,3612,0,3406,0,3166,0,2896,0,2598,0,2276,0,1931,0,1567,0,1189,0,799,0,401,0,0,0,-401,0,-799,0,-1189,0,-1567,0,-1931,0,-2276,0,-2598,0,-2896,0,-3166,0,-3406,0,-3612,0,-3784,0,-3920,0,-4017,0,-4076,0,-4096,0,-4076,0,-4017,0,-3920,0,-3784,0,-3612,0,-3406,0,-3166,0,-2896,0,-2598,0,-2276,0,-1931,0,-1567,0,-1189,0,-799,0,-401,0,0,0,401,0,799,0,1189,0,1567,0,1931,0,2276,0,2598,0,2896,0,3166,0,3406,0,3612,0,3784,0,3920,0,4017,0,4076,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
};
data_type get_stream_1()
{
  data_type data = get_stream_0();
  data.value = lookup_1[data.value];
  data.stalled = false;
  if(debug){
   cerr << 1 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_0 = 0;
data_type get_stream_0()
{
  data_type data;
  data.stalled = false;
  data.value = count_0;
  count_0 += 1;
  if (count_0 > 2047) count_0 = 0;
  if(debug){
   cerr << 0 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//array
int array_5[1024];
data_type get_stream_5()
{
  data_type data;
  data = get_stream_4();
  if(debug){
   cerr << 5 << " array " << data.value << " " << data.stalled << endl;
  }
  if (!data.stalled)
  {
    data.value = array_5[data.value];
  }
  return data;
}

data_type data_1_5 = {0, true};
data_type data_2_5 = {0, true};
void execute_5()
{
  if (data_1_5.stalled)
  {
    data_1_5 = get_stream_2();
  }
  if (data_2_5.stalled)
  {
    data_2_5 = get_stream_3();
  }
  if(!data_1_5.stalled && !data_2_5.stalled)
  {
    array_5[data_1_5.value] = data_2_5.value;
    data_1_5.stalled = true;
    data_2_5.stalled = true;
  }
}

//process output
data_type output_2 = {0, true};
data_type get_stream_2()
{
  data_type data = output_2;
  output_2.stalled = true;
  if(debug){
   cerr << 2 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_3 = {0, true};
data_type get_stream_3()
{
  data_type data = output_3;
  output_3.stalled = true;
  if(debug){
   cerr << 3 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_4 = {0, true};
data_type get_stream_4()
{
  data_type data = output_4;
  output_4.stalled = true;
  if(debug){
   cerr << 4 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//array
int array_9[1024];
data_type get_stream_9()
{
  data_type data;
  data = get_stream_8();
  if(debug){
   cerr << 9 << " array " << data.value << " " << data.stalled << endl;
  }
  if (!data.stalled)
  {
    data.value = array_9[data.value];
  }
  return data;
}

data_type data_1_9 = {0, true};
data_type data_2_9 = {0, true};
void execute_9()
{
  if (data_1_9.stalled)
  {
    data_1_9 = get_stream_6();
  }
  if (data_2_9.stalled)
  {
    data_2_9 = get_stream_7();
  }
  if(!data_1_9.stalled && !data_2_9.stalled)
  {
    array_9[data_1_9.value] = data_2_9.value;
    data_1_9.stalled = true;
    data_2_9.stalled = true;
  }
}

//process output
data_type output_6 = {0, true};
data_type get_stream_6()
{
  data_type data = output_6;
  output_6.stalled = true;
  if(debug){
   cerr << 6 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_7 = {0, true};
data_type get_stream_7()
{
  data_type data = output_7;
  output_7.stalled = true;
  if(debug){
   cerr << 7 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_8 = {0, true};
data_type get_stream_8()
{
  data_type data = output_8;
  output_8.stalled = true;
  if(debug){
   cerr << 8 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//lookup table
int lookup_11[10] = 
{
-4096,0,2896,3784,4017,4076,4091,4095,4096,4096
};
data_type get_stream_11()
{
  data_type data = get_stream_10();
  data.value = lookup_11[data.value];
  data.stalled = false;
  if(debug){
   cerr << 11 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_10 = 0;
data_type get_stream_10()
{
  data_type data;
  data.stalled = false;
  data.value = count_10;
  count_10 += 1;
  if (count_10 > 9) count_10 = 0;
  if(debug){
   cerr << 10 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//lookup table
int lookup_13[10] = 
{
0,-4096,-2896,-1567,-799,-401,-201,-101,-50,-25
};
data_type get_stream_13()
{
  data_type data = get_stream_12();
  data.value = lookup_13[data.value];
  data.stalled = false;
  if(debug){
   cerr << 13 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_12 = 0;
data_type get_stream_12()
{
  data_type data;
  data.stalled = false;
  data.value = count_12;
  count_12 += 1;
  if (count_12 > 9) count_12 = 0;
  if(debug){
   cerr << 12 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type output_14 = {0, true};
data_type get_stream_14()
{
  data_type data = output_14;
  output_14.stalled = true;
  if(debug){
   cerr << 14 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//response
ofstream outfile_18("resp_18.txt");
void execute_18()
{
  data_type data = get_stream_15();
  if(!data.stalled)
  {
     outfile_18 << data.value << endl;
  }
}

//process output
data_type output_15 = {0, true};
data_type get_stream_15()
{
  data_type data = output_15;
  output_15.stalled = true;
  if(debug){
   cerr << 15 << " process output " << data.value << " " << data.stalled << endl;
  }
  return data;
}

const int OP_DIV_16 = 0;
const int OP_MOD_16 = 1;
const int OP_MUL_16 = 2;
const int OP_ADD_16 = 3;
const int OP_SUB_16 = 4;
const int OP_BAND_16 = 5;
const int OP_BOR_16 = 6;
const int OP_BXOR_16 = 7;
const int OP_SL_16 = 8;
const int OP_SR_16 = 9;
const int OP_EQ_16 = 10;
const int OP_NE_16 = 11;
const int OP_GE_16 = 12;
const int OP_GT_16 = 13;
const int OP_WAIT_US_16 = 14;
const int OP_JMP_16 = 15;
const int OP_JMPF_16 = 16;
const int OP_MOVE_16 = 17;
const int OP_IMM_16 = 18;
const int OP_READ_1_16 = 19;
const int OP_READ_5_16 = 20;
const int OP_READ_9_16 = 21;
const int OP_READ_11_16 = 22;
const int OP_READ_13_16 = 23;
const int OP_WRITE_2_16 = 24;
const int OP_WRITE_3_16 = 25;
const int OP_WRITE_6_16 = 26;
const int OP_WRITE_7_16 = 27;
const int OP_WRITE_4_16 = 28;
const int OP_WRITE_8_16 = 29;
const int OP_WRITE_14_16 = 30;
const int OP_WRITE_15_16 = 31;
struct instruction_type_16 
{
  int operation;
  int srca;
  int srcb;
  int immediate;
};

instruction_type_16 instructions_16 [357] = 
{
  {OP_IMM_16, 1, 0, 0}, //file: ./example_6_fft.py line: 56
  {OP_IMM_16, 2, 0, 0}, //file: ./example_6_fft.py line: 58
  {OP_IMM_16, 3, 0, 0}, //file: ./example_6_fft.py line: 64
  {OP_IMM_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_IMM_16, 5, 0, 0}, //file: ./example_6_fft.py line: 65
  {OP_IMM_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_IMM_16, 7, 0, 0}, //file: ./example_6_fft.py line: 61
  {OP_IMM_16, 8, 0, 0}, //file: ./example_6_fft.py line: 60
  {OP_IMM_16, 9, 0, 0}, //file: ./example_6_fft.py line: 62
  {OP_IMM_16, 10, 0, 0}, //file: ./example_6_fft.py line: 63
  {OP_IMM_16, 11, 0, 0}, //file: ./example_6_fft.py line: 68
  {OP_IMM_16, 12, 0, 0}, //file: ./example_6_fft.py line: 69
  {OP_IMM_16, 13, 0, 0}, //file: ./example_6_fft.py line: 70
  {OP_IMM_16, 14, 0, 0}, //file: ./example_6_fft.py line: 71
  {OP_IMM_16, 15, 0, 0}, //file: ./example_6_fft.py line: 59
  {OP_IMM_16, 16, 0, 0}, //file: ./example_6_fft.py line: 57
  {OP_IMM_16, 17, 0, 0}, //file: ./example_6_fft.py line: 66
  {OP_IMM_16, 18, 0, 0}, //file: ./example_6_fft.py line: 67
  {OP_IMM_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1024}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GT_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 138
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 28}, //file: None line: None
  {OP_JMP_16, 0, 0, 43}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 28}, //file: None line: None
  {OP_READ_1_16, 2, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_2_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_3_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_1_16, 2, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_6_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_7_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 20}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_IMM_16, 19, 0, 512}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1022}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GE_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 55}, //file: None line: None
  {OP_JMP_16, 0, 0, 132}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 55}, //file: None line: None
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GT_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 138
  {OP_JMPF_16, 19, 0, 104}, //file: None line: None
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_4_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_5_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 65}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 3, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_8_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_9_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 73}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 5, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_2_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_4_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_5_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 83}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_WRITE_3_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_6_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_8_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_9_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 93}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_WRITE_7_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_2_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 3, 0}, //file: ./example_6_fft.py line: 64
  {OP_WRITE_3_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_6_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 5, 0}, //file: ./example_6_fft.py line: 65
  {OP_WRITE_7_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_JMP_16, 0, 0, 104}, //file: None line: None
  {OP_IMM_16, 19, 0, 512}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 7, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_MOVE_16, 20, 7, 0}, //file: ./example_6_fft.py line: 61
  {OP_GE_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 114}, //file: None line: None
  {OP_JMP_16, 0, 0, 123}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 114}, //file: None line: None
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_MOVE_16, 20, 7, 0}, //file: ./example_6_fft.py line: 61
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 7, 0}, //file: ./example_6_fft.py line: 61
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 7, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 106}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_MOVE_16, 20, 7, 0}, //file: ./example_6_fft.py line: 61
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 47}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_IMM_16, 19, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 8, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 10}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 8, 0}, //file: ./example_6_fft.py line: 60
  {OP_GE_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 142}, //file: None line: None
  {OP_JMP_16, 0, 0, 305}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 142}, //file: None line: None
  {OP_IMM_16, 19, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 8, 0}, //file: ./example_6_fft.py line: 60
  {OP_SL_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 149
  {OP_MOVE_16, 9, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 9, 0}, //file: ./example_6_fft.py line: 62
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 10, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 4096}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 11, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 12, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_READ_11_16, 13, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_READ_13_16, 14, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_IMM_16, 19, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 10, 0}, //file: ./example_6_fft.py line: 63
  {OP_MOVE_16, 20, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_GE_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 166}, //file: None line: None
  {OP_JMP_16, 0, 0, 300}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 166}, //file: None line: None
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_MOVE_16, 15, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 15, 0}, //file: ./example_6_fft.py line: 59
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1023}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GE_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 139
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 180}, //file: None line: None
  {OP_JMP_16, 0, 0, 269}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 180}, //file: None line: None
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_MOVE_16, 20, 10, 0}, //file: ./example_6_fft.py line: 63
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 16, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 16, 0}, //file: ./example_6_fft.py line: 57
  {OP_WRITE_4_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_5_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 190}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 17, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 16, 0}, //file: ./example_6_fft.py line: 57
  {OP_WRITE_8_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_9_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 198}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 18, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 17, 0}, //file: ./example_6_fft.py line: 66
  {OP_MOVE_16, 20, 11, 0}, //file: ./example_6_fft.py line: 68
  {OP_MUL_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 20, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 20, 18, 0}, //file: ./example_6_fft.py line: 67
  {OP_MOVE_16, 21, 12, 0}, //file: ./example_6_fft.py line: 69
  {OP_MUL_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 21, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_MOVE_16, 3, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 17, 0}, //file: ./example_6_fft.py line: 66
  {OP_MOVE_16, 20, 12, 0}, //file: ./example_6_fft.py line: 69
  {OP_MUL_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 20, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 20, 18, 0}, //file: ./example_6_fft.py line: 67
  {OP_MOVE_16, 21, 11, 0}, //file: ./example_6_fft.py line: 68
  {OP_MUL_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 21, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 5, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_4_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_5_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 230}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 17, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_8_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_9_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 238}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 18, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 16, 0}, //file: ./example_6_fft.py line: 57
  {OP_WRITE_2_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 17, 0}, //file: ./example_6_fft.py line: 66
  {OP_MOVE_16, 20, 3, 0}, //file: ./example_6_fft.py line: 64
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_WRITE_3_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 16, 0}, //file: ./example_6_fft.py line: 57
  {OP_WRITE_6_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 18, 0}, //file: ./example_6_fft.py line: 67
  {OP_MOVE_16, 20, 5, 0}, //file: ./example_6_fft.py line: 65
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_WRITE_7_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_2_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 17, 0}, //file: ./example_6_fft.py line: 66
  {OP_MOVE_16, 20, 3, 0}, //file: ./example_6_fft.py line: 64
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_WRITE_3_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_6_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 18, 0}, //file: ./example_6_fft.py line: 67
  {OP_MOVE_16, 20, 5, 0}, //file: ./example_6_fft.py line: 65
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_WRITE_7_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_MOVE_16, 20, 9, 0}, //file: ./example_6_fft.py line: 62
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 172}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_MOVE_16, 19, 11, 0}, //file: ./example_6_fft.py line: 68
  {OP_MOVE_16, 3, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 3, 0}, //file: ./example_6_fft.py line: 64
  {OP_MOVE_16, 20, 13, 0}, //file: ./example_6_fft.py line: 70
  {OP_MUL_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 20, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 20, 12, 0}, //file: ./example_6_fft.py line: 69
  {OP_MOVE_16, 21, 14, 0}, //file: ./example_6_fft.py line: 71
  {OP_MUL_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 21, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_SUB_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 125
  {OP_MOVE_16, 11, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 3, 0}, //file: ./example_6_fft.py line: 64
  {OP_MOVE_16, 20, 14, 0}, //file: ./example_6_fft.py line: 71
  {OP_MUL_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 20, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_MOVE_16, 20, 12, 0}, //file: ./example_6_fft.py line: 69
  {OP_MOVE_16, 21, 13, 0}, //file: ./example_6_fft.py line: 70
  {OP_MUL_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 126
  {OP_IMM_16, 21, 0, 12}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_SR_16, 20, 21, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 132
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 12, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 158}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_MOVE_16, 19, 8, 0}, //file: ./example_6_fft.py line: 60
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 8, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 134}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_IMM_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1024}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GT_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 138
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 315}, //file: None line: None
  {OP_JMP_16, 0, 0, 330}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 315}, //file: None line: None
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_4_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_5_16, 4, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 4, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 321}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_14_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 307}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_IMM_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_IMM_16, 19, 0, 1024}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_MOVE_16, 20, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_GT_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 138
  {OP_IMM_16, 20, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_EQ_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 134
  {OP_JMPF_16, 19, 0, 340}, //file: None line: None
  {OP_JMP_16, 0, 0, 355}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 62
  {OP_JMP_16, 0, 0, 340}, //file: None line: None
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_WRITE_8_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_READ_9_16, 6, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 151
  {OP_MOVE_16, 19, 6, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 188
  {OP_MOVE_16, 0, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_JMP_16, 0, 0, 346}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 199
  {OP_MOVE_16, 2, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_MOVE_16, 19, 2, 0}, //file: ./example_6_fft.py line: 58
  {OP_WRITE_15_16, 19, 0, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/streams.py line: 374
  {OP_MOVE_16, 19, 1, 0}, //file: ./example_6_fft.py line: 56
  {OP_IMM_16, 20, 0, 1}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 119
  {OP_ADD_16, 19, 20, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 124
  {OP_MOVE_16, 1, 19, 0}, //file: /usr/local/lib/python2.6/dist-packages/streams/instruction.py line: 274
  {OP_JMP_16, 0, 0, 332}, //file: /usr/local/lib/python2.6/dist-packages/streams/__init__.py line: 63
  {OP_JMP_16, 0, 0, 355}, //file: None line: None
  {OP_JMP_16, 0, 0, 0} //file: None line: None
};

//Process

int pc_16 = 0;
int registers_16[32];

void execute_16()
{
    instruction_type_16 instruction = instructions_16[pc_16];
    data_type data;
    int result = 0;
    int rega = registers_16[instruction.srca];
    int regb = registers_16[instruction.srcb];
    switch(instruction.operation)
    {
        case OP_DIV_16:
            result = resize(rega/regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_MOD_16:
            result = resize(rega%regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_MUL_16:
            result = resize(rega*regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_ADD_16:
            result = resize(rega+regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_SUB_16:
            result = resize(rega-regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_BAND_16:
            result = resize(rega&regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_BOR_16:
            result = resize(rega|regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_BXOR_16:
            result = resize(rega^regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_SL_16:
            result = resize(rega<<regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_SR_16:
            result = resize(rega>>regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_EQ_16:
            result = -resize(rega==regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_NE_16:
            result = -resize(rega!=regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_GE_16:
            result = -resize(rega>=regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_GT_16:
            result = -resize(rega>regb, 30); 
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_WAIT_US_16:
            break;
        case OP_JMP_16:
            pc_16 = instruction.immediate;
            break;
        case OP_JMPF_16:
            if (rega==0)
            {
              pc_16 = instruction.immediate;
            }
            else
            {
              pc_16++;
            }
            registers_16[instruction.srca] = result;
            break;
        case OP_MOVE_16:
            result = regb;
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
        case OP_IMM_16:
            result = instruction.immediate;
            pc_16++;
            registers_16[instruction.srca] = result;
            break;
          case OP_READ_1_16:
            data = get_stream_1();
            if (!data.stalled)
            {
              registers_16[instruction.srca] = data.value;
              pc_16++;
            }
            break;
          case OP_READ_5_16:
            data = get_stream_5();
            if (!data.stalled)
            {
              registers_16[instruction.srca] = data.value;
              pc_16++;
            }
            break;
          case OP_READ_9_16:
            data = get_stream_9();
            if (!data.stalled)
            {
              registers_16[instruction.srca] = data.value;
              pc_16++;
            }
            break;
          case OP_READ_11_16:
            data = get_stream_11();
            if (!data.stalled)
            {
              registers_16[instruction.srca] = data.value;
              pc_16++;
            }
            break;
          case OP_READ_13_16:
            data = get_stream_13();
            if (!data.stalled)
            {
              registers_16[instruction.srca] = data.value;
              pc_16++;
            }
            break;
          case OP_WRITE_2_16:
            if (output_2.stalled)
            {
              output_2.stalled = false;
              output_2.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_3_16:
            if (output_3.stalled)
            {
              output_3.stalled = false;
              output_3.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_6_16:
            if (output_6.stalled)
            {
              output_6.stalled = false;
              output_6.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_7_16:
            if (output_7.stalled)
            {
              output_7.stalled = false;
              output_7.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_4_16:
            if (output_4.stalled)
            {
              output_4.stalled = false;
              output_4.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_8_16:
            if (output_8.stalled)
            {
              output_8.stalled = false;
              output_8.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_14_16:
            if (output_14.stalled)
            {
              output_14.stalled = false;
              output_14.value = rega;
              pc_16++;
            }
            break;
          case OP_WRITE_15_16:
            if (output_15.stalled)
            {
              output_15.stalled = false;
              output_15.value = rega;
              pc_16++;
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
  execute_17();
execute_5();
  execute_5();
execute_9();
  execute_9();
  execute_18();
execute_16();
    }
  }
}