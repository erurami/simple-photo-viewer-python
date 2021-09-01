def csv_to_dic(csv_file, return_type = "dic"):
    rows_splited_csv_file = csv_file.split("\n")
    listed_csv = []
    for row in rows_splited_csv_file:
        listed_csv.append(row.split(","))
    if return_type == "dic":
        dicted_csv = {}
        for row in listed_csv:
            dicted_csv[row[0]] = ",".join(row[1:])
        return dicted_csv
    elif return_type == "list":
        return listed_csv
