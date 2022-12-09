loaded = read("./day09.txt", String)
lines = split(loaded, "\n")

directions = Dict("L" => [-1, 0],
                  "R" => [1, 0],
                  "U" => [0, 1],
                  "D" => [0, -1],
)

function move_tail(head, tail)
    dist_x, dist_y = head[1] - tail[1], head[2] - tail[2]
    if abs(dist_x) <= 1 && abs(dist_y) <= 1
        return
    elseif dist_x == 0
        tail[2] += sign(dist_y)
    elseif dist_y == 0
        tail[1] += sign(dist_x)
    else
        tail[2] += sign(dist_y)
        tail[1] += sign(dist_x)
    end
end

function part01()
    head = [0, 0]
    tail = [0, 0]
    visited = Set()
    push!(visited, "$tail")

    for line in lines
        direction, steps = split(line, " ")
        steps = parse(Int, steps)
        for _ in 1:steps
            head[1] += directions[direction][1]
            head[2] += directions[direction][2]
            move_tail(head, tail)
            push!(visited, "$tail")
        end
    end

    return length(visited)
end

function part02()
    knots = [[0, 0] for _ in 1:10]
    visited = Set()
    push!(visited, "$(knots[10])")

    for line in lines
        direction, steps = split(line, " ")
        steps = parse(Int, steps)
        for _ in 1:steps
            knots[1][1] += directions[direction][1]
            knots[1][2] += directions[direction][2]
            for i in 1:9
                move_tail(knots[i], knots[i+1])
            end
            push!(visited, "$(knots[10])")
        end
    end

    return length(visited)
end

println(part01())
println(part02())