
FILE_NAME = "day01.txt"

function read_file(file_name)
    arr = []
    f = open(file_name, "r")
        line = readline(f)
        append!(arr, line)
    close(f)
    return arr
end

x = read_file("day01.txt")
print(x)