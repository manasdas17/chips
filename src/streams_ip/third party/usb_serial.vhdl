--
--  USB 2.0 Default control endpoint
--
--  This entity implements the minimal required functionality of
--  the default control endpoint.
--
--  The low-level interface signals are named T_xxx and should be conditionally
--  connected to the usb_transact interface in the following way:
--    * Always connect output signal C_ADDR to T_ADDR;
--    * Always connect input signals T_FIN, T_OSYNC, T_RXRDY, T_RXDAT, T_TXRDY;
--    * If T_ENDPT = 0, connect input signals T_IN, T_OUT, T_SETUP, T_PING;
--      otherwise pull these inputs to zero.
--    * If T_ENDPT = 0, connect output signals T_NAK, T_STALL, T_NYET, T_SEND,
--      T_ISYNC, T_TXDAT; otherwise another endpoint should drive these.
--    * If T_ENDPT = 0 and C_DSCBUSY = 0, connect output signal T_TXDAT;
--      otherwise if T_ENDPT = 0 and C_DSCBUSY = 1, drive T_TXDAT
--      from descriptor memory;
--      otherwise another endpoint drives T_TXDAT.
--
--  A device descriptor and a configuration descriptor must be provided
--  in external memory. If high speed mode is supported, an other-speed
--  device qualifier and other-speed configuration descriptor must also
--  be provided. In addition, string descriptors may optionally be provided.
--  Each descriptor may be at most 255 bytes long.
--  A maximum packet size of 64 bytes is assumed for control transfers.
--
--  This entity uses the following protocol to access descriptor data:
--    * When C_DSCBUSY is high, the entity is accessing descriptor data.
--      A descriptor is selected by signals C_DSCTYP and C_DSCINX;
--      a byte within this descriptor is selected by signal C_DSCOFF.
--    * Based on C_DSCTYP and C_DSCINX, the application must assign
--      the length of the selected descriptor to C_DSCLEN. If the selected
--      descriptor does not exist, the application must set C_DSCLEN to zero.
--      C_DSCLEN must be valid one clock after rising C_DSCBUSY and must
--      remain stable as long as C_DSCBUSY, C_DSCTYP and C_DSCINX remain
--      unchanged.
--    * When C_DSCRD is asserted, the application must put the selected
--      byte from the selected descriptor on T_TXDAT towards usb_transact.
--      The application must respond in the first clock cycle following
--      assertion of C_DSCRD.
--    * When C_DSCRD is not asserted, but C_DSCBUSY is still high, 
--      the application must keep T_TXDAT unchanged. Changes to C_DSCOFF
--      must not affect T_TXDAT while C_DSCRD is low.
--
--  The standard device requests are handled as follows:
--
--    Clear Feature:
--      When clearing the ENDPOINT_HALT feature, reset the endpoint's
--      sync bits (as required by spec). Otherwise ignore but report
--      success status.
--      BAD: should return STALL when referring to invalid endpoint/interface.
--
--    Get Configuration:
--      Return 1 if configured, 0 if not configured.
--
--    Get Descriptor:
--      Handled by application through descriptor data interface as
--      described above.
--
--    Get Interface:
--      Always return zero byte.
--      BAD: should return STALL when referring to invalid endpoint/interface.
--
--    Get Status:
--      Return device status / endpoint status / zero.
--      BAD: should return STALL when referring to invalid endpoint/interface.
--
--    Set Address:
--      Store new address.
--
--    Set Configuration:
--      Switch between Configured and Address states; clear all endpoint
--      sync bits (as required by spec). Accepts only configuration values
--      0 and 1.
--
--    Set Descriptor:
--      Not implemented; returns STALL. (Correct; request is optional.)
--
--    Set Feature:
--      Only ENDPOINT_HALT feature implemented; otherwise returns STALL.
--      BAD: every high speed device must support TEST_MODE.
--
--    Set Interface:
--      Not implemented; returns STALL.
--      (Correct; request is optional if no interfaces have alternate settings.)
--
--    Synch Frame:
--      Not implemented; returns STALL.
--      (Correct, assuming no isosynchronous endpoints.)
--
--  Non-standard requests are silently ignored but return success status.
--  This is incorrect, but necessary to get host software to accept usb_serial
--  as CDC-ACM device.
--

library ieee;
use ieee.std_logic_1164.all, ieee.numeric_std.all;

entity usb_control is

    generic (

        -- Highest endpoint number in use.
        NENDPT : integer range 1 to 15 );

    port (

        -- 60 MHz UTMI clock.
        CLK :           in  std_logic;

        -- Synchronous reset of this entity.
        RESET :         in  std_logic;

        -- Current device address.
        C_ADDR :        out std_logic_vector(6 downto 0);

        -- High when in Configured state.
        C_CONFD :       out std_logic;

        -- Trigger clearing of sync/halt bits for IN endpoint.
        C_CLRIN :       out std_logic_vector(1 to NENDPT);

        -- Trigger clearing of sync/halt bits for OUT endpoint.
        C_CLROUT :      out std_logic_vector(1 to NENDPT);

         -- Current status of halt bit for IN endpoints.
        C_HLTIN :       in  std_logic_vector(1 to NENDPT);

        -- Current status of halt bit for IN endpoints.
        C_HLTOUT :      in  std_logic_vector(1 to NENDPT);

        -- Trigger setting of halt bit for IN endpoints.
        C_SHLTIN :      out std_logic_vector(1 to NENDPT);

        -- Trigger setting of halt bit for OUT endpoints.
        C_SHLTOUT :     out std_logic_vector(1 to NENDPT);

        -- High when accessing descriptor memory.
        -- Note that C_DSCBUSY may go low in between packets of a single descriptor.
        C_DSCBUSY :     out std_logic;

        -- Descriptor read enable. Asserted to request a descriptor byte;
        -- in the next clock cycle, the application must update T_TXDAT.
        C_DSCRD :       out std_logic;

        -- LSB bits of the requested descriptor type. Valid when C_DSCBUSY is high.
        C_DSCTYP :      out std_logic_vector(2 downto 0);

        -- Requested descriptor index. Valid when C_DSCBUSY is high.
        C_DSCINX :      out std_logic_vector(7 downto 0);

        -- Offset within requested descriptor. Valid when C_DSCBUSY and C_DSCRD are high.
        C_DSCOFF :      out std_logic_vector(7 downto 0);

        -- Set to length of current descriptor by application.
        C_DSCLEN :      in  std_logic_vector(7 downto 0);

        -- High if the device is not drawing bus power.
        C_SELFPOWERED : in  std_logic;

        -- Connect to T_IN from usb_transact when T_ENDPT = 0, otherwise pull to 0.
        T_IN :          in  std_logic;

        -- Connect to T_OUT from usb_transact when T_ENDPT = 0, otherwise pull to 0.
        T_OUT :         in  std_logic;

        -- Connect to T_SETUP from usb_transact when T_ENDPT = 0, otherwise pull to 0.
        T_SETUP :       in  std_logic;

        -- Connect to T_PING from usb_transact when T_ENDPT = 0, otherwise pull to 0.
        T_PING :        in  std_logic;

        -- Connect to T_FIN from ubs_transact.
        T_FIN :         in  std_logic;

        -- Connect to T_NAK towards usb_transact when T_ENDPT = 0.
        T_NAK :         out std_logic;

        -- Connect to T_STALL towards usb_transact when T_ENDPT = 0.
        T_STALL :       out std_logic;

        -- Connect to T_NYET towards usb_transact when T_ENDPT = 0.
        T_NYET :        out std_logic;

        -- Connect to T_SEND towards usb_transact when T_ENDPT = 0.
        T_SEND :        out std_logic;

        -- Connect to T_ISYNC towards usb_transact when T_ENDPT = 0.
        T_ISYNC :       out std_logic;

        -- Connect to T_OSYNC from usb_transact.
        T_OSYNC :       in  std_logic;

        -- Connect to T_RXRDY from usb_transact.
        T_RXRDY :       in  std_logic;

        -- Connect to T_RXDAT from usb_transact.
        T_RXDAT :       in  std_logic_vector(7 downto 0);

        -- Connect to T_TXRDY from usb_transact.
        T_TXRDY :       in  std_logic;

        -- Connect to T_TXDAT towards usb_transact when T_ENDPT = 0 and C_DSCBUSY = '0'.
        T_TXDAT :       out std_logic_vector(7 downto 0) );

end entity usb_control;

architecture usb_control_arch of usb_control is

    -- Constants for control request
    constant req_getstatus :    std_logic_vector(3 downto 0) := "0000";
    constant req_clearfeature : std_logic_vector(3 downto 0) := "0001";
    constant req_setfeature :   std_logic_vector(3 downto 0) := "0011";
    constant req_setaddress :   std_logic_vector(3 downto 0) := "0101";
    constant req_getdesc :      std_logic_vector(3 downto 0) := "0110";
    constant req_getconf :      std_logic_vector(3 downto 0) := "1000";
    constant req_setconf :      std_logic_vector(3 downto 0) := "1001";
    constant req_getiface :     std_logic_vector(3 downto 0) := "1010";

    -- State machine
    type t_state is (
      ST_IDLE, ST_STALL,
      ST_SETUP, ST_SETUPERR, ST_NONSTANDARD, ST_ENDSETUP, ST_WAITIN,
      ST_SENDRESP, ST_STARTDESC, ST_SENDDESC, ST_DONESEND );
    signal s_state : t_state := ST_IDLE;

    -- Current control request
    signal s_ctlrequest :   std_logic_vector(3 downto 0);
    signal s_ctlparam :     std_logic_vector(7 downto 0);
    signal s_desctyp :      std_logic_vector(2 downto 0);
    signal s_answerlen :    unsigned(7 downto 0);
    signal s_sendbyte :     std_logic_vector(7 downto 0) := "00000000";

    -- Device state
    signal s_addr :         std_logic_vector(6 downto 0) := "0000000";
    signal s_confd :        std_logic := '0';

    -- Counters
    signal s_setupptr :     unsigned(2 downto 0);
    signal s_answerptr :    unsigned(7 downto 0);

begin

    -- Status signals
    C_ADDR <= s_addr;
    C_CONFD <= s_confd;

    -- Memory interface
    C_DSCBUSY   <= T_IN when (s_state = ST_WAITIN) else
                   '1' when (s_state = ST_STARTDESC or s_state = ST_SENDDESC) else
	           '0';
    C_DSCRD     <= '1' when (s_state = ST_STARTDESC) else T_TXRDY;
    C_DSCTYP    <= s_desctyp;
    C_DSCINX    <= s_ctlparam;
    C_DSCOFF    <= std_logic_vector(s_answerptr);

    -- Transaction interface
    T_NAK   <= '0';
    T_STALL <= '1' when (s_state = ST_STALL) else '0';  
    T_NYET  <= '0';
    T_SEND  <= '1' when ((s_state = ST_SENDRESP) or (s_state = ST_SENDDESC))
	       else '0';
    T_ISYNC <= not std_logic(s_answerptr(6));
    T_TXDAT <= s_sendbyte;

    -- On every rising clock edge
    process is
    begin
        wait until rising_edge(CLK);

        -- Set endpoint reset/halt lines to zero by default
        C_CLRIN   <= (others => '0');
        C_CLROUT  <= (others => '0');
        C_SHLTIN  <= (others => '0');
        C_SHLTOUT <= (others => '0');

        -- State machine
        if RESET = '1' then

            -- Reset this entity
            s_state <= ST_IDLE;
            s_addr  <= "0000000";
            s_confd <= '0';

            -- Trigger endpoint reset lines
            C_CLRIN  <= (others => '1');
            C_CLROUT <= (others => '1');

        else

            case s_state is

                when ST_IDLE =>
                    -- Idle; wait for SETUP transaction;
                    -- OUT transactions are ignored but acknowledged;
                    -- IN transactions send an empty packet.
                    s_answerptr <= to_unsigned(0, s_answerptr'length);
                    if T_SETUP = '1' then
                        -- Start of SETUP transaction
                        s_state <= ST_SETUP;
                        s_setupptr <= to_unsigned(0, s_setupptr'length);
                    end if;

                when ST_STALL =>
                    -- Stalled; wait for next SETUP transaction;
                    -- respond to IN/OUT transactions with a STALL handshake.
                    if T_SETUP = '1' then
                        -- Start of SETUP transaction
                        s_state <= ST_SETUP;
                        s_setupptr <= to_unsigned(0, s_setupptr'length);
                    end if;

                when ST_SETUP =>
                    -- In SETUP transaction; parse request structure.
                    s_answerptr <= to_unsigned(0, s_answerptr'length);
                    if T_RXRDY = '1' then
                        -- Process next request byte
                        case s_setupptr is
                            when "000" =>
                                -- bmRequestType
                                s_ctlparam <= T_RXDAT;
                                if T_RXDAT(6 downto 5) /= "00" then
                                    -- non-standard device request
                                    s_state <= ST_NONSTANDARD;
                                end if;
                            when "001" =>
                                -- bRequest
                                s_ctlrequest <= T_RXDAT(3 downto 0);
                                if T_RXDAT(7 downto 4) /= "0000" then
                                    -- Unknown request
                                    s_state <= ST_SETUPERR;
                                end if;
                            when "010" =>
                                -- wValue lsb
                                if s_ctlrequest /= req_getstatus then
                                    s_ctlparam <= T_RXDAT;
                                end if;
                            when "011" =>
                                -- wValue msb
                                if s_ctlrequest = req_getdesc then
                                    if T_RXDAT(7 downto 3) /= "00000" then
                                        -- Unsupported descriptor type
                                        s_state <= ST_SETUPERR;
                                    end if;
                                end if;
                                -- Store descriptor type (assuming GET_DESCRIPTOR request)
                                s_desctyp <= T_RXDAT(2 downto 0);
                            when "100" =>
                                -- wIndex lsb
                                case s_ctlrequest is
                                    when req_clearfeature =>
                                        if s_ctlparam = "00000000" then
                                            -- Clear ENDPOINT_HALT feature;
                                            -- store endpoint selector
                                            s_ctlparam <= T_RXDAT;
                                        else
                                            -- Unknown clear feature request
                                            s_ctlparam <= "00000000";
                                        end if;
                                    when req_setfeature => 
                                        if s_ctlparam = "00000000" then
                                            -- Set ENDPOINT_HALT feature;
                                            -- store endpoint selector
                                            s_ctlparam <= T_RXDAT;
                                        else
                                            -- Unsupported set feature request
                                            s_state <= ST_SETUPERR;
                                        end if;
                                    when req_getstatus =>
                                        if s_ctlparam(1 downto 0) = "00" then
                                            -- Get device status
                                            s_sendbyte <= "0000000" & C_SELFPOWERED;
                                            s_ctlparam <= "00000000";
                                        elsif s_ctlparam(1 downto 0) = "10" then
                                            -- Get endpoint status
                                            s_sendbyte <= "00000000";
                                            s_ctlparam <= T_RXDAT;
                                        else
                                            -- Probably get interface status
                                            s_sendbyte <= "00000000";
                                            s_ctlparam <= "00000000";
                                        end if;
                                    when others =>
                                        -- Don't care about index.
                                end case;
                            when "101" =>
                                -- wIndex msb; don't care
                            when "110" =>
                                -- wLength lsb
                                s_answerlen <= unsigned(T_RXDAT);
                            when "111" =>
                                -- wLength msb
                                if T_RXDAT /= "00000000" then
                                    s_answerlen <= "11111111";
                                end if;
                                s_state <= ST_ENDSETUP;
                            when others =>
                                -- Impossible
                        end case;
                        -- Increment position within SETUP packet
                        s_setupptr <= s_setupptr + 1;
                    elsif T_FIN = '1' then
                        -- Got short SETUP packet; answer with STALL status.
                        s_state <= ST_STALL;
                    elsif T_SETUP = '0' then
                        -- Got corrupt SETUP packet; ignore.
                        s_state <= ST_IDLE;
                    end if;

		when ST_SETUPERR =>
                    -- In SETUP transaction; got request error
                    if T_FIN = '1' then
                        -- Got good SETUP packet that causes request error
                        s_state <= ST_STALL;
                    elsif T_SETUP = '0' then
                        -- Got corrupt SETUP packet; ignore
                        s_state <= ST_IDLE;
                    end if;

                when ST_NONSTANDARD =>
                    -- Ignore non-standard requests
                    if T_SETUP = '0' then
                        s_state <= ST_IDLE;
                    end if;

                when ST_ENDSETUP =>
                    -- Parsed request packet; wait for end of SETUP transaction
                    if T_FIN = '1' then
                        -- Got complet SETUP packet; handle it
                        case s_ctlrequest is
                            when req_getstatus =>
                                -- Prepare status byte and move to data stage
                                -- If s_ctlparam = 0, the status byte has already
                                -- been prepared in state S_SETUP.
                                for i in 1 to NENDPT loop
                                    if unsigned(s_ctlparam(3 downto 0)) = i then
                                        if s_ctlparam(7) = '1' then
                                            s_sendbyte <= "0000000" & C_HLTIN(i);
                                        else
                                            s_sendbyte <= "0000000" & C_HLTOUT(i);
                                        end if;
                                    end if;
                                end loop;
                                s_state <= ST_WAITIN;
                            when req_clearfeature =>
                                -- Reset endpoint
                                for i in 1 to NENDPT loop
                                    if unsigned(s_ctlparam(3 downto 0)) = i then
                                        if s_ctlparam(7) = '1' then
                                            C_CLRIN(i)  <= '1';
                                        else
                                            C_CLROUT(i) <= '1';
                                        end if;
                                    end if;
                                end loop;
                                s_state <= ST_IDLE;
                            when req_setfeature =>
                                -- Set endpoint HALT
                                for i in 1 to NENDPT loop
                                    if unsigned(s_ctlparam(3 downto 0)) = i then
                                        if s_ctlparam(7) = '1' then
                                            C_SHLTIN(i)  <= '1';
                                        else
                                            C_SHLTOUT(i) <= '1';
                                        end if;
                                    end if;
                                end loop;
                                s_state <= ST_IDLE;
                            when req_setaddress =>
                                -- Move to status stage
                                s_state <= ST_WAITIN;
                            when req_getdesc =>
                                -- Move to data stage
                                s_state <= ST_WAITIN;
                            when req_getconf =>
                                -- Move to data stage
                                s_state <= ST_WAITIN;
                            when req_setconf =>
                                -- Set device configuration
                                if s_ctlparam(7 downto 1) = "0000000" then
                                    s_confd <= s_ctlparam(0);
                                    s_state <= ST_IDLE;
                                    C_CLRIN  <= (others => '1');
                                    C_CLROUT <= (others => '1');
                                else
                                    -- Unknown configuration number
                                    s_state <= ST_STALL;
                                end if;
                            when req_getiface =>
                                -- Move to data stage
                                s_state <= ST_WAITIN;
                            when others =>
                                -- Unsupported request
                                s_state <= ST_STALL;
                        end case;
                    elsif T_SETUP = '0' then
                        -- Got corrupt SETUP packet; ignore
                        s_state <= ST_IDLE;
                    end if;

                when ST_WAITIN =>
                    -- Got valid SETUP packet; waiting for IN transaction.
                    s_answerptr(5 downto 0) <= "000000";
                    if T_SETUP = '1' then
                        -- Start of next SETUP transaction
                        s_state <= ST_SETUP;
                        s_setupptr <= to_unsigned(0, s_setupptr'length);
                    elsif T_IN = '1' then
                        -- Start of IN transaction; respond to the request
                        case s_ctlrequest is
                            when req_getstatus =>
                                -- Respond with status byte, followed by zero byte.
                                s_state <= ST_SENDRESP;
                            when req_setaddress =>
                                -- Effectuate change of device address
                                s_addr <= s_ctlparam(6 downto 0);
                                s_state <= ST_IDLE;
                            when req_getdesc =>
                                -- Respond with descriptor
                                s_state <= ST_STARTDESC;
                            when req_getconf =>
                                -- Respond with current configuration
                                s_sendbyte  <= "0000000" & s_confd;
                                s_state     <= ST_SENDRESP;
                            when req_getiface =>
                                -- Respond with zero byte
                                s_sendbyte  <= "00000000";
                                s_state     <= ST_SENDRESP;
                            when others =>
                                -- Impossible
                        end case;
                    end if;

                when ST_SENDRESP =>
                    -- Respond to IN with a preset byte,
                    -- followed by zero or more nul byte(s)
                    if T_IN = '0' then
                        -- Aborted IN transaction; wait for retry
                        s_state <= ST_WAITIN;
                    elsif T_TXRDY = '1' then
                        -- Need next data byte
                        s_sendbyte <= "00000000";
                        if (s_answerptr(0) = '1') or (s_answerlen(0) = '1') then
                            -- Reached end of transfer.
                            -- Note that we only ever send 1 or 2 byte answers.
                            s_state <= ST_DONESEND;
                        end if;
                        s_answerptr(5 downto 0) <= s_answerptr(5 downto 0) + 1;
                    end if;

                when ST_STARTDESC =>
                    -- Fetching first byte of packet.
                    if T_IN = '0' then
                        -- Aborted IN transaction; wait for retry
                        s_state <= ST_WAITIN;
                    elsif unsigned(C_DSCLEN) = 0 then
                        -- Invalid descriptor.
                        s_state <= ST_STALL;
                    elsif (s_answerptr = unsigned(C_DSCLEN)) or
                          (s_answerptr = s_answerlen) then
                        -- Send an empty packet to complete the transfer.
                        s_state <= ST_DONESEND;
                    else
                        -- Send a normal descriptor packet.
                        s_state <= ST_SENDDESC;
                    end if;
                    s_answerptr(5 downto 0) <= s_answerptr(5 downto 0) + 1;

		when ST_SENDDESC =>
		    -- Respond to IN with descriptor
		    if T_IN = '0' then
			-- Aborted IN transaction; wait for retry
			s_state <= ST_WAITIN;
		    elsif T_TXRDY = '1' then
			-- Need next data byte
                        if (s_answerptr(5 downto 0) = 0) or
                           (s_answerptr = unsigned(C_DSCLEN)) or
                           (s_answerptr = s_answerlen) then
                            -- Just sent the last byte of the packet
                            s_state <= ST_DONESEND;
                        else
                            s_answerptr(5 downto 0) <= s_answerptr(5 downto 0) + 1;
                        end if;
		    end if;

		when ST_DONESEND =>
                    -- Done sending packet; wait until IN transaction completes.
                    -- Note: s_answerptr contains the number of bytes sent so-far,
                    -- unless this is a multiple of 64, in which case s_answerptr
                    -- contains 64 less than the number of bytes sent; and unless
                    -- the last packet sent was an empty end-of-transfer packet,
                    -- in which case s_answerptr contains 1 more than the number
                    -- of bytes sent.
                    if T_FIN = '1' then
                        -- Host acknowledged transaction.
                        if s_answerptr(5 downto 0) = 0 then
                            -- The last sent packet was a full sized packet.
                            -- If s_answerptr + 64 = s_answerlen, the transfer
                            -- is now complete; otherwise the host will expect
                            -- more data. In either case, we go back to WAITIN.
                            -- This can't go wrong because WAITIN also listens
                            -- for the next SETUP and handles it properly.
                            s_state <= ST_WAITIN;
                        else
                            -- The last sent packet was not full sized;
                            -- it was either empty or reached the end of
                            -- the descriptor. In either case, the transfer
                            -- is now complete.
                            s_state <= ST_IDLE;
                        end if;
                        s_answerptr <= s_answerptr + 64;
                    elsif T_IN = '0' then
                        -- Transaction failed; wait for retry.
                        s_state <= ST_WAITIN;
                    end if;

            end case;

        end if;

    end process;

end architecture usb_control_arch;
--  USB 2.0 Packet-level logic.
--
--  This entity hides the details of the UTMI interface and handles
--  computation and verificaton of CRCs.
--
--  The low-level interface signals are named PHY_xxx and may be
--  connected to an UTMI compliant USB PHY, such as the SMSC GT3200.
--
--  The application interface signals are named P_xxx.
--  The receiving side of the interface operates as follows:
--    * At the start of an incoming packet, RXACT is set high.
--    * When a new byte arrives, RXRDY is asserted and the byte is put
--      on RXDAT. These signals are valid for only one clock cycle; the
--      application must accept them immediately.
--    * The first byte of a packet is the PID. Subsequent bytes contain
--      data and CRC. This entity verifies the CRC, but does not
--      discard it from the data stream.
--    * Some time after correctly receiving the last byte of a packet,
--      RXACT is deasserted; at the same time RXFIN is asserted for one cycle
--      to confirm the packet.
--    * If a corrupt packet is received, RXACT is deasserted without
--      asserting RXFIN.
--
--  The transmission side of the interface operates as follows:
--    * The application starts transmission by setting TXACT to 1 and setting
--      TXDAT to the PID value (with correctly mirrored high order bits).
--    * The entity asserts TXRDY when it needs the next payload byte.
--      On the following clock cycle, the application must then provide the
--      next payload byte on TXDAT, or deassert TXACT to indicate the end of
--      the packet. The signal on TXDAT must be held stable until the next
--      assertion of TXRDY.
--    * CRC bytes should not be included in the payload; the entity will
--      add them automatically.
--    * As part of the high speed handshake, the application may request
--      transmission of a continuous chirp K state by asserting CHIRPK.
--
--  Implementation note:
--  Transmission timing is a bit tricky due to the following issues:
--    * After the PHY asserts PHY_TXREADY, we must immediately provide
--      new data or deassert PHY_TXVALID on the next clock cycle.
--    * The PHY may assert PHY_TXREADY during subsequent clock cycles,
--      even though the average byte period is more than 40 cycles.
--    * We want to register PHY inputs and outputs to ensure valid timing.
--
--  To satisfy these requirements, we make the application run one byte
--  ahead. While keeping the current byte in the output register PHY_DATAOUT,
--  the application already provides the following data byte. That way, we
--  can respond to PHY_TXREADY immediately in the next cycle, with the
--  application following up in the clock cycle after that.
--

library ieee;
use ieee.std_logic_1164.all, ieee.numeric_std.all;

entity usb_packet is

    port (

        -- 60 MHz UTMI clock.
        CLK :           in  std_logic;

        -- Synchronous reset of this entity.
        RESET :         in  std_logic;

        -- High to force chirp K transmission.
	P_CHIRPK :      in  std_logic;

        -- High while receiving a packet.
        P_RXACT :       out std_logic;

        -- Indicates next byte received; data must be read from RXDAT immediately.
        P_RXRDY :       out std_logic;

        -- High for one cycle to indicate successful completion of packet.
        P_RXFIN :       out std_logic;

        -- Received byte value. Valid if RXRDY is high.
        P_RXDAT :       out std_logic_vector(7 downto 0);

        -- High while transmitting a packet.
        P_TXACT :       in  std_logic;

        -- Request for next data byte; application must change TXDAT on the next clock cycle.
        P_TXRDY :       out std_logic;

        -- Data byte to transmit. Hold stable until next assertion of TXRDY.
        P_TXDAT :       in  std_logic_vector(7 downto 0);

        -- Connect to UTMI DataIn signal.
        PHY_DATAIN :    in std_logic_vector(7 downto 0);

        -- Connect to UTMI DataOut signal.
        PHY_DATAOUT :   out std_logic_vector(7 downto 0);

        -- Connect to UTMI TxValid signal.
        PHY_TXVALID :   out std_logic;

        -- Connect to UTMI TxReady signal.
        PHY_TXREADY :   in std_logic;

        -- Connect to UTMI RxActive signal.
        PHY_RXACTIVE :  in std_logic;

        -- Connect to UTMI RxValid signal.
        PHY_RXVALID :   in std_logic;

        -- Connect to UTMI RxError signal.
        PHY_RXERROR :   in std_logic );

end entity usb_packet;

architecture usb_packet_arch of usb_packet is

    -- State machine
    type t_state is (
	ST_NONE, ST_CHIRPK,
	ST_RWAIT, ST_RTOKEN, ST_RDATA, ST_RSHAKE,
	ST_TSTART, ST_TDATA, ST_TCRC1, ST_TCRC2 );
    signal s_state : t_state := ST_NONE;
    signal s_txfirst : std_logic := '0';

    -- Registered inputs
    signal s_rxactive : std_logic;
    signal s_rxvalid : std_logic;
    signal s_rxerror : std_logic;
    signal s_datain : std_logic_vector(7 downto 0);
    signal s_txready : std_logic;

    -- Byte pending for transmission
    signal s_dataout : std_logic_vector(7 downto 0);

    -- True if an incoming packet would be valid if it ended now.
    signal s_rxgoodpacket : std_logic;

    -- CRC computation
    constant crc5_gen : std_logic_vector(4 downto 0) := "00101";
    constant crc5_res : std_logic_vector(4 downto 0) := "01100";
    constant crc16_gen : std_logic_vector(15 downto 0) := "1000000000000101";
    constant crc16_res : std_logic_vector(15 downto 0) := "1000000000001101";
    signal crc5_buf : std_logic_vector(4 downto 0);
    signal crc16_buf : std_logic_vector(15 downto 0);

    -- Update CRC 5 to account for a new byte
    function crc5_upd(
	c : in std_logic_vector(4 downto 0);
	b : in std_logic_vector(7 downto 0) )
	return std_logic_vector
    is
	variable t : std_logic_vector(4 downto 0);
	variable y : std_logic_vector(4 downto 0);
    begin
	t := (
	    b(0) xor c(4),
	    b(1) xor c(3),
	    b(2) xor c(2),
	    b(3) xor c(1),
	    b(4) xor c(0) );
	y := (
	    b(5) xor t(1) xor t(2),
	    b(6) xor t(0) xor t(1) xor t(4),
	    b(5) xor b(7) xor t(0) xor t(3) xor t(4),
	    b(6) xor t(1) xor t(3) xor t(4),
	    b(7) xor t(0) xor t(2) xor t(3) );
	return y;
    end function;

    -- Update CRC-16 to account for new byte
    function crc16_upd(
	c : in std_logic_vector(15 downto 0);
	b : in std_logic_vector(7 downto 0) )
	return std_logic_vector
    is
	variable t : std_logic_vector(7 downto 0);
	variable y : std_logic_vector(15 downto 0);
    begin
	t := (
	    b(0) xor c(15),
	    b(1) xor c(14),
	    b(2) xor c(13),
	    b(3) xor c(12),
	    b(4) xor c(11),
	    b(5) xor c(10),
	    b(6) xor c(9),
	    b(7) xor c(8) );
	y := (
	    c(7) xor t(0) xor t(1) xor t(2) xor t(3) xor t(4) xor t(5) xor t(6) xor t(7),
	    c(6), c(5), c(4), c(3), c(2),
	    c(1) xor t(7),
	    c(0) xor t(6) xor t(7),
	    t(5) xor t(6),
	    t(4) xor t(5),
	    t(3) xor t(4),
	    t(2) xor t(3),
	    t(1) xor t(2),
	    t(0) xor t(1),
	    t(1) xor t(2) xor t(3) xor t(4) xor t(5) xor t(6) xor t(7),
	    t(0) xor t(1) xor t(2) xor t(3) xor t(4) xor t(5) xor t(6) xor t(7) );
	return y;
    end function;

begin

    -- Assign output signals
    P_RXACT <= s_rxactive;
    P_RXFIN <= (not s_rxactive) and (not s_rxerror) and s_rxgoodpacket;
    P_RXRDY <= s_rxactive and s_rxvalid;
    P_RXDAT <= s_datain;

    -- Assert P_TXRDY during ST_TSTART to acknowledge the PID byte,
    -- during the first cycle of ST_TDATA to acknowledge the first
    -- data byte, and whenever we need a new data byte during ST_TDATA.
    P_TXRDY <= '1' when (s_state = ST_TSTART)
               else (s_txfirst or s_txready) when (s_state = ST_TDATA)
	       else '0';

    -- On every rising clock edge
    process is
	variable v_dataout : std_logic_vector(7 downto 0);
	variable v_txvalid : std_logic;	
	variable v_crc_upd : std_logic;	
	variable v_crc_data : std_logic_vector(7 downto 0);
        variable v_crc5_new : std_logic_vector(4 downto 0);
        variable v_crc16_new : std_logic_vector(15 downto 0);
    begin
	wait until rising_edge(CLK);

	-- Default assignment to temporary variables
        v_dataout := s_dataout;
	v_txvalid := '0';
	v_crc_upd := '0';
	v_crc_data := "00000000";
        v_crc5_new := "00000";
        v_crc16_new := "0000000000000000";

	-- Default assignment to s_txfirst
	s_txfirst <= '0';

	-- Register inputs
	s_rxactive <= PHY_RXACTIVE;
	s_rxvalid <= PHY_RXVALID;
	s_rxerror <= PHY_RXERROR;
	s_datain <= PHY_DATAIN;
	s_txready <= PHY_TXREADY;

	-- State machine
	if RESET = '1' then

	    -- Reset entity
	    s_state <= ST_NONE;
            s_rxgoodpacket <= '0';

	else

	    case s_state is
		when ST_NONE =>
		    -- Waiting for incoming or outgoing packet

		    -- Initialize CRC buffers
		    crc5_buf <= "11111";
		    crc16_buf <= "1111111111111111";
                    s_rxgoodpacket <= '0';

                    if P_CHIRPK = '1' then
                        -- Send continuous chirp K.
                        s_state <= ST_CHIRPK;

                    elsif s_rxactive = '1' then
			-- Receiver starting

			if s_rxerror = '1' then
			    -- Receive error at PHY level
			    s_state <= ST_RWAIT;
			elsif s_rxvalid = '1' then
			    -- Got PID byte
			    if s_datain(3 downto 0) = not s_datain(7 downto 4) then
				case s_datain(1 downto 0) is
				    when "01" => -- token packet
					s_state <= ST_RTOKEN;
				    when "11" => -- data packet
					s_state <= ST_RDATA;
				    when "10" => -- handshake packet
					s_state <= ST_RSHAKE;
                                        s_rxgoodpacket <= '1';
				    when others => -- PING token or special packet
                                        -- If this is a PING token, it will work out fine;
                                        -- otherwise it will be flagged as a bad packet
                                        -- either here or in usb_transact.
					s_state <= ST_RTOKEN;
				end case;
			    else
				-- Corrupt PID byte
				s_state <= ST_RWAIT;
			    end if;
			end if;

		    elsif P_TXACT = '1' then
			-- Transmission starting; put data in output buffer
			v_txvalid := '1';
			v_dataout := P_TXDAT;
			s_state <= ST_TSTART;
		    end if;

                when ST_CHIRPK =>
                    -- Sending continuous chirp K.
                    if P_CHIRPK = '0' then
                        s_state <= ST_NONE;
                    end if;

		when ST_RTOKEN =>
		    -- Receiving a token packet
		    if s_rxactive = '0' then
			-- End of packet
                        s_rxgoodpacket <= '0';
                        s_state <= ST_NONE;
		    elsif s_rxerror = '1' then
			-- Error at PHY level
                        s_rxgoodpacket <= '0';
			s_state <= ST_RWAIT;
		    elsif s_rxvalid = '1' then
			-- Just received a byte; update CRC
			v_crc5_new := crc5_upd(crc5_buf, s_datain);
                        crc5_buf   <= v_crc5_new;
                        if v_crc5_new = crc5_res then
                            s_rxgoodpacket <= '1';
                        else
                            s_rxgoodpacket <= '0';
                        end if;
		    end if;

		when ST_RDATA =>
		    -- Receiving a data packet
		    if s_rxactive = '0' then
			-- End of packet
                        s_rxgoodpacket <= '0';
                        s_state <= ST_NONE;
		    elsif s_rxerror = '1' then
			-- Error at PHY level
                        s_rxgoodpacket <= '0';
			s_state <= ST_RWAIT;
		    elsif s_rxvalid = '1' then
			-- Just received a byte; update CRC
			v_crc_upd := '1';
			v_crc_data := s_datain;
		    end if;

		when ST_RWAIT =>
		    -- Wait until the end of the current packet
		    if s_rxactive = '0' then
			s_state <= ST_NONE;
		    end if;

		when ST_RSHAKE =>
		    -- Receiving a handshake packet
		    if s_rxactive = '0' then
			-- Got good handshake
                        s_rxgoodpacket <= '0';
			s_state <= ST_NONE;
		    elsif s_rxerror = '1' or s_rxvalid = '1' then
			-- Error or unexpected data byte in handshake packet
                        s_rxgoodpacket <= '0';
			s_state <= ST_RWAIT;
		    end if;

		when ST_TSTART =>
		    -- Transmission starting;
		    -- PHY module sees our PHY_TXVALID signal;
		    -- PHY_TXREADY is undefined;
		    -- we assert P_TXRDY to acknowledge the PID byte
		    v_txvalid := '1';
		    -- Check packet type
		    case P_TXDAT(1 downto 0) is
			when "11" => -- data packet
			    s_state <= ST_TDATA;
			    s_txfirst <= '1';
			when "10" => -- handshake packet
			    s_state <= ST_RWAIT;
			when others => -- should not happen
		    end case;

		when ST_TDATA =>
		    -- Sending a data packet
		    v_txvalid := '1';
		    if (s_txready = '1') or (s_txfirst = '1') then
			-- Need next byte
			if P_TXACT = '0' then
			    -- No more data; send first CRC byte
			    for i in 0 to 7 loop
				v_dataout(i) := not crc16_buf(15-i);
			    end loop;
			    s_state <= ST_TCRC1;
			else
			    -- Put next byte in output buffer
			    v_dataout := P_TXDAT;
			    -- And update the CRC
			    v_crc_upd := '1';
			    v_crc_data := P_TXDAT;
			end if;
		    end if;

		when ST_TCRC1 =>
		    -- Sending the first CRC byte of a data packet
		    v_txvalid := '1';
		    if s_txready = '1' then
			-- Just queued the first CRC byte; move to 2nd byte
			for i in 0 to 7 loop
			    v_dataout(i) := not crc16_buf(7-i);
			end loop;
			s_state <= ST_TCRC2;
		    end if;

		when ST_TCRC2 =>
		    -- Sending the second CRC byte of a data packet
		    if s_txready = '1' then
			-- Just sent the 2nd CRC byte; end packet
			s_state <= ST_RWAIT;
		    else
			-- Last byte is still pending
			v_txvalid := '1';
		    end if;

	    end case;

	end if;

	-- CRC-16 update
	if v_crc_upd = '1' then
	    v_crc16_new := crc16_upd(crc16_buf, v_crc_data);
	    crc16_buf   <= v_crc16_new;
            if s_state = ST_RDATA and v_crc16_new = crc16_res then
                -- If this is the last byte of the packet, it is a valid packet.
                s_rxgoodpacket <= '1';
            else
                s_rxgoodpacket <= '0';
            end if;
	end if;

        -- Drive data output to PHY
        if RESET = '1' then
            -- Reset.
            PHY_TXVALID <= '0';
            PHY_DATAOUT <= "00000000";
        elsif s_state = ST_CHIRPK then
            -- Continuous chirp-K.
            PHY_TXVALID <= P_CHIRPK;
            PHY_DATAOUT <= "00000000";
        elsif (PHY_TXREADY = '1') or (s_state = ST_NONE and P_TXACT = '1') then
            -- Move a data byte from the buffer to the output lines when the PHY
            -- accepts the previous byte, and also at the start of a new packet.
	    PHY_TXVALID <= v_txvalid;
	    PHY_DATAOUT <= v_dataout;
	end if;

        -- Keep pending output byte in register.
        s_dataout <= v_dataout;

    end process;

end architecture usb_packet_arch;
--  USB 2.0 Initialization, handshake and reset detection.
--
--  This entity provides the following functions:
--
--    * USB bus attachment: At powerup and after a RESET signal, switch to
--      non-driving mode, wait for 17 ms, then attach to the USB bus. This
--      should ensure that the host notices our reattachment and initiates
--      a reset procedure.
--
--    * High speed handshake (if HSSUPPORT enabled): attempt to enter
--      high speed mode after a bus reset.
--
--    * Monitor the linestate for reset and/or suspend signalling.
--
--  The low-level interface connects to an UTMI compliant USB PHY such as
--  the SMSC GT3200. The UTMI interface must be configured for 60 MHz operation
--  with an 8-bit data bus.
--

library ieee;
use ieee.std_logic_1164.all, ieee.numeric_std.all;

entity usb_init is

    generic (

        -- Support high speed mode.
        HSSUPPORT : boolean := false );

    port (

        -- 60 MHz UTMI clock.
        CLK :           in std_logic;

        -- Synchronous reset; triggers detach and reattach to the USB bus.
        RESET :         in std_logic;

        -- High for one clock if a reset signal is detected on the USB bus.
        I_USBRST :      out std_logic;

        -- High when attached to the host in high speed mode.
        I_HIGHSPEED :   out std_logic;

        -- High when suspended.
        -- Reset of this signal is asynchronous.
        -- This signal may be used to drive (inverted) the UTMI SuspendM pin.
        I_SUSPEND :     out std_logic;

        -- High to tell usb_packet that it must drive a continuous K state.
        P_CHIRPK :      out std_logic;

        -- Connect to the UTMI Reset signal.
        PHY_RESET :     out std_logic;

        -- Connect to the UTMI LineState signal.
        PHY_LINESTATE : in std_logic_vector(1 downto 0);

        -- Cconnect to the UTMI OpMode signal.
        PHY_OPMODE :    out std_logic_vector(1 downto 0);

        -- Connect to the UTMI XcvrSelect signal (0 = high speed, 1 = full speed).
        PHY_XCVRSELECT : out std_logic;

        -- Connect to the UTMI TermSelect signal (0 = high speed, 1 = full speed).
        PHY_TERMSELECT : out std_logic );

end entity usb_init;

architecture usb_init_arch of usb_init is

    -- Time from bus idle until device suspend (3 ms).
    constant TIME_SUSPEND : unsigned(19 downto 0) := to_unsigned(180000, 20);

    -- Time from start of SE0 until detection of reset signal (2.5 us + 10%).
    constant TIME_RESET :   unsigned(7 downto 0)  := to_unsigned(165, 8);

    -- Time to wait for good SE0 when waking up from suspend (6 ms).
    constant TIME_SUSPRST:  unsigned(19 downto 0) := to_unsigned(360000, 20);

    -- Duration of chirp K from device during high speed detection (1 ms + 10%).
    constant TIME_CHIRPK :  unsigned(19 downto 0) := to_unsigned(66000, 20);

    -- Minimum duration of chirp J/K during high speed detection (2.5 us + 10%).
    constant TIME_FILT :    unsigned(7 downto 0)  := to_unsigned(165, 8);

    -- Time to wait for chirp until giving up (1.1 ms).
    constant TIME_WTFS :    unsigned(19 downto 0) := to_unsigned(66000, 20);

    -- Time to wait after reverting to full-speed before sampling the bus (100 us).
    constant TIME_WTRSTHS : unsigned(19 downto 0) := to_unsigned(6000, 20);

    -- State machine
    type t_state is (
        ST_INIT, ST_FSRESET, ST_FULLSPEED, ST_SUSPEND, ST_SUSPRESET,
        ST_SENDCHIRP, ST_RECVCHIRP, ST_HIGHSPEED, ST_HSREVERT );
    signal s_state :        t_state := ST_INIT;

    -- Timers.
    signal s_timer1 :       unsigned(7 downto 0);
    signal s_timer2 :       unsigned(19 downto 0) := to_unsigned(0, 20);

    -- Count J/K chirps.
    signal s_chirpcnt :     unsigned(2 downto 0);

    -- High if the device is operating in high speed (or suspended from high speed).
    signal s_highspeed :    std_logic := '0';

    -- High if the device is currently suspended.
    -- Reset of this signal is asynchronous.
    signal s_suspend :      std_logic := '0';

    -- Input registers.
    signal s_linestate :    std_logic_vector(1 downto 0);

    -- Output registers.
    signal s_reset :        std_logic := '1';
    signal s_opmode :       std_logic_vector(1 downto 0) := "01";
    signal s_xcvrselect :   std_logic := '1';
    signal s_termselect :   std_logic := '1';
    signal s_chirpk :       std_logic := '0';

begin

    I_USBRST    <= s_reset;
    I_HIGHSPEED <= s_highspeed;
    I_SUSPEND   <= s_suspend;
    P_CHIRPK    <= s_chirpk;
    PHY_RESET   <= s_reset;
    PHY_OPMODE  <= s_opmode;
    PHY_XCVRSELECT <= s_xcvrselect;
    PHY_TERMSELECT <= s_termselect;

    -- Synchronous process.
    process is
        variable v_clrtimer1 : std_logic;
        variable v_clrtimer2 : std_logic;
    begin
	wait until rising_edge(CLK);

        -- By default, do not clear the timers.
        v_clrtimer1 := '0';
        v_clrtimer2 := '0';

	-- Register linestate input.
	s_linestate <= PHY_LINESTATE;

        -- Default assignments to registers.
        s_reset     <= '0';
        s_chirpk    <= '0';

        if RESET = '1' then

            -- Reset PHY.
            s_reset      <= '1';
	    s_opmode     <= "01";
            s_xcvrselect <= '1';
            s_termselect <= '1';

            -- Go to ST_INIT state and wait until bus attachment.
            v_clrtimer1  := '1';
            v_clrtimer2  := '1';
            s_highspeed  <= '0';
            s_state      <= ST_INIT;

	else

            case s_state is

                when ST_INIT =>
                    -- Wait before attaching to bus.
                    s_opmode     <= "01";   -- non-driving
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    v_clrtimer1  := '1';
                    if s_timer2 = to_unsigned(0, s_timer2'length) - 1 then
                        -- Timer2 overflows after ~ 17 ms; attach to bus.
                        v_clrtimer2 := '1';
                        s_state     <= ST_FULLSPEED;
                    end if;

                when ST_FSRESET =>
                    -- Waiting for end of reset before full speed operation.
                    s_highspeed  <= '0';
                    s_opmode     <= "00";   -- normal
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    v_clrtimer1  := '1';
                    v_clrtimer2  := '1';
                    if s_linestate /= "00" then
                        -- Reset signal ended.
                        s_state     <= ST_FULLSPEED;
                    end if;

                when ST_FULLSPEED =>
                    -- Operating in full speed.
                    s_highspeed  <= '0';
                    s_opmode     <= "00";   -- normal
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    if s_linestate /= "00" then
                        -- Bus not in SE0 state; clear reset timer.
                        v_clrtimer1 := '1';
                    end if;
                    if s_linestate /= "01" then
                        -- Bus not in J state; clear suspend timer.
                        v_clrtimer2 := '1';
                    end if;
                    if s_timer1 = TIME_RESET then
                        -- Bus has been in SE0 state for TIME_RESET;
                        -- this is a reset signal.
                        s_reset     <= '1';
                        if HSSUPPORT then
                            s_state     <= ST_SENDCHIRP;
                        else
                            s_state     <= ST_FSRESET;
                        end if;
                    elsif s_timer2 = TIME_SUSPEND then
                        -- Bus has been idle for TIME_SUSPEND;
                        -- go to suspend state.
                        s_state     <= ST_SUSPEND;
                    end if;

                when ST_SUSPEND =>
                    -- Suspended; waiting for resume signal.
                    -- Possibly our clock will be disabled; wake up
                    -- is initiated by the asynchronous reset of s_suspend.
                    s_opmode     <= "00";   -- normal   
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    v_clrtimer1  := '1';
                    v_clrtimer2  := '1';
                    if s_linestate /= "01" then
                        -- Bus not in J state; resume.
                        if HSSUPPORT and s_highspeed = '1' then
                            -- High speed resume protocol.
                            if s_linestate = "10" then
                                -- Bus in K state; resume to high speed.
                                s_state     <= ST_HIGHSPEED;
                            elsif s_linestate = "00" then
                                -- Bus in SE0 state; start reset detection.
                                s_state     <= ST_SUSPRESET;
                            end if;
                        else
                            -- Resume to full speed.
                            s_state     <= ST_FULLSPEED;
                        end if;
                    end if;

                when ST_SUSPRESET =>
                    -- Wake up in SE0 state; wait for proper reset signal.
                    s_opmode     <= "00";   -- normal   
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    if s_linestate /= "00" then
                        -- Bus not in SE0 state; clear reset timer.
                        v_clrtimer1 := '1';
                    end if;
                    if s_timer1 = TIME_RESET then
                        -- Bus has been in SE0 state for TIME_RESET;
                        -- this is a reset signal.
                        s_reset     <= '1';
                        v_clrtimer2 := '1';
                        s_state     <= ST_SENDCHIRP;
                    end if;
                    if s_timer2 = TIME_SUSPRST then
                        -- Still no proper reset signal; go back to sleep.
                        s_state     <= ST_SUSPEND;
                    end if;

                when ST_SENDCHIRP =>
                    -- Sending chirp K for a duration of TIME_CHIRPK.
                    s_highspeed  <= '0';
                    s_opmode     <= "10";   -- disable bit stuffing
                    s_xcvrselect <= '0';    -- high speed
                    s_termselect <= '1';    -- full speed
                    s_chirpk     <= '1';    -- send chirp K
                    v_clrtimer1  := '1';
                    if s_timer2 = TIME_CHIRPK then
                        -- end of chirp K
                        v_clrtimer2 := '1';
                        s_chirpcnt  <= "000";
                        s_state     <= ST_RECVCHIRP;
                    end if;

                when ST_RECVCHIRP =>
                    -- Waiting for K-J-K-J-K-J chirps.
                    -- Note: DO NOT switch Opmode to normal yet; there
                    -- may be pending bits in the transmission buffer.
                    s_opmode     <= "10";   -- disable bit stuffing
                    s_xcvrselect <= '0';    -- high speed
                    s_termselect <= '1';    -- full speed
                    if ( s_chirpcnt(0) = '0' and s_linestate /= "10" ) or
                       ( s_chirpcnt(0) = '1' and s_linestate /= "01" ) then
                        -- Not the linestate we want.
                        v_clrtimer1 := '1';
                    end if;
                    if s_timer2 = TIME_WTFS then
                        -- High speed detection failed; go to full speed.
                        v_clrtimer1 := '1';
                        v_clrtimer2 := '1';
                        s_state     <= ST_FSRESET;
                    elsif s_timer1 = TIME_FILT then
                        -- We got the chirp we wanted.
                        if s_chirpcnt = 5 then
                            -- This was the last chirp;
                            -- we got a successful high speed handshake.
                            v_clrtimer2 := '1';
                            s_state     <= ST_HIGHSPEED;
                        end if;
                        s_chirpcnt  <= s_chirpcnt + 1;
                        v_clrtimer1 := '1';
                    end if;

                when ST_HIGHSPEED =>
                    -- Operating in high speed.
                    s_highspeed  <= '1';
                    s_opmode     <= "00";   -- normal
                    s_xcvrselect <= '0';    -- high speed
                    s_termselect <= '0';    -- high speed
                    if s_linestate /= "00" then
                        -- Bus not idle; clear revert timer.
                        v_clrtimer2 := '1';
                    end if;
                    if s_timer2 = TIME_SUSPEND then
                        -- Bus has been idle for TIME_SUSPEND;
                        -- revert to full speed.
                        v_clrtimer2 := '1';
                        s_state     <= ST_HSREVERT;
                    end if;

                when ST_HSREVERT =>
                    -- Revert to full speed and wait for 100 us.
                    s_opmode     <= "00";   -- normal
                    s_xcvrselect <= '1';    -- full speed
                    s_termselect <= '1';    -- full speed
                    if s_timer2 = TIME_WTRSTHS then
                        v_clrtimer2 := '1';
                        if s_linestate = "00" then
                            -- Reset from high speed.
                            s_reset     <= '1';
                            s_state     <= ST_SENDCHIRP;
                        else
                            -- Suspend from high speed.
                            s_state     <= ST_SUSPEND;
                        end if;
                    end if;

            end case;

	end if;

        -- Increment or clear timer1.
        if v_clrtimer1 = '1' then
            s_timer1 <= to_unsigned(0, s_timer1'length);
        else
            s_timer1 <= s_timer1 + 1;
        end if;

        -- Increment or clear timer2.
        if v_clrtimer2 = '1' then
            s_timer2 <= to_unsigned(0, s_timer2'length);
        else
            s_timer2 <= s_timer2 + 1;
        end if;

    end process;

    -- Drive the s_suspend flipflop (synchronous set, asynchronous reset).
    process (CLK, PHY_LINESTATE) is
    begin
        if PHY_LINESTATE /= "01" then
            -- The bus is not in full speed idle state;
            -- reset the s_suspend flipflop.
            s_suspend   <= '0';
        elsif rising_edge(CLK) then
            if s_state = ST_SUSPEND then
                -- Bus is idle and FSM is in suspend state;
                -- enable the s_suspend flipflop.
                s_suspend   <= '1';
            end if;
        end if;
    end process;

end architecture usb_init_arch;

--  USB 2.0 Serial data transfer entity
--
--  This entity implements a USB 2.0 device that carries a bidirectional
--  byte stream over the bus. It communicates with the host according to
--  the USB Communication Device Class, specifically the ACM (Abstract
--  Control Model) variant.
--
--  The low-level interface signals are labeled PHY_xxx and can be connected
--  to an UTMI-compliant PHY component. The PHY should be configured in 8-bit
--  mode.
--
--  The application interface supports simple byte-at-a-time sending and
--  receiving. Three block RAMs are used to implement a receive buffer,
--  a transmission buffer and descriptor ROM.
--
--  The CLK input must be the 60 MHz clock generated by the UTMI transceiver.
--  All application interface signals and PHY interface signals are
--  synchronized to the rising edge of CLK, except for SUSPEND which has
--  an asynchronous reset.
--
--  Transmission:
--    * The entity asserts TXRDY when it is ready to send data.
--    * The application puts data on TXDAT and asserts TXVAL when it is
--      ready to send data.
--    * In each clock cycle in which TXRDY and TXVAL are both asserted,
--      the entity takes a byte from TXDAT and queues it for transmission.
--
--  Receiving:
--    * The application asserts RXRDY when it is ready to receive data.
--    * The entity puts data on RXDAT and asserts RXVAL when it has
--      data available. It will only do this in response to RXRDY.
--    * When RXVAL is high, the application must either accept a byte
--      from RXDAT and be ready for the next byte in the following cycle,
--      or it must deassert RXRDY to pause the receive queue.
--
--  At power on, and after RESET, the device waits for 16 ms before
--  attaching to the USB bus. A high signal on ONLINE indicates that
--  the device has been fully configured by the host.
--
--  Bugs and limitations:
--    * The TEST_MODE feature (mandatory for high speed devices) is
--      not implemented and returns an error condition to the host.
--    * The SEND_ENCAPSULATED_COMMAND and GET_ENCAPSULATED_RESPONSE commands
--      (mandatory CDC-ACM requests) are not supported but will return a
--      success condition to the host.
--    * The default control pipe does not verify requests from the host
--      as strictly as required by the standard. As a result, invalid
--      requests from the host may sometimes appear to succeed when
--      they should have returned an error condition.
--
--  Implementation note:
--  At some point it may become useful to implement separate clock domains
--  for the application resp. PHY side of this entity, using the FIFO buffers
--  for clock domain crossing. As a first step, a distinction has been made
--  between application-side signals (prefixed with q_) and PHY-side signals
--  (prefixed with s_). Currently the corresponding signals from both sides
--  are simply wired together with asynchronous assignments. By replacing
--  these hardwired connections with carefully designed synchronization logic,
--  a separation of clock domains could be realized.
--

library ieee;
use ieee.std_logic_1164.all, ieee.numeric_std.all;
use work.usb_pkg.all;

entity usb_serial is

    generic (

        -- Vendor ID to report in device descriptor.
        VENDORID :      std_logic_vector(15 downto 0);

        -- Product ID to report in device descriptor.
        PRODUCTID :     std_logic_vector(15 downto 0);

        -- Product version to report in device descriptor.
        VERSIONBCD :    std_logic_vector(15 downto 0);

        -- Support high speed mode.
        HSSUPPORT :     boolean := false;

        -- Set to true if the device never draws power from the USB bus.
        SELFPOWERED :   boolean := false;

        -- Size of receive buffer as 2-logarithm of the number of bytes.
        -- Must be at least 10 (1024 bytes) for high speed support.
        RXBUFSIZE_BITS: integer range 7 to 12 := 11;

        -- Size of transmit buffer as 2-logarithm of the number of bytes.
        TXBUFSIZE_BITS: integer range 7 to 12 := 10 );

    port (

        -- 60 MHz UTMI clock.
        CLK :           in  std_logic;

        -- Synchronous reset; clear buffers and re-attach to the bus.
        RESET :         in  std_logic;

        -- High for one clock when a reset signal is detected on the USB bus.
        -- Note: do NOT wire this signal to RESET externally.
        USBRST :        out std_logic;

        -- High when the device is operating (or suspended) in high speed mode.
        HIGHSPEED :     out std_logic;

        -- High while the device is suspended.
        -- Note: This signal is not synchronized to CLK.
        -- It may be used to asynchronously drive the UTMI SuspendM pin.
        SUSPEND :       out std_logic;

        -- High when the device is in the Configured state.
        ONLINE :        out std_logic;

        -- High if a received byte is available on RXDAT.
        RXVAL :         out std_logic;

        -- Received data byte, valid if RXVAL is high.
        RXDAT :         out std_logic_vector(7 downto 0);

        -- High if the application is ready to receive the next byte.
        RXRDY :         in  std_logic;

        -- Number of bytes currently available in receive buffer.
        RXLEN :         out std_logic_vector((RXBUFSIZE_BITS-1) downto 0);

        -- High if the application has data to send.
        TXVAL :         in  std_logic;

        -- Data byte to send, must be valid if TXVAL is high.
        TXDAT :         in  std_logic_vector(7 downto 0);

        -- High if the entity is ready to accept the next byte.
        TXRDY :         out std_logic;

        -- Number of free byte positions currently available in transmit buffer.
        TXROOM :        out std_logic_vector((TXBUFSIZE_BITS-1) downto 0);

        -- Temporarily suppress transmissions at the outgoing endpoint.
        -- This gives the application an oppertunity to fill the transmit
        -- buffer in order to blast data efficiently in big chunks.
        TXCORK :        in  std_logic;

        PHY_DATAIN :    in  std_logic_vector(7 downto 0);
	PHY_DATAOUT :   out std_logic_vector(7 downto 0);
	PHY_TXVALID :   out std_logic;
	PHY_TXREADY :   in  std_logic;
	PHY_RXACTIVE :  in  std_logic;
	PHY_RXVALID :   in  std_logic;
	PHY_RXERROR :   in  std_logic;
	PHY_LINESTATE : in  std_logic_vector(1 downto 0);
	PHY_OPMODE :    out std_logic_vector(1 downto 0);
        PHY_XCVRSELECT: out std_logic;
        PHY_TERMSELECT: out std_logic;
	PHY_RESET :     out std_logic );
	
end entity usb_serial;

architecture usb_serial_arch of usb_serial is

    -- Byte array type
    type t_byte_array is array(natural range <>) of std_logic_vector(7 downto 0);

    -- Conditional expression.
    function choose_int(z: boolean; a, b: integer)
        return integer is
    begin
        if z then return a; else return b; end if;
    end function;

    -- Conditional expression.
    function choose_byte(z: boolean; a, b: std_logic_vector)
        return std_logic_vector is
    begin
        if z then return a; else return b; end if;
    end function;

    -- Maximum packet size according to protocol.
    constant MAX_FSPACKET_SIZE: integer := 64;
    constant MAX_HSPACKET_SIZE: integer := 512;

    -- Width required for a pointer that can cover either RX or TX buffer.
    constant BUFPTR_SIZE :  integer := choose_int(RXBUFSIZE_BITS > TXBUFSIZE_BITS, RXBUFSIZE_BITS, TXBUFSIZE_BITS);

    -- Data endpoint number.
    constant data_endpt :   std_logic_vector(3 downto 0) := "0001";
    constant notify_endpt : std_logic_vector(3 downto 0) := "0010";

    -- Descriptor ROM
    --   addr   0 ..  17 : device descriptor
    --   addr  20 ..  29 : device qualifier
    --   addr  32 ..  98 : full speed configuration descriptor 
    --   addr 112 .. 178 : high speed configuration descriptor
    --   addr 179 :        other_speed_configuration hack
    constant DESC_DEV_ADDR :        integer := 0;
    constant DESC_DEV_LEN  :        integer := 18;
    constant DESC_QUAL_ADDR :       integer := 20;
    constant DESC_QUAL_LEN :        integer := 10;
    constant DESC_FSCFG_ADDR :      integer := 32;
    constant DESC_FSCFG_LEN :       integer := 67;
    constant DESC_HSCFG_ADDR :      integer := 112;
    constant DESC_HSCFG_LEN :       integer := 67;
    constant DESC_OTHERSPEED_ADDR : integer := 179;

    constant descrom_pre: t_byte_array(0 to 191) :=
        -- 18 bytes device descriptor
      ( X"12",                  -- bLength = 18 bytes
        X"01",                  -- bDescriptorType = device descriptor
        choose_byte(HSSUPPORT, X"00", X"10"),   -- bcdUSB = 1.10 or 2.00
        choose_byte(HSSUPPORT, X"02", X"01"),
        X"02",                  -- bDeviceClass = Communication Device Class
        X"00",                  -- bDeviceSubClass = none
        X"00",                  -- bDeviceProtocol = none
        X"40",                  -- bMaxPacketSize0 = 64 bytes
        VENDORID(7 downto 0),   -- idVendor
        VENDORID(15 downto 8),
        PRODUCTID(7 downto 0),  -- idProduct
        PRODUCTID(15 downto 8),
        VERSIONBCD(7 downto 0), -- bcdDevice
        VERSIONBCD(15 downto 8),
        X"00",                  -- iManufacturer
        X"00",                  -- iProduct
        X"00",                  -- iSerialNumber
        X"01",                  -- bNumConfigurations = 1
        -- 2 bytes padding
        X"00", X"00",
        -- 10 bytes device qualifier
        X"0a",                  -- bLength = 10 bytes
        X"06",                  -- bDescriptorType = device qualifier
        X"00", X"02",           -- bcdUSB = 2.0
        X"02",                  -- bDeviceClass = Communication Device Class
        X"00",                  -- bDeviceSubClass = none
        X"00",                  -- bDeviceProtocol = none
        X"40",                  -- bMaxPacketSize0 = 64 bytes
        X"01",                  -- bNumConfigurations = 1
        X"00",                  -- bReserved
        -- 2 bytes padding
        X"00", X"00",
        -- 67 bytes full-speed configuration descriptor
        -- 9 bytes configuration header
        X"09",                  -- bLength = 9 bytes
        X"02",                  -- bDescriptorType = configuration descriptor
        X"43", X"00",           -- wTotalLength = 67 bytes
        X"02",                  -- bNumInterfaces = 2
        X"01",                  -- bConfigurationValue = 1
        X"00",                  -- iConfiguration = none
        choose_byte(SELFPOWERED, X"c0", X"80"), -- bmAttributes
        X"fa",                  -- bMaxPower = 500 mA
        -- 9 bytes interface descriptor (communication control class)
        X"09",                  -- bLength = 9 bytes
        X"04",                  -- bDescriptorType = interface descriptor
        X"00",                  -- bInterfaceNumber = 0
        X"00",                  -- bAlternateSetting = 0
        X"01",                  -- bNumEndpoints = 1
        X"02",                  -- bInterfaceClass = Communication Interface
        X"02",                  -- bInterfaceSubClass = Abstract Control Model
        X"01",                  -- bInterfaceProtocol = V.25ter (required for Linux CDC-ACM driver)
        X"00",                  -- iInterface = none
        -- 5 bytes functional descriptor (header)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"00",                  -- bDescriptorSubtype = header
        X"10", X"01",           -- bcdCDC = 1.10
        -- 4 bytes functional descriptor (abstract control management)
        X"04",                  -- bLength = 4 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"02",                  -- bDescriptorSubtype = Abstract Control Mgmnt
        X"00",                  -- bmCapabilities = none
        -- 5 bytes functional descriptor (union)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"06",                  -- bDescriptorSubtype = union
        X"00",                  -- bMasterInterface = 0
        X"01",                  -- bSlaveInterface0 = 1
        -- 5 bytes functional descriptor (call management)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"01",                  -- bDescriptorSubType = Call Management
        X"00",                  -- bmCapabilities = no call mgmnt
        X"01",                  -- bDataInterface = 1
        -- 7 bytes endpoint descriptor (notify IN)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"82",                  -- bEndpointAddress = IN 2
        X"03",                  -- bmAttributes = interrupt data
        X"08", X"00",           -- wMaxPacketSize = 8 bytes
        X"ff",                  -- bInterval = 255 frames
        -- 9 bytes interface descriptor (data class)
        X"09",                  -- bLength = 9 bytes
        X"04",                  -- bDescriptorType = interface descriptor
        X"01",                  -- bInterfaceNumber = 1
        X"00",                  -- bAlternateSetting = 0
        X"02",                  -- bNumEndpoints = 2
        X"0a",                  -- bInterfaceClass = Data Interface
        X"00",                  -- bInterfaceSubClass = none
        X"00",                  -- bInterafceProtocol = none
        X"00",                  -- iInterface = none
	-- 7 bytes endpoint descriptor (data IN)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"81",                  -- bEndpointAddress = IN 1
        X"02",                  -- bmAttributes = bulk data
        X"40", X"00",           -- wMaxPacketSize = 64 bytes
        X"00",                  -- bInterval
        -- 7 bytes endpoint descriptor (data OUT)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"01",                  -- bEndpointAddress = OUT 1
        X"02",                  -- bmAttributes = bulk data
        X"40", X"00",           -- wMaxPacketSize = 64 bytes
        X"00",                  -- bInterval
        -- 13 bytes padding
        X"00", X"00", X"00", X"00", X"00", X"00", X"00", X"00",
        X"00", X"00", X"00", X"00", X"00",
        -- 67 bytes high-speed configuration descriptor
        -- 9 bytes configuration header
        X"09",                  -- bLength = 9 bytes
        X"02",                  -- bDescriptorType = configuration descriptor
        X"43", X"00",           -- wTotalLength = 67 bytes
        X"02",                  -- bNumInterfaces = 2
        X"01",                  -- bConfigurationValue = 1
        X"00",                  -- iConfiguration = none
        choose_byte(SELFPOWERED, X"c0", X"80" ), -- bmAttributes = self-powered
        X"fa",                  -- bMaxPower = 500 mA
        -- 9 bytes interface descriptor (communication control class)
        X"09",                  -- bLength = 9 bytes
        X"04",                  -- bDescriptorType = interface descriptor
        X"00",                  -- bInterfaceNumber = 0
        X"00",                  -- bAlternateSetting = 0
        X"01",                  -- bNumEndpoints = 1
        X"02",                  -- bInterfaceClass = Communication Interface
        X"02",                  -- bInterfaceSubClass = Abstract Control Model
        X"01",                  -- bInterfaceProtocol = V.25ter (required for Linux CDC-ACM driver)
        X"00",                  -- iInterface = none
        -- 5 bytes functional descriptor (header)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"00",                  -- bDescriptorSubtype = header
        X"10", X"01",           -- bcdCDC = 1.10
        -- 4 bytes functional descriptor (abstract control management)
        X"04",                  -- bLength = 4 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"02",                  -- bDescriptorSubtype = Abstract Control Mgmnt
        X"00",                  -- bmCapabilities = none
        -- 5 bytes functional descriptor (union)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"06",                  -- bDescriptorSubtype = union
        X"00",                  -- bMasterInterface = 0
        X"01",                  -- bSlaveInterface0 = 1
        -- 5 bytes functional descriptor (call management)
        X"05",                  -- bLength = 5 bytes
        X"24",                  -- bDescriptorType = CS_INTERFACE
        X"01",                  -- bDescriptorSubType = Call Management
        X"00",                  -- bmCapabilities = no call mgmnt
        X"01",                  -- bDataInterface = 1
        -- 7 bytes endpoint descriptor (notify IN)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"82",                  -- bEndpointAddress = IN 2
        X"03",                  -- bmAttributes = interrupt data
        X"08", X"00",           -- wMaxPacketSize = 8 bytes
        X"0f",                  -- bInterval = 2**14 frames
        -- 9 bytes interface descriptor (data class)
        X"09",                  -- bLength = 9 bytes
        X"04",                  -- bDescriptorType = interface descriptor
        X"01",                  -- bInterfaceNumber = 1
        X"00",                  -- bAlternateSetting = 0
        X"02",                  -- bNumEndpoints = 2
        X"0a",                  -- bInterfaceClass = Data Interface
        X"00",                  -- bInterfaceSubClass = none
        X"00",                  -- bInterafceProtocol = none
        X"00",                  -- iInterface = none
	-- 7 bytes endpoint descriptor (data IN)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"81",                  -- bEndpointAddress = IN 1
        X"02",                  -- bmAttributes = bulk data
        X"00", X"02",           -- wMaxPacketSize = 512 bytes
        X"00",                  -- bInterval
        -- 7 bytes endpoint descriptor (data OUT)
        X"07",                  -- bLength = 7 bytes
        X"05",                  -- bDescriptorType = endpoint descriptor
        X"01",                  -- bEndpointAddress = OUT 1
        X"02",                  -- bmAttributes = bulk data
        X"00", X"02",           -- wMaxPacketSize = 512 bytes
        X"00",                  -- bInterval = never NAK
        -- other_speed_configuration hack
        X"07",
        -- 12 bytes padding
        X"00", X"00", X"00", X"00", X"00", X"00", X"00", X"00",
        X"00", X"00", X"00", X"00" );

    constant descrom: t_byte_array(0 to (choose_int(HSSUPPORT, 191, 111))) :=
        descrom_pre(0 to choose_int(HSSUPPORT, 191, 111));
    signal descrom_start:   unsigned(choose_int(HSSUPPORT, 7, 6) downto 0);
    signal descrom_raddr:   unsigned(choose_int(HSSUPPORT, 7, 6) downto 0);
    signal descrom_rdat:    std_logic_vector(7 downto 0);

    -- RX buffer
    signal rxbuf:           t_byte_array(0 to (2**RXBUFSIZE_BITS-1));
    signal rxbuf_rdat:      std_logic_vector(7 downto 0);

    -- TX buffer
    signal txbuf:           t_byte_array(0 to (2**TXBUFSIZE_BITS-1));
    signal txbuf_rdat:      std_logic_vector(7 downto 0);

    -- Interface to usb_init
    signal usbi_usbrst :    std_logic;
    signal usbi_highspeed : std_logic;
    signal usbi_suspend :   std_logic;

    -- Interface to usb_packet
    signal usbp_chirpk :    std_logic;
    signal usbp_rxact :     std_logic;
    signal usbp_rxrdy :     std_logic;
    signal usbp_rxfin :     std_logic;
    signal usbp_rxdat :     std_logic_vector(7 downto 0);
    signal usbp_txact :     std_logic;
    signal usbp_txrdy :     std_logic;
    signal usbp_txdat :     std_logic_vector(7 downto 0);

    -- Interface to usb_transact
    signal usbt_in :        std_logic;
    signal usbt_out :       std_logic;
    signal usbt_setup :     std_logic;
    signal usbt_ping :      std_logic;
    signal usbt_fin :       std_logic;
    signal usbt_endpt :     std_logic_vector(3 downto 0);
    signal usbt_nak :       std_logic;
    signal usbt_stall :     std_logic;
    signal usbt_nyet :      std_logic;
    signal usbt_send :      std_logic;
    signal usbt_isync :     std_logic;
    signal usbt_osync :     std_logic;
    signal usbt_rxrdy :     std_logic;
    signal usbt_rxdat :     std_logic_vector(7 downto 0);
    signal usbt_txrdy :     std_logic;
    signal usbt_txdat :     std_logic_vector(7 downto 0);

    -- Interface to usb_control
    signal usbc_addr :      std_logic_vector(6 downto 0);
    signal usbc_confd :     std_logic;
    signal usbc_clr_in :    std_logic_vector(1 to 2);
    signal usbc_clr_out :   std_logic_vector(1 to 2);
    signal usbc_sethlt_in : std_logic_vector(1 to 2);
    signal usbc_sethlt_out: std_logic_vector(1 to 2);
    signal usbc_dscbusy :   std_logic;
    signal usbc_dscrd :     std_logic;
    signal usbc_dsctyp :    std_logic_vector(2 downto 0);
    signal usbc_dscinx :    std_logic_vector(7 downto 0);
    signal usbc_dscoff :    std_logic_vector(7 downto 0);
    signal usbc_dsclen :    std_logic_vector(7 downto 0);
    signal usbc_selfpowered : std_logic;
    signal usbc_in :        std_logic;
    signal usbc_out :       std_logic;
    signal usbc_setup :     std_logic;
    signal usbc_ping :      std_logic;
    signal usbc_nak :       std_logic;
    signal usbc_stall :     std_logic;
    signal usbc_nyet :      std_logic;
    signal usbc_send :      std_logic;
    signal usbc_isync :     std_logic;
    signal usbc_txdat :     std_logic_vector(7 downto 0);

    -- State machine
    type t_state is (
      ST_IDLE, ST_STALL, ST_NAK,
      ST_INSTART, ST_INSEND, ST_INDONE, ST_OUTRECV, ST_OUTNAK );
    signal s_state : t_state := ST_IDLE;

    -- Endpoint administration (PHY side).
    signal s_rxbuf_head :   unsigned(RXBUFSIZE_BITS-1 downto 0) := to_unsigned(0, RXBUFSIZE_BITS);
    signal s_rxbuf_tail :   unsigned(RXBUFSIZE_BITS-1 downto 0);
    signal s_txbuf_head :   unsigned(TXBUFSIZE_BITS-1 downto 0);
    signal s_txbuf_tail :   unsigned(TXBUFSIZE_BITS-1 downto 0) := to_unsigned(0, TXBUFSIZE_BITS);
    signal s_txbuf_stop :   unsigned(TXBUFSIZE_BITS-1 downto 0);
    signal s_bufptr :       unsigned(BUFPTR_SIZE-1 downto 0);
    signal s_txprev_full :  std_logic := '0';       -- Last transmitted packet was full-size
    signal s_txprev_acked : std_logic := '1';       -- Last trantsmitted packet was ack-ed.
    signal s_isync :        std_logic := '0';
    signal s_osync :        std_logic := '0';
    signal s_halt_in :      std_logic_vector(1 to 2) := "00";
    signal s_halt_out :     std_logic_vector(1 to 2) := "00";
    signal s_nyet :         std_logic := '0';

    -- Buffer state (application side).
    signal q_rxbuf_head :   unsigned(RXBUFSIZE_BITS-1 downto 0);
    signal q_rxbuf_tail :   unsigned(RXBUFSIZE_BITS-1 downto 0) := to_unsigned(0, RXBUFSIZE_BITS);
    signal q_txbuf_head :   unsigned(TXBUFSIZE_BITS-1 downto 0) := to_unsigned(0, TXBUFSIZE_BITS);
    signal q_txbuf_tail :   unsigned(TXBUFSIZE_BITS-1 downto 0);

    -- Control signals (PHY side).
    signal s_reset :        std_logic;
    signal s_txcork :       std_logic;

    -- Status signals (application side).
    signal q_usbrst :       std_logic;
    signal q_online :       std_logic;
    signal q_highspeed :    std_logic;

    -- Receive buffer logic (application side).
    signal q_rxval :        std_logic := '0';
    signal q_rxbuf_read :   std_logic;
    signal q_txbuf_rdy :    std_logic;

begin

    -- Check buffer size.
    assert ((not HSSUPPORT) or (RXBUFSIZE_BITS >= 10))
        report "High-speed device needs at least 1024 bytes RX buffer";

    -- Bus reset logic
    usb_init_inst : usb_init
        generic map (
            HSSUPPORT       => HSSUPPORT )
        port map (
            CLK             => CLK,
            RESET           => s_reset,
            I_USBRST        => usbi_usbrst,
            I_HIGHSPEED     => usbi_highspeed,
            I_SUSPEND       => usbi_suspend,
            P_CHIRPK        => usbp_chirpk,
            PHY_RESET       => PHY_RESET,
            PHY_LINESTATE   => PHY_LINESTATE,
            PHY_OPMODE      => PHY_OPMODE,
            PHY_XCVRSELECT  => PHY_XCVRSELECT,
            PHY_TERMSELECT  => PHY_TERMSELECT );

    -- Packet level logic
    usb_packet_inst : usb_packet
        port map (
            CLK             => CLK,
            RESET           => usbi_usbrst,
            P_CHIRPK        => usbp_chirpk,
            P_RXACT         => usbp_rxact,
            P_RXRDY         => usbp_rxrdy,
            P_RXFIN         => usbp_rxfin,
            P_RXDAT         => usbp_rxdat,
            P_TXACT         => usbp_txact,
            P_TXRDY         => usbp_txrdy,
            P_TXDAT         => usbp_txdat,
            PHY_DATAIN      => PHY_DATAIN,
            PHY_DATAOUT     => PHY_DATAOUT,
            PHY_TXVALID     => PHY_TXVALID,
            PHY_TXREADY     => PHY_TXREADY,
            PHY_RXACTIVE    => PHY_RXACTIVE,
            PHY_RXVALID     => PHY_RXVALID,
            PHY_RXERROR     => PHY_RXERROR );

    -- Transaction level logic
    usb_transact_inst : usb_transact
        generic map (
            HSSUPPORT       => HSSUPPORT )
        port map (
            CLK             => CLK,
            RESET           => usbi_usbrst,
            T_IN            => usbt_in,
            T_OUT           => usbt_out,
            T_SETUP         => usbt_setup,
            T_PING          => usbt_ping,
            T_FIN           => usbt_fin,
            T_ADDR          => usbc_addr,
            T_ENDPT         => usbt_endpt,
            T_NAK           => usbt_nak,
            T_STALL         => usbt_stall,
            T_NYET          => usbt_nyet,
            T_SEND          => usbt_send,
            T_ISYNC         => usbt_isync,
            T_OSYNC         => usbt_osync,
            T_RXRDY         => usbt_rxrdy,
            T_RXDAT         => usbt_rxdat,
            T_TXRDY         => usbt_txrdy,
            T_TXDAT         => usbt_txdat,
            I_HIGHSPEED     => usbi_highspeed,
            P_RXACT         => usbp_rxact,
            P_RXRDY         => usbp_rxrdy,
            P_RXFIN         => usbp_rxfin,
            P_RXDAT         => usbp_rxdat,
            P_TXACT         => usbp_txact,
            P_TXRDY         => usbp_txrdy,
            P_TXDAT         => usbp_txdat );

    -- Default control endpoint
    usb_control_inst : usb_control
        generic map (
	    NENDPT          => 2 )
        port map (
            CLK             => CLK,
            RESET           => usbi_usbrst,
            C_ADDR          => usbc_addr,
            C_CONFD         => usbc_confd,
            C_CLRIN         => usbc_clr_in,
            C_CLROUT        => usbc_clr_out,
            C_HLTIN         => s_halt_in,
            C_HLTOUT        => s_halt_out,
            C_SHLTIN        => usbc_sethlt_in,
            C_SHLTOUT       => usbc_sethlt_out,
            C_DSCBUSY       => usbc_dscbusy,
            C_DSCRD         => usbc_dscrd,
            C_DSCTYP        => usbc_dsctyp,
            C_DSCINX        => usbc_dscinx,
            C_DSCOFF        => usbc_dscoff,
            C_DSCLEN        => usbc_dsclen,
            C_SELFPOWERED   => usbc_selfpowered,
            T_IN            => usbc_in,
            T_OUT           => usbc_out,
            T_SETUP         => usbc_setup,
            T_PING          => usbc_ping,
            T_FIN           => usbt_fin,
            T_NAK           => usbc_nak,
            T_STALL         => usbc_stall,
            T_NYET          => usbc_nyet,
            T_SEND          => usbc_send,
            T_ISYNC         => usbc_isync,
            T_OSYNC         => usbt_osync,
            T_RXRDY         => usbt_rxrdy,
            T_RXDAT         => usbt_rxdat,
            T_TXRDY         => usbt_txrdy,
            T_TXDAT         => usbc_txdat );

    -- Assign usb_serial output signals.
    USBRST      <= q_usbrst;
    HIGHSPEED   <= q_highspeed;
    SUSPEND     <= usbi_suspend;
    ONLINE      <= q_online;
    RXVAL       <= q_rxval;
    RXDAT       <= rxbuf_rdat;
    RXLEN       <= std_logic_vector(q_rxbuf_head - q_rxbuf_tail);
    TXRDY       <= q_txbuf_rdy;
    TXROOM      <= std_logic_vector(q_txbuf_tail - q_txbuf_head - 1);

    -- Assign usb_control input signals
    usbc_in     <= usbt_in    when (usbt_endpt = "0000") else '0';
    usbc_out    <= usbt_out   when (usbt_endpt = "0000") else '0';
    usbc_setup  <= usbt_setup when (usbt_endpt = "0000") else '0';
    usbc_ping   <= usbt_ping  when (usbt_endpt = "0000") else '0';
    usbc_selfpowered <= '1'   when SELFPOWERED else '0';

    -- Assign usb_transact input lines
    usbt_nak    <= usbc_nak   when (usbt_endpt = "0000") else
                   '1'        when (s_state = ST_NAK) else
                   '0';
    usbt_stall  <= usbc_stall when (usbt_endpt = "0000") else
                   '1'        when (s_state = ST_STALL) else
                   '0';
    usbt_nyet   <= usbc_nyet  when (usbt_endpt = "0000") else
                   s_nyet;
    usbt_send   <= usbc_send  when (usbt_endpt = "0000") else
                   '1'        when (s_state = ST_INSEND) else
		   '0';
    usbt_isync  <= usbc_isync when (usbt_endpt = "0000") else
                   s_isync;
    usbt_txdat  <= usbc_txdat when (usbt_endpt = "0000" and usbc_dscbusy = '0') else
                   descrom_rdat when (usbt_endpt = "0000") else
                   txbuf_rdat;

    -- Buffer logic.
    q_rxbuf_read <= (RXRDY or (not q_rxval)) when (q_rxbuf_tail /= q_rxbuf_head) else '0';
    q_txbuf_rdy <= '1' when (q_txbuf_head + 1 /= q_txbuf_tail) else '0';

    -- Connection between PHY-side and application-side signals.
    -- This could be a good place to insert clock domain crossing.
    q_rxbuf_head <= s_rxbuf_head;
    s_rxbuf_tail <= q_rxbuf_tail;
    s_txbuf_head <= q_txbuf_head;
    q_txbuf_tail <= s_txbuf_tail;
    s_txcork    <= TXCORK;
    s_reset     <= RESET;
    q_online    <= usbc_confd;
    q_usbrst    <= usbi_usbrst;
    q_highspeed <= usbi_highspeed;

    -- Lookup address/length of the selected descriptor (combinatorial).
    process (usbc_dsctyp, usbc_dscinx, usbi_highspeed)
        constant slen: integer := descrom_start'length;
        constant nlen: integer := USBC_DSCLEN'length;
        variable s: unsigned((slen-1) downto 0);
        variable n: unsigned((nlen-1) downto 0);
    begin
        s := to_unsigned(0, slen);
        n := to_unsigned(0, nlen);
        case usbc_dsctyp is
            when "001" =>   -- device descriptor
                s := to_unsigned(DESC_DEV_ADDR, slen);
                n := to_unsigned(DESC_DEV_LEN, nlen);
            when "010" =>   -- configuration descriptor
                if usbc_dscinx = X"00" then
                    if HSSUPPORT and (usbi_highspeed = '1') then
                        s := to_unsigned(DESC_HSCFG_ADDR, slen);
                        n := to_unsigned(DESC_HSCFG_LEN, nlen);
                    else
                        s := to_unsigned(DESC_FSCFG_ADDR, slen);
                        n := to_unsigned(DESC_FSCFG_LEN, nlen);
                    end if;
                end if;
            when "110" =>   -- device qualifier
                if HSSUPPORT then
                    s := to_unsigned(DESC_QUAL_ADDR, slen);
                    n := to_unsigned(DESC_QUAL_LEN, nlen);
                end if;
            when "111" =>   -- other speed configuration
                if HSSUPPORT and (usbc_dscinx = X"00") then
                    if usbi_highspeed = '1' then
                        s := to_unsigned(DESC_FSCFG_ADDR, slen);
                        n := to_unsigned(DESC_FSCFG_LEN, nlen);
                    else
                        s := to_unsigned(DESC_HSCFG_ADDR, slen);
                        n := to_unsigned(DESC_HSCFG_LEN, nlen);
                    end if;
                end if;
            when others =>
                -- unsupported descriptor type
        end case;
        descrom_start <= s;
        usbc_dsclen   <= std_logic_vector(n);
    end process;

    -- Main application-side synchronous process.
    process is
    begin
        wait until rising_edge(CLK);

        if RESET = '1' then

            -- Reset this entity.
            q_rxbuf_tail <= to_unsigned(0, RXBUFSIZE_BITS);
            q_txbuf_head <= to_unsigned(0, TXBUFSIZE_BITS);
            q_rxval      <= '0'; 

        else

            -- Read data from the RX buffer.
            if q_rxbuf_read = '1' then
                -- The RAM buffer reads a byte in this cycle.
                q_rxbuf_tail    <= q_rxbuf_tail + 1;
                q_rxval         <= '1';
            elsif RXRDY = '1' then
                -- Byte consumed by application; no new data yet.
                q_rxval         <= '0';
            end if;

            -- Write data to the TX buffer.
            if (TXVAL = '1') and (q_txbuf_rdy = '1') then
                -- The RAM buffer writes a byte in this cycle.
                q_txbuf_head    <= q_txbuf_head + 1;
            end if;

        end if;

    end process;

    -- Main PHY-side synchronous process.
    process is
        variable v_max_txsize :     unsigned(TXBUFSIZE_BITS-1 downto 0);
        variable v_rxbuf_len_lim :  unsigned(RXBUFSIZE_BITS-1 downto 0);
        variable v_rxbuf_tmp_head : unsigned(RXBUFSIZE_BITS-1 downto 0);
        variable v_rxbuf_pktroom :  std_logic;
    begin
        wait until rising_edge(CLK);

        -- Determine the maximum packet size we can transmit.
        if HSSUPPORT and usbi_highspeed = '1' then
            v_max_txsize := to_unsigned(MAX_HSPACKET_SIZE, TXBUFSIZE_BITS);
        else
            v_max_txsize := to_unsigned(MAX_FSPACKET_SIZE, TXBUFSIZE_BITS);
        end if;

        -- Determine if there is room for another packet in the RX buffer.
        -- We need room for the largest possible incoming packet, plus
        -- two CRC bytes.
        if HSSUPPORT then
            v_rxbuf_len_lim := to_unsigned(2**RXBUFSIZE_BITS - MAX_HSPACKET_SIZE - 2, RXBUFSIZE_BITS);
        else
            v_rxbuf_len_lim := to_unsigned(2**RXBUFSIZE_BITS - MAX_FSPACKET_SIZE - 2, RXBUFSIZE_BITS);
        end if;
        if HSSUPPORT and s_state = ST_OUTRECV then
            -- Currently receiving a packet; compare against the temporary
            -- tail pointer to decide NYET vs ACK.
            v_rxbuf_tmp_head := resize(s_bufptr, RXBUFSIZE_BITS);
        else
            -- Not receiving a packet (or NYET not supported);
            -- compare against the tail pointer to decide NAK vs ACK.
            v_rxbuf_tmp_head := s_rxbuf_head;
        end if;
        if v_rxbuf_tmp_head - s_rxbuf_tail < v_rxbuf_len_lim then
            v_rxbuf_pktroom := '1';
        else
            v_rxbuf_pktroom := '0';
        end if;

        -- State machine
        if s_reset = '1' then

            -- Reset this entity.
            s_state         <= ST_IDLE;
            s_rxbuf_head    <= to_unsigned(0, RXBUFSIZE_BITS);
            s_txbuf_tail    <= to_unsigned(0, TXBUFSIZE_BITS);
            s_txprev_full   <= '0';
            s_txprev_acked  <= '1';
            s_isync         <= '0';
            s_osync         <= '0';
            s_halt_in       <= "00";
            s_halt_out      <= "00";

        elsif usbi_usbrst = '1' then

            -- Reset protocol state.
            s_state         <= ST_IDLE;
            s_txprev_full   <= '0';
            s_txprev_acked  <= '1';
            s_isync         <= '0';
            s_osync         <= '0';
            s_halt_in       <= "00";
            s_halt_out      <= "00";

        else

            case s_state is

                when ST_IDLE =>
                    -- Idle; wait for a transaction
                    s_nyet <= '0';
                    if (usbt_endpt = data_endpt) and (usbt_in = '1') then
                        -- Start of IN transaction
                        if s_halt_in(1) = '1' then
                            -- Endpoint halted
                            s_state  <= ST_STALL;
                        elsif (s_txbuf_tail /= s_txbuf_head and s_txcork = '0') or s_txprev_full = '1' then
                            -- Prepare to send data
                            s_bufptr <= resize(s_txbuf_tail, s_bufptr'length);
                            s_state  <= ST_INSTART;
                        else
                            -- We have no data to send
                            s_state  <= ST_NAK;
                        end if;
                    elsif (usbt_endpt = data_endpt) and (usbt_out = '1') then
                        -- Start of OUT transaction
                        if s_halt_out(1) = '1' then
                            -- Endpoint halted
                            s_state  <= ST_STALL;
                        elsif v_rxbuf_pktroom = '1' then
                            -- Prepare to receive data
                            s_bufptr <= resize(s_rxbuf_head, s_bufptr'length);
                            s_state  <= ST_OUTRECV; 
                        else
                            -- We have no room to store a new packet
                            s_state  <= ST_OUTNAK;
                        end if;
                    elsif HSSUPPORT and (usbt_endpt = data_endpt) and (usbt_ping = '1') then
                         -- Start of PING transaction
                        if v_rxbuf_pktroom = '1' then
                            -- There is room in the RX buffer for another packet; do nothing (ACK).
                            s_state  <= ST_IDLE;
                        else
                            -- There is no room in the RX buffer; respond with NAK.
                            s_state  <= ST_NAK;
                        end if;
                    elsif (usbt_endpt = notify_endpt) and (usbt_in = '1') then
                        -- The notify endpoint simply NAK's all IN transactions
                        if s_halt_in(2) = '1' then
                            -- Endpoint halted
                            s_state <= ST_STALL;
                        else
                            s_state <= ST_NAK;
                        end if;
                    end if;

                    -- Reset sync bits when the control endpoint tells us.
                    s_isync <= s_isync and (not usbc_clr_in(1));
                    s_osync <= s_osync and (not usbc_clr_out(1));

                    -- Set/reset halt bits when the control endpoint tells us.
                    s_halt_in(1)  <= (s_halt_in(1) or usbc_sethlt_in(1)) and (not usbc_clr_in(1));
                    s_halt_in(2)  <= (s_halt_in(2) or usbc_sethlt_in(2)) and (not usbc_clr_in(2));
                    s_halt_out(1) <= (s_halt_out(1) or usbc_sethlt_out(1)) and (not usbc_clr_out(1));

                when ST_STALL =>
                    -- Wait for end of transaction
                    if (usbt_in = '0') and (usbt_out = '0') and (usbt_ping = '0') then
                        s_state <= ST_IDLE;
                    end if;

                when ST_NAK =>
                    -- Wait for end of transaction
                    if (usbt_in = '0') and (usbt_out = '0') and (usbt_ping = '0') then
                        s_state <= ST_IDLE;
                    end if;

                when ST_INSTART =>
                    -- Prepare to send data; read first byte from memory.
                    if usbt_in = '0' then
                        -- Transaction canceled.
                        s_state <= ST_IDLE;
                    elsif (s_txbuf_tail = s_txbuf_head) or
                          (s_txprev_acked = '0' and resize(s_bufptr, TXBUFSIZE_BITS) = s_txbuf_stop) or
                          (s_txprev_acked = '1' and s_txcork = '1') then
                        -- The TX buffer is empty, or a previous empty packet
                        -- is unacknowledged, or the TX buffer is corked;
                        -- must send an empty packet.
                        s_state <= ST_INDONE;
                    else
                        -- Send a non-empty packet.
                        if s_txprev_acked = '1' then
                            -- Set up a size limit for this packet.
                            s_txbuf_stop <= s_txbuf_tail + v_max_txsize;
                        end if;
			s_bufptr <= s_bufptr + 1;
                        s_state <= ST_INSEND;
                    end if;

                when ST_INSEND =>
                    -- Sending data
                    if usbt_in = '0' then
                        -- Transaction canceled.
                        s_state <= ST_IDLE;
                    elsif usbt_txrdy = '1' then
                        -- Need to provide the next data byte;
                        -- stop when we reach the end of the TX buffer;
                        -- stop when we reach the packet size limit.
                        if (resize(s_bufptr, TXBUFSIZE_BITS) = s_txbuf_head) or
                           (resize(s_bufptr, TXBUFSIZE_BITS) = s_txbuf_stop) then
                            -- No more bytes
                            s_state <= ST_INDONE;
                        else
                            s_bufptr <= s_bufptr + 1;
                        end if;
                    end if;

                when ST_INDONE =>
                    -- Done sending packet; wait for ACK.
                    if usbt_in = '0' then
                        -- No acknowledgement
                        s_txprev_acked <= '0';
                        -- Set limit for next packet to the same point
			s_txbuf_stop <= resize(s_bufptr, TXBUFSIZE_BITS);
                        -- Done
                        s_state <= ST_IDLE;
                    elsif usbt_fin = '1' then
                        -- Got acknowledgement
                        s_txprev_acked <= '1';
                        -- Update buffer tail
                        s_txbuf_tail <= resize(s_bufptr, TXBUFSIZE_BITS);
                        -- Flip sync bit
                        s_isync <= not s_isync;
                        -- Remember if this was a full-sized packet.
                        if s_txbuf_tail + v_max_txsize = resize(s_bufptr, TXBUFSIZE_BITS) then
                            s_txprev_full <= '1';
                        else
                            s_txprev_full <= '0';
                        end if;
                        -- Done
                        s_state <= ST_IDLE;
                    end if;

                when ST_OUTRECV =>
                    -- Receiving data
                    if usbt_out = '0' then
                        -- Transaction ended.
                        -- If the transaction was succesful, usbt_fin has been
                        -- asserted in the previous cycle and has triggered
                        -- an update of s_rxbuf_head.
                        s_state <= ST_IDLE;
                    elsif (usbt_fin = '1') and (usbt_osync = s_osync) then
                        -- Good packet received; discard CRC bytes
                        s_rxbuf_head <= resize(s_bufptr, RXBUFSIZE_BITS) - 2;
                        s_osync <= not s_osync;
                    elsif usbt_rxrdy = '1' then
                        -- Got data byte
                        s_bufptr <= s_bufptr + 1;
                        if HSSUPPORT then
                            -- Set NYET if there is no room to receive
                            -- another packet after this one.
                            s_nyet <= not v_rxbuf_pktroom;
                        end if;
                    end if;

                when ST_OUTNAK =>
                    -- Receiving data while we don't have room to store it
                    if usbt_out = '0' then
                        -- End of transaction
                        s_state <= ST_IDLE;
                    elsif (usbt_rxrdy = '1') and (usbt_osync = s_osync) then
                        -- This is a new (non-duplicate) packet, but we can
                        -- not store it; so respond with NAK.
                        s_state <= ST_NAK;
                    end if;

            end case;

        end if;
    end process;

    -- It is always a fight to get the synthesizer to infer block RAM.
    -- The problem is we need dual port RAM with read-enable signals.
    -- The recommended coding style, with registered read addresses,
    -- does not work in this case.
    -- The code below generates three RAM blocks on the Xilinx Spartan-3,
    -- but it is doubtful whether it will work on other FPGA families.

    -- Write to RX buffer.
    process (CLK) is
    begin
        if rising_edge(CLK) then
            if s_state = ST_OUTRECV and usbt_rxrdy = '1' then
                rxbuf(to_integer(resize(s_bufptr, RXBUFSIZE_BITS))) <= usbt_rxdat;
            end if;
        end if;
    end process;

    -- Read from RX buffer.
    process (CLK) is
    begin
        if rising_edge(CLK) then
            if q_rxbuf_read = '1' then
                rxbuf_rdat <= rxbuf(to_integer(q_rxbuf_tail));
            end if;
        end if;
    end process;

    -- Write to TX buffer.
    process (CLK) is
    begin
        if rising_edge(CLK) then
            if TXVAL = '1' then
                txbuf(to_integer(q_txbuf_head)) <= TXDAT;
            end if;
        end if;
    end process;

    -- Read from TX buffer.
    process (CLK) is
    begin
        if rising_edge(CLK) then
            if (usbt_txrdy = '1') or (s_state = ST_INSTART) then
                txbuf_rdat <= txbuf(to_integer(resize(s_bufptr, TXBUFSIZE_BITS)));
            end if;
        end if;
    end process;

    -- Read from descriptor memory.
    process (CLK) is
    begin
        if rising_edge(CLK) then
            if usbc_dscrd = '1' then
                if HSSUPPORT and unsigned(usbc_dscoff) = 1 and usbc_dsctyp = "111" then
                    -- Disguise the configuration descriptor as an
                    -- other_speed_configuration descriptor.
                    descrom_raddr <= to_unsigned(DESC_OTHERSPEED_ADDR, descrom_raddr'length);
                else
                    descrom_raddr <= descrom_start + resize(unsigned(usbc_dscoff), descrom_raddr'length);
                end if;
            end if;
        end if;
    end process;
    assert to_integer(descrom_raddr) < descrom_rdat'length;
    descrom_rdat <= descrom(to_integer(descrom_raddr));

end architecture usb_serial_arch;

entity USB_WRAPPER is
    port (
      CLK            : in  std_logic;
      RST            : in  std_logic;

      RX             : out std_logic_vector(7 downto 0);
      RX_STB         : out std_logic;
      RX_ACK         : in  std_logic;

      TX             : in  std_logic_vector(7 downto 0);
      TX_STB         : in  std_logic;
      TX_ACK         : out std_logic;

      PHY_DATAIN     : in  std_logic_vector(7 downto 0);
      PHY_DATAOUT    : out std_logic_vector(7 downto 0);
      PHY_TXVALID    : out std_logic;
      PHY_TXREADY    : in  std_logic;
      PHY_RXACTIVE   : in  std_logic;
      PHY_RXVALID    : in  std_logic;
      PHY_RXERROR    : in  std_logic;
      PHY_LINESTATE  : in  std_logic_vector(1 downto 0);
      PHY_OPMODE     : out std_logic_vector(1 downto 0);
      PHY_XCVRSELECT : out std_logic;
      PHY_TERMSELECT : out std_logic;
      PHY_RESET      : out std_logic
  );
end entity USB_WRAPPER;

architecture RTL of USB is
  component usb_serial is
    generic (
      VENDORID :      std_logic_vector(15 downto 0);
      PRODUCTID :     std_logic_vector(15 downto 0);
      VERSIONBCD :    std_logic_vector(15 downto 0);
      HSSUPPORT :     boolean := false;
      SELFPOWERED :   boolean := false;
      RXBUFSIZE_BITS: integer range 7 to 12 := 11;
      TXBUFSIZE_BITS: integer range 7 to 12 := 10 );
    port (
      CLK :           in  std_logic;
      RESET :         in  std_logic;
      USBRST :        out std_logic;
      HIGHSPEED :     out std_logic;
      SUSPEND :       out std_logic;
      ONLINE :        out std_logic;
      RXVAL :         out std_logic;
      RXDAT :         out std_logic_vector(7 downto 0);
      RXRDY :         in  std_logic;
      RXLEN :         out std_logic_vector((RXBUFSIZE_BITS-1) downto 0);
      TXVAL :         in  std_logic;
      TXDAT :         in  std_logic_vector(7 downto 0);
      TXRDY :         out std_logic;
      TXROOM :        out std_logic_vector((TXBUFSIZE_BITS-1) downto 0);
      TXCORK :        in  std_logic;

      PHY_DATAIN :    in  std_logic_vector(7 downto 0);
      PHY_DATAOUT :   out std_logic_vector(7 downto 0);
      PHY_TXVALID :   out std_logic;
      PHY_TXREADY :   in  std_logic;
      PHY_RXACTIVE :  in  std_logic;
      PHY_RXVALID :   in  std_logic;
      PHY_RXERROR :   in  std_logic;
      PHY_LINESTATE : in  std_logic_vector(1 downto 0);
      PHY_OPMODE :    out std_logic_vector(1 downto 0);
      PHY_XCVRSELECT: out std_logic;
      PHY_TERMSELECT: out std_logic;
      PHY_RESET :     out std_logic 
    );
  end component usb_serial;

  type RX_STATE_TYPE is (GET_RX, PUT_RX);
  signal RX_STATE : RX_STATE_TYPE;

  type TX_STATE_TYPE is (GET_TX, ACKNOWLEDGE_TX);
  signal TX_STATE : TX_STATE_TYPE;

  signal RXVAL  : std_logic;
  signal RXDAT  : std_logic_vector(7 downto 0);
  signal RXRDY  : std_logic;
  signal TXVAL  : std_logic;
  signal TXDAT  : std_logic_vector(7 downto 0);
  signal TXRDY  : std_logic;

begin

  usb_serial_1 : usb_serial generic map(
      VENDORID       => X"0000",
      PRODUCTID      => X"0000",
      VERSIONBCD     => X"0000",
      HSSUPPORT      => false,
      SELFPOWERED    => false,
      RXBUFSIZE_BITS => 11,
      TXBUFSIZE_BITS => 10);
    port (
      CLK            => CLK,
      RESET          => RST,
      USBRST         => open,
      HIGHSPEED      => open,
      SUSPEND        => open,
      ONLINE         => open,
      RXVAL          => RXVAL,
      RXDAT          => RXDAT,
      RXRDY          => RXRDY,
      RXLEN          => open,
      TXVAL          => TXVAL,
      TXDAT          => TXDAT,
      TXRDY          => TXRDY,
      TXROOM         => open,
      TXCORK         => open,

      PHY_DATAIN     => PHY_DATAIN,
      PHY_DATAOUT    => PHY_DATAOUT,
      PHY_TXVALID    => PHY_TXVALID,
      PHY_TXREADY    => PHY_TXREADY,
      PHY_RXACTIVE   => PHY_RXACTIVE,
      PHY_RXVALID    => PHY_RXVALID,
      PHY_RXERROR    => PHY_RXERROR,
      PHY_LINESTATE  => PHY_LINESTATE,
      PHY_OPMODE     => PHY_OPMODE,
      PHY_XCVRSELECT => PHY_XCVRSELECT,
      PHY_TERMSELECT => PHY_TERMSELECT,
      PHY_RESET      => PHY_RESET);
	
  process
  begin
    wait until rising_edge(CLK);
    case RX_STATE is
      when GET_RX =>
        if RXVAL = '1' then
          RX <= RXDAT; RXRDY <= '1'; RX_STB <= '1';
          RX_STATE <= PUT_RX;
        end if;
      when PUT_RX =>
        RXRDY <= '0';
        if RX_ACK = '1' then
          RX_STB <= '0';
          RX_STATE <= GET_RX;
        end if;
    end case;
    if RST = '1' then
      RXRDY <= '0';
      RX_STB <= '0';
    end if;
  end process;

  process
  begin
    wait until rising_edge(CLK);
    case TX_STATE is
      when GET_TX =>
        if TX_STB = '1' and TX_RDY = '1' then
          TXDAT <= TX; TXVAL <= '1'; TX_ACK <= '1';
          TX_STATE <= ACKNOWLEDGE_TX;
        end if;
      when ACKNOWLEDGE_TX =>
        TXVAL <= '0'; TX_ACK <= '0';
        TX_STATE <= GET_TX;
    end case;
    if RST = '1' then
      TXVAL <= '0';
      TX_ACK <= '0';
    end if;
  end process;

end architecture RTL;
