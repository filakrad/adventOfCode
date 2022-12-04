# import Pkg
# Pkg.add("Pipe")

using Pipe: @pipe

loaded = read("./day04.txt", String)
lines = split(loaded, "\r\n")

function part01()
    bad_lines = 0
    for line in lines
        p = (@pipe split(line, ',') .|> split(_, "-") |> Iterators.flatten .|> parse(Int, _))
        if (p[1] <= p[3] && p[2] >= p[4]) || (p[3] <= p[1] && p[4] >= p[2])
            bad_lines += 1
        end
    end
    return bad_lines
end

println(part01())

function part02()
    bad_lines = 0
    for line in lines
        p = (@pipe split(line, ',') .|> split(_, "-") |> Iterators.flatten .|> parse(Int, _))
        size1 = (p[2] - p[1]) + 1 + (p[4] - p[3]) + 1
        size2 = length( Set(p[1]:p[2]) ∪ Set(p[3]:p[4]) )
        if size1 != size2
            bad_lines += 1
        end
    end
    return bad_lines
end

println(part02())