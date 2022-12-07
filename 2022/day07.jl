
loaded = read("./day07.txt", String)
lines = split(loaded, "\n")


function get_dir_dict()
    # Create dictionary (directory_path => size)
    current = "/"
    dirs = Dict(current => 0)
    for line in lines
        line_parts = split(line, " ")
        if startswith(line, "\$ cd ..")
            curr_vec = split(current, "/")
            current = join(curr_vec[1:end-1], "/")
        elseif startswith(line, "\$ cd /")
            current = "/"
        elseif startswith(line, "\$ cd")
            current *= "/" * line_parts[3]
        elseif startswith(line, "\$ ls")
            nothing
        elseif startswith(line, "dir")
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
    best_value = needed
    for (k, v) in dirs
        if to_clean < v < best_value
            best_value = v
        end
    end
    return best_value
end


println(part01())
println(part02())