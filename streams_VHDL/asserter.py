import common

def write(stream):

    identifier = stream.a.get_identifier()
    bits = stream.a.get_bits()

    ports = [
    ]

    declarations = [
    ]

    definitions = [
    "  --Asserter({0})".format(identifier),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier),
    "    if STREAM_{0}_STB = '1' and STREAM_{0}_ACK = '0' then".format(identifier),
    "      assert(STREAM_{0} /= {1}) severity failure;".format(identifier, common.binary(0, bits)),
    "      STREAM_{0}_ACK <= '1';".format(identifier),
    "    end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
