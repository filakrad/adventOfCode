using Profile

loaded = read("./day17.txt", String)
jets_num = length(loaded)

rocks = [
    Dict("positions"=>((0, 0), (1, 0), (2, 0), (3, 0)),
         "height" => 1, 
         "width" => 4
        ),
    Dict("positions"=>((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
        "height" => 3,
        "width" => 3
    ),
    Dict("positions"=>((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        "height" => 3,
        "width" => 3
    ),
    Dict("positions"=>((0, 0), (0, 1), (0, 2), (0, 3)),
        "height" => 4,
        "width" => 1
    ),
    Dict("positions"=>((0, 0), (0, 1), (1, 0), (1, 1)),
        "height" => 2,
        "width" => 2
    )    
]

directions = Dict('<' => -1, '>' => 1)

function side_push(rock, pos, field, dirchar)
    for p in rock["positions"]
        newx = pos[1] + p[1] + directions[dirchar]
        if newx < 1 || newx > 7 || field[p[2]+pos[2]][newx] == 1
            return pos
        end
    end
    return (pos[1] + directions[dirchar], pos[2])
end

function down_push(rock, pos, field)
    for p in rock["positions"]
        newy = pos[2] + p[2] - 1
        if field[newy][pos[1]+p[1]] == 1
            return true, pos
        end
    end
    return false, (pos[1], pos[2] - 1)
end

function rock_fall(rock_idx, jet_idx, field)
    rock = rocks[rock_idx]
    xpos = 3
    for _ in 1:3
        dir = directions[loaded[jet_idx]]
        jet_idx = mod(jet_idx + 1, 1:jets_num)
        xpos += dir
        if xpos == 0 || 8 == xpos + rock["width"] - 1
            xpos -= dir
        end
    end
    max_height = length(field)
    position = (xpos, length(field) + 1)
    for _ in 1:rock["height"] + 0
        push!(field, [0 for _ in 1:7])
    end
    fallen = false
    while ! fallen
        position = side_push(rock, position, field, loaded[jet_idx])
        jet_idx = mod(jet_idx + 1, 1:jets_num)
        fallen, position = down_push(rock, position, field)
        if ! fallen && length(field) > max_height
            pop!(field)
        end
    end
    added = Set()
    for p in rock["positions"]
        field[p[2]+position[2]][p[1]+position[1]] = 1
        push!(added, p[2]+position[2])
    end

    return field, jet_idx, added
end


function get_top_heights(field)
    tops::Array{Union{Int, Nothing}} = [nothing for _ in 1:7]
    for (i, row) in enumerate(reverse(field))
        for (j, v) in enumerate(row)
            if v == 1 && tops[j] === nothing
                tops[j] = i
            end
        end
        if all(tops .!== nothing)
            break
        end
    end
    return tops
end


function part01(n)
    field::Array{Array{Int}} = [[1 for _ in 1:7]]
    jet_index = 1
    total = 0
    known = Dict()
    for i in 1:n
        rock_index = mod(i, 1:5)
        field, jet_index, added = rock_fall(rock_index, jet_index, field)
        for a in added
            if all(field[a] .== 1)
                total += a - 1
                field = field[a:end]
                break
            end
        end
        new_key = (rock_index, jet_index, string(get_top_heights(field)))
        curr_height = total + length(field) - 1
        if haskey(known, new_key)
            cycle_length = i - known[new_key][2]
            cycle_height = curr_height - known[new_key][1]
            unfinished_cycles = n - i
            skipped_cycles = unfinished_cycles ÷ cycle_length
            to_finish = mod(unfinished_cycles, cycle_length)
            total += skipped_cycles * cycle_height
            # println("found cycle on length $i, $cycle_length, $start_length, $(known[new_key])")
            # println("found cycle on height $curr_height, $cycle_height, $start_height")
            # println("skipped $skipped_cycles, $to_finish, $skip_height")
            for j in 1:to_finish
                rock_index = mod(i+j, 1:5)
                field, jet_index, added = rock_fall(rock_index, jet_index, field)
            end
            break
        else
            known[new_key] = (curr_height, i)
        end
    end
    return total + length(field) - 1
end


println(part01(2022))
@time println(part01(1000000000000))