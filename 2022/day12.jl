loaded = read("./day12.txt", String)
lines = split(loaded, "\n")

directions = [[-1, 0],[1, 0],[0, 1],[0, -1]]

function get_starting_position(symbol)
    for i in 1:length(lines)
        for j in 1:length(lines[1])
            if lines[i][j] == symbol
                return (i, j)
            end
        end
    end
end

function part01()
    visited = Dict()
    starting = get_starting_position('S')
    visited[starting] = 0
    y_size = length(lines[1])
    x_size = length(lines)
    while true
        for (k, v) in visited
            for dir in directions
                new_x, new_y = k[1] + dir[1], k[2] + dir[2]
                if haskey(visited, (new_x, new_y))
                    continue
                end
                if 1 <= new_x <= x_size && 1 <= new_y <= y_size
                    if lines[new_x][new_y] == 'E' && (lines[k[1]][k[2]] == 'z' || lines[k[1]][k[2]] == 'y')
                        return v+1
                    elseif lines[k[1]][k[2]] - lines[new_x][new_y] >= -1 && lines[new_x][new_y] != 'E'
                        visited[(new_x, new_y)] = v+1
                    elseif lines[k[1]][k[2]] == 'S' && ( lines[new_x][new_y] == 'a' || lines[new_x][new_y] == 'b') 
                        visited[(new_x, new_y)] = v+1
                    end
                end
            end
        end
    end
end

function part02()
    visited = Dict()
    starting = get_starting_position('E')
    visited[starting] = 0
    y_size = length(lines[1])
    x_size = length(lines)
    while true
        for (k, v) in visited
            for dir in directions
                new_x, new_y = k[1] + dir[1], k[2] + dir[2]
                # println("$new_x, $new_y, $i")
                if haskey(visited, (new_x, new_y))
                    continue
                end
                if 1 <= new_x <= x_size && 1 <= new_y <= y_size
                    # println("$new_x, $new_y, $(lines[k[1]][k[2]]), $(lines[new_x][new_y])")
                    if lines[k[1]][k[2]] == 'E' && (lines[new_x][new_y] == 'z' || lines[new_x][new_y] == 'y')
                        visited[(new_x, new_y)] = v+1
                    elseif lines[k[1]][k[2]] == 'b' && lines[new_x][new_y] == 'a' 
                        return v+1
                    elseif lines[k[1]][k[2]] - lines[new_x][new_y] <= 1 && lines[k[1]][k[2]] != 'E'
                        visited[(new_x, new_y)] = v+1
                        # println("$(lines[k[1]][k[2]] - lines[new_x][new_y]), $visited")
                    end
                end
            end
        end
    end
end

# 'z' - 'x'
#  'x' - 'E'
# 'a' - 1
println(part01())
println(part02())

