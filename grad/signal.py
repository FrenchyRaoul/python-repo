from numpy import real, imag, ceil, array, round, sin, pi
#from numpy import round as npround

__all__ = ['padhex', 'quantize', 'hex_checksum',]

def padhex(hexint, n):
    n = int(n)
    hexint = int(hexint)
    hexstr = hex(hexint)
    return hexstr.split('0x')[1].zfill(n)

def quantize(signal, n=16, data='offset_binary'):
    if data == 'offset_binary':
        shifted = signal - min(signal)
        scale = max((max(abs(real(shifted))), max(abs(imag(shifted)))))
        sized = shifted / scale * ((2 ** n) - 1)
        quantized = round(sized)
    else:
        return None
    return quantized#.astype(int)

def hex_checksum(hexint):
    try:
        hex(hexint)
    except:
        raise Exception("Input string must be hexadecimal.")
    hexstr = hex(hexint)[2:]
    hexstr = hexstr.zfill(int(ceil(len(hexstr)/2)*2))
    total = sum((int(hexstr[i:i+2], 16) for i in range(0, len(hexstr), 2)))
    checksum = ((int(hex(total & 0xFF)[2:][-2:], 16) ^ 0xFF) + 1)
    return checksum & 0xFF

def hex_file_writer(fout, signal_array, n=16, data=4, address=2, datatype=0):
    """
    :param fout: an output steam
    :param signal_array: a numpy-like array containing real or complex signal entries
    :param n: bit-resolution of signal-array
    :param data: bytes of data per entry
    :param: address: bytes in address
    :param: datatype: Format-specific 'data-type'. Set to 00 in Binary.
    """
    newline = ''
    for ind, val in enumerate(signal_array):
        real_data = real(val)
        imag_data = imag(val)
        prestr = ''.join((padhex(data,2), padhex(ind,address*2), padhex(datatype,2),
                          padhex(real_data, n/4), padhex(imag_data, n/4)))
        outstr = prestr + padhex(hex_checksum(int(prestr,16)), 2)
        fout.write(newline + ':' + outstr.upper())
        newline = '\n'
    fout.write(newline + ':00000001FF')  # End-of-file

def csv_writer(fout, signal_array):
    newline = ''
    for ind, val in enumerate(signal_array):
        real_data = str(real(val))
        imag_data = str(imag(val))
        fout.write(newline + real_data.upper() + ',' + imag_data.upper())
        newline = '\r\n'

def create_sin_signal(sig_freq, samp_freq, addr_bits):
    time = array(range(0,2**addr_bits,1)) * 1/samp_freq
    return array(sin(2 * pi * sig_freq * time))