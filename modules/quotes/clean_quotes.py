import sys;
import json;
import copy;

if __name__ == "__main__":
    file_input_name = sys.argv[1];
    file_output_name = sys.argv[2];
    dic_file = []
    try:
        with open(file_input_name, "r") as f:
            dic_file = json.loads(f.read())
    except IOError as err:
        print(err);
    nb_del = 0;
    i=0;
    previous_len = len(dic_file);
    for _ in range(previous_len):
        if dic_file[i]["body"]=="":
            dic_file.pop(i);
            nb_del+=1;
        else:
            i+=1;
    print("Nb Deleted Items: {} over {}.".format(nb_del, previous_len));
    try:
        with open(file_output_name, "w") as f:
            f.write(json.dumps(dic_file))
    except IOError as err:
        print(err);
