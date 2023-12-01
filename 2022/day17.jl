

jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

rocks = (
    Dict("widths" => [4], "heights" => [1, 1, 1, 1], "max_width" => 4, "max_height" => 1),
    Dict("widths" => [1, 3, 1], "heights" => [1, 3, 1], "max_width" => 3, "max_height" => 3),
    Dict("widths" => [1, 1, 3], "heights" => [1, 1, 3], "max_width" => 3, "max_height" => 3),
    Dict("widths" => [1, 1, 1, 1], "heights" => [4], "max_width" => 1, "max_height" => 4),
    Dict("widths" => [2, 2], "heights" => [2, 2], "max_width" => 2, "max_height" => 2)
)

function fall_rock(heights, rock_count, field, moves)
    bottom = maximum(heights)
    rock = rocks[mod(rock_count, 1:length(rocks))]
    for _ in 1:3
        field = vcat([0, 0, 0, 0, 0, 0, 0]', field)
    end
    is_down = false
    while ! is_down
        jet = jets[mod(moves, 1:length(jets))]
        moves += 1
        move_sideways(jet, )
    end
end


function part01()
    field = ones(Int, 1, 7)
    heights = [0 for _ ∈ 1:7]
    moves = 1
    for r in 1:2022
        moves = fall_rock(heights, r, field, moves)
    end
    return max(heights)
end
