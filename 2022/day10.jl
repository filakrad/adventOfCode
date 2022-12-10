loaded = read("./day10.txt", String)
lines = split(loaded, "\n")

function part01()
    cycle = 0
    register = 1
    result = 0
    result_indicator = 0

    for line in lines
        old_indicator = result_indicator
        if startswith(line, "noop")
            cycle += 1
            to_register = 0
        else
            cycle += 2
            to_register = parse(Int, split(line, " ")[2])
        end
        result_indicator = mod(20 + cycle, 40)
        if result_indicator < old_indicator
            result += register * (cycle - result_indicator)
        end
        register += to_register
    end

    return result
end

function part02()
    cycle = 0
    register = 1
    result = zeros(Int, 6, 40)
    for line in lines
        if startswith(line, "noop")
            to_register = 0
            cycles = 1
        else
            to_register = parse(Int, split(line, " ")[2])
            cycles = 2
        end

        for _ in 1:cycles
            cycle += 1
            position = mod(cycle, 1:40)
            if register in (position-2):(position+0)
                result[cycle ÷ 40 + 1, position] = 1
            end
        end
        register += to_register
    end
    return result
end


println(part01())
part02()
