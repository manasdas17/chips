library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

entity STREAMS_VHDL_MODEL is

end entity STREAMS_VHDL_MODEL;

architecture RTL of STREAMS_VHDL_MODEL is


  --returns the greater of the two parameters
  function MAX(
    A : integer;
    B : integer) return integer is
  begin
    if A > B then
      return A;
    else
      return B;
    end if;
  end MAX;

  --returns a std_logic_vector sum of the two parameters
  function ADD(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), MAX(A'length, B'length) + 1) + 
      resize(signed(B), MAX(A'length, B'length) + 1));
    end ADD;

  --returns a std_logic_vector product of the two parameters
  function MUL(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      signed(A) *
      signed(B));
    end MUL;

  --returns a std_logic_vector difference of the two parameters
  function SUB(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), MAX(A'length, B'length) + 1) - 
      resize(signed(B), MAX(A'length, B'length) + 1));
  end SUB;

  --returns A shifted right (arithmetic) by A
  function SR(
    A  : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(shift_right(signed(A), to_integer(signed(B))));
  end SR;

  --returns A shifted left by B
  function SL(
    A  : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
        shift_left(
           resize(signed(A), A'length + (2**(B'length-1))-1),
           to_integer(signed(B))
       )
   );
  end SL;

  --returns bitwise and of A and B
  --(A and B are resized to the length of the larger first)
  function BAND(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) and
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));
  end BAND;

  --returns bitwise or of A and B
  --(A and B are resized to the length of the larger first)
  function BOR(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) or
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));
  end BOR;

  --returns bitwise xor of A and B
  --(A and B are resized to the length of the larger first)
  function BXOR(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) xor
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));
  end BXOR;

  --equality comparison of A and B
  --(A and B are resized to the length of the larger first)
  function EQ(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) =
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end EQ;

  --inequality comparison of A and B
  --(A and B are resized to the length of the larger first)
  function NE(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
    resize(signed(A), MAX(A'LENGTH, B'LENGTH)) /=
    resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end NE;

  --greater than comparison of A and B
  --(A and B are resized to the length of the larger first)
  function GT(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) >
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end GT;

  --greater than or equal comparison of A and B
  --(A and B are resized to the length of the larger first)
  function GE(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) >=
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end GE;

  --less than comparison of A and B
  --(A and B are resized to the length of the larger first)
  function LT(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) <
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end LT;

  --less than or equal comparison of A and B
  --(A and B are resized to the length of the larger first)
  function LE(
    A : std_logic_vector; 
    B : std_logic_vector) return std_logic_vector is
  begin
    if 
      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) <=
      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then
      return "1";
    else
      return "0";
    end if;
  end LE;

  --resize A to B bits
  function STD_RESIZE(
    A : std_logic_vector; 
    B : integer) return std_logic_vector is
  begin
    return std_logic_vector(
      resize(signed(A), B));
  end STD_RESIZE;

  --print a value
  procedure PRINT(
    A : std_logic_vector) is
    variable output_line : line;
  begin
    write(output_line, to_integer(signed(A)));
    writeline(output, output_line);
  end PRINT;

  type SWITCH_STATE_TYPE is (SWITCH_INPUT_SEL, SWITCH_INPUT, SWITCH_OUTPUT);
  type SPINNER_STATE_TYPE is (SPINNER_INPUT, SPINNER_OUTPUT, SPINNER_ACK);
  type STEPPER_STATE_TYPE is (STEPPER_INPUT, STEPPER_OUTPUT, STEPPER_ACK);
  type BINARY_STATE_TYPE is (BINARY_INPUT, BINARY_OUTPUT);
  type UNARY_STATE_TYPE is (UNARY_INPUT, UNARY_OUTPUT);
  type TEE_STATE_TYPE is (TEE_INPUT_A, TEE_WAIT_YZ, TEE_WAIT_Y, TEE_WAIT_Z);
  type DIVIDER_STATE_TYPE is (READ_A_B, DIVIDE_1, DIVIDE_2, WRITE_Z);
  type SERIAL_IN_STATE_TYPE is (IDLE, START, RX0, RX1, RX2, RX3, RX4, RX5, RX6, RX7, STOP, OUTPUT_DATA);
  type SERIAL_OUT_STATE_TYPE is (IDLE, START, WAIT_EN, TX0, TX1, TX2, TX3, TX4, TX5, TX6, TX7, STOP);
  type FORMATER_STATE_TYPE is (INPUT_A, SHIFT, OUTPUT_SIGN, OUTPUT_Z);

  signal CLK : std_logic;
  signal RST : std_logic;
  signal STREAM_25     : std_logic_vector(4 downto 0);
  signal STREAM_25_STB : std_logic;
  signal STREAM_25_ACK : std_logic;
  signal STREAM_25_BRK : std_logic;
  signal STREAM_25_SKP : std_logic;

  signal STATE_26      : BINARY_STATE_TYPE;
  signal STREAM_26     : std_logic_vector(0 downto 0);
  signal STREAM_26_STB : std_logic;
  signal STREAM_26_ACK : std_logic;
  signal STREAM_26_BRK : std_logic;
  signal STREAM_26_SKP : std_logic;

  signal STREAM_22     : std_logic_vector(1 downto 0);
  signal STREAM_22_STB : std_logic;
  signal STREAM_22_ACK : std_logic;
  signal STREAM_22_BRK : std_logic;
  signal STREAM_22_SKP : std_logic;

  signal STATE_23      : BINARY_STATE_TYPE;
  signal STREAM_23     : std_logic_vector(8 downto 0);
  signal STREAM_23_STB : std_logic;
  signal STREAM_23_ACK : std_logic;
  signal STREAM_23_BRK : std_logic;
  signal STREAM_23_SKP : std_logic;

  TYPE PROCESS_16_STATE_TYPE is (INSTRUCTION_20, INSTRUCTION_21, INSTRUCTION_24, INSTRUCTION_24_1);
  signal STATE_16 : PROCESS_16_STATE_TYPE;
  signal STREAM_17     : std_logic_vector(7 downto 0);
  signal STREAM_17_STB : std_logic;
  signal STREAM_17_ACK : std_logic;
  signal STREAM_18     : std_logic_vector(7 downto 0);
  signal STREAM_18_STB : std_logic;
  signal STREAM_18_ACK : std_logic;
  signal VARIABLE_19   : std_logic_vector(7 downto 0);

begin

  --internal clock generator
  process
  begin
    while True loop
      CLK <= '0';
      wait for 5 ns;
      CLK <= '1';
      wait for 5 ns;
    end loop;
    wait;
  end process;

  --internal reset generator
  process
  begin
    RST <= '1';
    wait for 20 ns;
    RST <= '0';
    wait;
  end process;

  --STREAM 25 Counter(0, 10, 1, 5)
  process
  begin
    wait until rising_edge(CLK);
    STREAM_25_STB <= '1';
    if STREAM_25_ACK = '1' then
      STREAM_25_STB <= '0';
      STREAM_25 <= STD_RESIZE(ADD(STREAM_25, "00001"), 5);
      if STREAM_25 = "01010" then
        STREAM_25 <= "00000";
      end if;
    end if;
    if RST = '1' then
      STREAM_25_STB <= '0';
      STREAM_25 <= "00000";
    end if;
  end process;
  STREAM_25_BRK <= '0';
  STREAM_25_SKP <= '0';

  --STREAM 26 Binary(18, 25, 'eq')
  process
  begin
    wait until rising_edge(CLK);
    case STATE_26 is
      when BINARY_INPUT =>
        if STREAM_18_STB = '1' and STREAM_25_STB = '1' then
          STREAM_18_ACK <= '1'; STREAM_25_ACK <= '1';
          STREAM_26 <= EQ(  STREAM_18, STREAM_25);
          STREAM_26_STB <= '1';
          STATE_26 <= BINARY_OUTPUT;
        end if;
      when BINARY_OUTPUT =>
        STREAM_18_ACK <= '0'; STREAM_25_ACK <= '0';
        if STREAM_26_ACK = '1' then
           STREAM_26_STB <= '0';
           STATE_26 <= BINARY_INPUT;
        end if;
     end case;
     if RST = '1' then
       STREAM_26_STB <= '0';
       STREAM_18_ACK <= '0';
       STREAM_25_ACK <= '0';
       STATE_26 <= BINARY_INPUT;
     end if;
  end process;
  STREAM_26_BRK <= '0';
  STREAM_26_SKP <= '0';

  --Asserter(26)
  process
  begin
    wait until rising_edge(CLK);
    STREAM_26_ACK <= '0';
    if STREAM_26_STB = '1' and STREAM_26_ACK = '0' then
      assert(STREAM_26 /= "0") severity failure;
      STREAM_26_ACK <= '1';
    end if;
  end process;

  --STREAM 22 Repeater(1, 2)
  STREAM_22 <= "01";
  process
  begin
    wait until rising_edge(CLK);
    STREAM_22_STB <= not STREAM_22_ACK;
  end process;
  STREAM_22_BRK <= '0';
  STREAM_22_SKP <= '0';

  --STREAM 23 Binary(17, 22, 'add')
  process
  begin
    wait until rising_edge(CLK);
    case STATE_23 is
      when BINARY_INPUT =>
        if STREAM_17_STB = '1' and STREAM_22_STB = '1' then
          STREAM_17_ACK <= '1'; STREAM_22_ACK <= '1';
          STREAM_23 <= ADD( STREAM_17, STREAM_22);
          STREAM_23_STB <= '1';
          STATE_23 <= BINARY_OUTPUT;
        end if;
      when BINARY_OUTPUT =>
        STREAM_17_ACK <= '0'; STREAM_22_ACK <= '0';
        if STREAM_23_ACK = '1' then
           STREAM_23_STB <= '0';
           STATE_23 <= BINARY_INPUT;
        end if;
     end case;
     if RST = '1' then
       STREAM_23_STB <= '0';
       STREAM_17_ACK <= '0';
       STREAM_22_ACK <= '0';
       STATE_23 <= BINARY_INPUT;
     end if;
  end process;
  STREAM_23_BRK <= '0';
  STREAM_23_SKP <= '0';

  process
  begin
    wait until rising_edge(CLK);
    case STATE_16 is
     when INSTRUCTION_20 =>
       STREAM_17 <= VARIABLE_19;
       STREAM_17_STB <= '1';
       if STREAM_17_ACK = '1' then
         STREAM_17_ACK <= '0';
         STATE_16 <= INSTRUCTION_21;
       end if;
     when INSTRUCTION_21 =>
       STREAM_18 <= VARIABLE_19;
       STREAM_18_STB <= '1';
       if STREAM_18_ACK = '1' then
         STREAM_18_ACK <= '0';
         STATE_16 <= INSTRUCTION_24;
       end if;
     when INSTRUCTION_24 =>
       VARIABLE_19 <= STD_RESIZE(STREAM_23, 8);
       if STREAM_23_STB = '1' then
         STREAM_23_ACK <= '1';
         STATE_16 <= INSTRUCTION_24_1;
       end if;
     when INSTRUCTION_24_1 =>
       STREAM_23_ACK <= '0';
       STATE_16 <= INSTRUCTION_24;
    end case;
    if RST = '1' then
      STATE_16 <= INSTRUCTION_20;
      STREAM_17_STB <= '0';
      STREAM_18_STB <= '0';
      STREAM_23_ACK <= '0';
      VARIABLE_19 <= "00000000";
    end if;
  end process;

end architecture RTL;