# import Pkg
# Pkg.add("Distances")

using Distances

loaded = read("./day15.txt", String)
rows = split(loaded, "\n")

int = x -> parse(Int, x)

parsed = []

for row in rows
    pairs = match(r"Sensor at x=([\-]?\d+), y=([\-]?\d+): closest beacon is at x=([\-]?\d+), y=([\-]?\d+)", row) |> x -> [[int(x[1]), int(x[2])], [int(x[3]), int(x[4])]]
    push!(parsed, pairs)
end

function get_blocked(the_row)
    row_blocked = []
    for (sensor, beacon) in parsed
        D = cityblock(sensor, beacon)
        Dy = cityblock([sensor[1], the_row], sensor)
        if Dy > D
            continue
        end
        num_blocked = D - Dy
        push!(row_blocked, [sensor[1]-num_blocked, sensor[1]+num_blocked])
    end
    sort!(row_blocked, by= x -> x[1])
    b1, b2 = row_blocked[1]
    overlapped = []
    for (x1, x2) in row_blocked
        if x1 > b2 
            push!(overlapped, [b1, b2])
            b1, b2 = x1, x2
        else
            b2 = max(x2, b2)
        end
    end
    push!(overlapped, [b1, b2])
    return overlapped
end

function part01()
    blocked = get_blocked(2000000)
    total = 0
    for (x1, x2) in blocked
        total += x2-x1
    end
    return total
end

function part02()
    y = 0
    blocked = nothing
    for i in 1:4000000
        blocked = get_blocked(i)
        if length(blocked) > 1
            y = i
            break
        end
    end
    
    x = blocked[1][2] + 1
    return 4000000*x + y
end

println(part01())
println(part02())
