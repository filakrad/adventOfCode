# import Pkg
# Pkg.add("Pipe")

using Pipe: @pipe

loaded = read("./day08.txt", String)
lines = (@pipe split(loaded, "\n") .|> split(_, ""))

parsed = []

for line in lines
    push!(parsed, @pipe line .|> parse(Int, _))
end

function set_visible(m, visib, i, j)
    small_tree = -1
    for v in arr
        if v > small_tree
            visible[i][j] = true
            small_tree = v
        else
            break
        end
    end
end

function part01()
    matrix = mapreduce(permutedims, vcat, parsed)
    visible = falses(length(matrix[:, 1]), length(matrix[1, :]))
    for i in 1:length(matrix[:, 1])
        small_tree = -1
        for j in 1:length(matrix[1, :])
            if matrix[i, j] > small_tree
                visible[i, j] = true
                small_tree = matrix[i, j]
            end
        end
        small_tree = -1
        for j in reverse(1:length(matrix[1, :]))
            if matrix[i, j] > small_tree
                visible[i, j] = true
                small_tree = matrix[i, j]
            end
        end
    end
    for i in 1:length(matrix[1, :])
        small_tree = -1
        for j in 1:length(matrix[:, 1])
            if matrix[j, i] > small_tree
                visible[j, i] = true
                small_tree = matrix[j, i]
            end
        end
        small_tree = -1
        for j in reverse(1:length(matrix[:, 1]))
            if matrix[j, i] > small_tree
                visible[j, i] = true
                small_tree = matrix[j, i]
            end
        end
    end
    # return visible
    return sum(visible)
end

function get_direction_score(matrix, i, j, direction)
    tree_height = matrix[i, j]
    ii = i
    jj = j
    max_i = length(matrix[:, 1])
    max_j = length(matrix[1, :])
    view_distance = 0
    while true
        ii += direction[1]
        jj += direction[2]
        if ii < 1 || jj < 1 || ii > max_i || jj > max_j
            break
        end
        view_distance += 1
        if matrix[ii, jj] >= tree_height
            break
        end 
    end
    return view_distance
end

function part02()
    matrix = mapreduce(permutedims, vcat, parsed)
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    max_score = 0
    for i in 1:length(matrix[:, 1])
        for j in 1:length(matrix[1, :])
            scenic_score = 1
            for direction in directions 
                scenic_score *= get_direction_score(matrix, i, j, direction)
            end
            max_score = max(max_score, scenic_score)
        end
    end
    return max_score
end


println(part01())
println(part02())