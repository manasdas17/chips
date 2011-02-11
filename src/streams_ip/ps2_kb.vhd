--+============================================================================+
--|                    *** PS/2 KEYBOARD DECODER ***                           |
--+============================================================================+
--| Filename         :PS2Keyboard.vhd                                          |
--| Project          :Python Streams                                           |
--| Version          :0.1                                                      |
--| Author           :Jonathan P Dawson                                        |
--| Created Date     :2006-04-14                                               |
--+============================================================================+
--| Description      :PS/2 keyboard decoder                                    |
--+============================================================================+
--| Dependencies     :Standard Libraries                                       |
--+============================================================================+
--| Revision History :                                                         |
--|                                                                            |
--| Date :2006-04-14                                                           |
--| Author :Jonathan P Dawson                                                  |
--| Modification: Created File                                                 |
--|                                                                            |
--| Date :2010-12-21                                                           |
--| Author :Jonathan P Dawson                                                  |
--| Modification: Modified for incorporation into Python Streams               |
--|                                                                            |
--+============================================================================+
--| Copyright (C) Jonathan P Dawson 2005                                       |
--+============================================================================+

library ieee;
use ieee.std_logic_1164.all;

entity PS2_KEYBOARD is
  port (
  CLK         : in  Std_logic;
  RST         : in  Std_logic;
  TIMER_1us   : in  Std_logic;
  TIMER_10us  : in  Std_logic;
  TIMER_100us : in  Std_logic;
  TIMER_1ms   : in  Std_logic;

  DATA        : out Std_logic_vector (7 downto 0);
  DATA_STB    : out Std_logic;
  DATA_ACK    : in  Std_logic;
  
  KD          : in  Std_logic;
  KC          : in  Std_logic);
end PS2_KEYBOARD;


architecture RTL of PS2_KEYBOARD is

  type STATETYPE is ( IDLE, RX7, RX6, RX5, 
  RX4, RX3, RX2, RX1, RX0, STOP, PARITY);
  type IF_STATETYPE is ( IDLE, SEND_DATA);
  signal STATE : STATETYPE;
  signal IF_STATE : IF_STATETYPE;
  signal RXCOMPLETE : Std_logic;
  signal LAST_KC, INT_KC, INT_KD, KC_DEL, KD_DEL, KC_DEL2, KD_DEL2 : Std_logic;
  signal INT_DATA : Std_logic_vector(7 downto 0);
  
begin
  
  --Double Register Inputs;
  --SAMPLE EVERY 10US;
  process
  begin
    wait until Rising_edge(CLK);
    KD_DEL <= KD;
    KC_DEL <= KC;
    KD_DEL2 <= KD_DEL;
    KC_DEL2 <= KC_DEL;
    if TIMER_10us = '1' then
      INT_KD <= KD_DEL2;
      INT_KC <= KC_DEL2;
    end if;
  end process;
  
  process
  begin
    wait until rising_edge(CLK);
    RXCOMPLETE <= '0';
    if TIMER_10us = '1' then
      --STORE LAST CLOCK VALUE
      LAST_KC <= INT_KC;
      --EXECUTE STATE MACHINE EACH TIME A CLOCK IS RECIEVED
      if LAST_KC = '1' and INT_KC = '0' then
        --RESET TIMEOUT EACH TIME A CLOCK IS RECIEVED
        case STATE is
          when IDLE =>
          if INT_KD = '0' then
            STATE <= RX0;
          end if;
          when RX0 =>
          INT_DATA(0) <= INT_KD;
          STATE <= RX1;
          when RX1 =>
          INT_DATA(1) <= INT_KD;
          STATE <= RX2;
          when RX2 =>
          INT_DATA(2) <= INT_KD;
          STATE <= RX3;
          when RX3 =>
          INT_DATA(3) <= INT_KD;
          STATE <= RX4;
          when RX4 =>
          INT_DATA(4) <= INT_KD;
          STATE <= RX5;
          when RX5 =>
          INT_DATA(5) <= INT_KD;
          STATE <= RX6;
          when RX6 =>
          INT_DATA(6) <= INT_KD;
          STATE <= RX7;
          when RX7 =>
          INT_DATA(7) <= INT_KD;
          STATE <= PARITY;
          when PARITY =>
          STATE <= STOP;
          when STOP =>
          STATE <= IDLE;
          if INT_KD = '1' then
            RXCOMPLETE <= '1';
          end if;
        end case;
      end if;
    end if;
  end process;
  
  --IMPLEMENT Python Stream INTERFACE
  process
  begin
    wait until rising_edge(CLK);

    case IF_STATE is
      when IDLE =>
        if RXCOMPLETE = '1' then
          IF_STATE <= SEND_DATA;
        end if;
      when SEND_DATA =>
        DATA <= INT_DATA;
        DATA_STB <= '1';
        if DATA_ACK = '1' then
          DATA_STB <= '0';
          IF_STATE <= IDLE;
        end if;
    end case;

    if RST = '1' then
      IF_STATE <= IDLE;
      DATA_STB <= '0';
    end if;
  end process;
  
end RTL;

--+============================================================================+
--|                  *** END OF PS/2 KEYBOARD DECODER ***                      |
--+============================================================================+
