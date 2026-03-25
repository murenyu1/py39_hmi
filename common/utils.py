def decode_data(bytes_arr: bytes) -> str:
    try:
        msg = bytes_arr.decode("UTF-8")
    except Exception as e:
        msg = bytes_arr.decode("GBK")
        
    return msg