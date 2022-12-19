loaded = read("./day16.txt", String)
rows = split(loaded, "\n")

int = x -> parse(Int, x)

parsed = Dict()

for row in rows
    p = match(r"Valve ([A-Z]+) has flow rate=(\d+);[a-z ]+([A-Z]+(, [A-Z]+)*)", row) |> x -> [x[1], int(x[2]), split(x[3], ", ")]
    parsed[p[1]] = [p[2], p[3], 0, false] # value, neighbors, visited, opened
end

function next_valve(parent, name, ticks, rate, total)
   
    # println("$parent -> $name, $ticks, $rate, $total, $(parsed[name][3])")
    if parsed[name][3] > 3
        return total
    end

    if ticks == -1
        return total
    end

    parsed[name][3] += 1

    old_total = total
    for next_name in parsed[name][2]
        if parsed[name][1] > 0 && ticks > 0 && !parsed[name][4]
            parsed[name][4] = true
            total = max(total, next_valve(name, next_name, ticks-2, rate+parsed[name][1], old_total + 2*rate))
            parsed[name][4] = false
        end
        if parent == next_name
            continue
        end
        total = max(total, next_valve(name, next_name, ticks-1, rate, old_total + rate))
    end
    parsed[name][3] -= 1
    return total
end


function part01()
    return next_valve("None","AA", 30, 0, 0)#slow
end

# println(part01())