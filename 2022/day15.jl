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

#precalculate distances - doesnt help much
sensor_with_dist::Array{Tuple{Int64, Int64, Int64}} = [] #but typing does! Copied from martinjonas
for (sensor, beacon) in parsed
    push!(sensor_with_dist, (sensor[1], sensor[2], cityblock(sensor, beacon)))
end


function get_blocked(the_row)
    row_blocked::Array{Tuple{Int64, Int64}} = []
    for (s1, s2, D) in sensor_with_dist
        Dy = abs(the_row - s2)
        if Dy > D
            continue
        end
        num_blocked = D - Dy
        push!(row_blocked, (s1-num_blocked, s1+num_blocked))
    end
    sort!(row_blocked, by= x -> x[1])
    b1, b2 = row_blocked[1]
    overlapped::Array{Tuple{Int64, Int64}} = []
    for (x1, x2) in row_blocked
        if x1 > b2 
            push!(overlapped, (b1, b2))
            b1, b2 = x1, x2
        else
            b2 = max(x2, b2)
        end
    end
    push!(overlapped, (b1, b2))
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
@time part02()
