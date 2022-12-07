
loaded = read("./day07.txt", String)
lines = split(loaded, "\n")

function get_dir_dict()
    current = "/"
    dirs = Dict(current => 0)
    for line in lines
        line_parts = split(line, " ")
        if line_parts[1] == "\$"
            if line_parts[2] == "cd"
                if line_parts[3] == ".."
                    curr_vec = split(current, "/")
                    current = join(curr_vec[1:end-1], "/")
                    if current == ""
                        current = "/"
                    end
                elseif line_parts[3] == "/"
                    current = "/"
                    continue
                else
                    current *= "/" * line_parts[3]
                end
            elseif line_parts[2] == "ls"

            end
        elseif line_parts[1] == "dir"
            dirs[current * "/" * line_parts[2]] = 0
        else
            path = split(current, "/")
            num = parse(Int, line_parts[1])
            while length(path) > 1
                dirs[join(path, "/")] += num
                pop!(path)
            end
        end

    end

    return dirs
end

function part01()
    dirs = get_dir_dict()
    total = 0
    for (k, v) in dirs
        if v < 100000
            total += v
        end
    end
    return total
end

function part02()
    dirs = get_dir_dict()
    max = 70000000
    needed = 30000000
    current_space = max - dirs["/"]
    to_clean = needed - current_space
    possible_value = max
    for (k, v) in dirs
        if v > to_clean && v < possible_value
            possible_value = v
        end
    end
    return possible_value
end


println(part01())
println(part02())