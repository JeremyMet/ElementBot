import re;
import sys;

if __name__ == "__main__":
    input_name = sys.argv[1];
    output_name = sys.argv[2];
    with open(input_name, "r") as f_in, open(output_name, "w") as f_out:
        input_size = output_size = 0;
        for line in f_in:
            input_size+=1;
            if re.fullmatch("^[a-z]+\\n$", line):
                output_size+=1;
                f_out.write(line);
    print("Done")
    print("Input File Nb Words: {}.".format(input_size))
    print("Output File Nb Words: {}.".format(output_size))
