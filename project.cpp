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

void execute_156();
data_type get_stream_155();
data_type get_stream_151();
data_type get_stream_150();
data_type get_stream_152();
data_type get_stream_154();

//asserter
void execute_156()
{
  assert(get_stream_155().value);
}

//binary
data_type get_stream_155()
{
  data_type data;
  data_type a = get_stream_152();
  data_type b = get_stream_154();
  data.value = resize((a.value == b.value), 1);
  data.stalled = a.stalled || b.stalled;
  if(debug){
   cerr << 155 << " binary " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//lookup table
int lookup_151[3] = 
{
49,48,10
};
data_type get_stream_151()
{
  data_type data = get_stream_150();
  data.value = lookup_151[data.value];
  data.stalled = false;
  if(debug){
   cerr << 151 << " lookup " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//counter
int count_150 = 0;
data_type get_stream_150()
{
  data_type data;
  data.stalled = false;
  data.value = count_150;
  count_150 += 1;
  if (count_150 > 2) count_150 = 0;
  if(debug){
   cerr << 150 << " counter " << data.value << " " << data.stalled << endl;
  }
  return data;
}

//process output
data_type get_stream_152()
{
  return 0;
}

//repeater
data_type get_stream_154()
{
  data_type data =
  {
    10,
    false
  };
  if(debug){
   cerr << 154 << " repeater " << data.value << " " << data.stalled << endl;
  }
  return data;
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
  execute_156();
    }
  }
}
