function read_file(file_name)
    arr = []
    open(file_name, "r") do f
        while ! eof(f)
            line = readline(f)
            partial_sum = 0
            while ! isempty(line)
                partial_sum += parse(Int64, line)
                line = readline(f)
            end
            append!(arr, partial_sum)
        end
    end
    return arr
end

x = read_file("day01.txt")
println(maximum(x))


sort!(x, rev=true)
println(sum(x[1:3]))