def handle_uploaded_file(f, dest):
    print('handle xlsx and csv')
    # import column matching function
    from src.vars_text_match import ms_raw_column_reader
    print(ms_raw_column_reader.__doc__)

    with open(dest, 'wb') as d:
        for chunk in f.chunks():
            # writing chunk to standard raw data destination
            d.write(chunk)
            # run macrosheds variable matching function on input data
            matches = ms_raw_column_reader(dest)
            print(matches)
            return(matches)
