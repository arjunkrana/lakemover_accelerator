def dual_write(
    source_writer,
    lakebase_writer,
    data
):

    source_writer(data)

    lakebase_writer(data)

    print(
        "Dual write completed"
    )