loaded = read("./day14.txt", String)
rows = split(loaded, "\n")

int = x-> parse(Int, x)

all_walls = Set()

for row in rows
    borders = split(row, "->")
    for pair in zip(borders[1:end], borders[2:end])
        p1_x, p1_y = split(pair[1], ",") .|> int
        p2_x, p2_y = split(pair[2], ",") .|> int
        pts = Iterators.product(min(p1_x, p2_x):max(p1_x, p2_x), min(p1_y, p2_y):max(p1_y, p2_y)) |> collect
        for p in pts
            push!(all_walls, p)
        end
    end
end

min_x = minimum(x -> x[1], all_walls)
max_x = maximum(x -> x[1], all_walls)
min_y = 0
max_y = maximum(x -> x[2], all_walls)

source = 500, 0

x_pos = x -> x - min_x + 1
y_pos = x -> x - min_y + 1

field = zeros(Int, y_pos(max_y), x_pos(max_x))

for wall in all_walls
    field[y_pos(wall[2]), x_pos(wall[1])] = 1
end
field[y_pos(source[2]), x_pos(source[1])] = 2

dirs = [[0, 1], [-1, 1], [1, 1]]

function sand_fall(current_field::Matrix)
    new_pos = x_pos(source[1]), y_pos(source[2])
    old_pos = 0, 0
    while new_pos != old_pos
        old_pos = new_pos
        for d in dirs
            new_test = d[1] + old_pos[1], d[2] + old_pos[2]
            if !(x_pos(min_x) <= new_test[1] <= x_pos(max_x) && y_pos(min_y) <= new_test[2] <= y_pos(max_y))
                return new_test
            end
            if current_field[new_test[2], new_test[1]] == 0
                new_pos = new_test
                break
            end
        end
    end
    return new_pos
end

function part01()
    current_field = copy(field)
    sands = 0
    sand = nothing
    while true 
        sand = sand_fall(current_field)
        if !(x_pos(min_x) <= sand[1] <= x_pos(max_x) && y_pos(min_y) <= sand[2] <= y_pos(max_y))
            break
        end
        current_field[sand[2], sand[1]] = 2
        sands += 1
    end
    return sands
end

println(part01())


function sand_fall(walls::Set)
    new_pos = source
    old_pos = 0, 0
    while new_pos != old_pos
        old_pos = new_pos
        for d in dirs
            new_test = d[1] + old_pos[1], d[2] + old_pos[2]
            if new_test[2] > max_y+1
                return old_pos
            end
            if ! (new_test ∈ walls)
                new_pos = new_test
                break
            end
        end
    end
    return new_pos
end

function part02()
    walls = copy(all_walls)
    sand = 0, 0
    sands = 0
    while sand != source
        sand = sand_fall(walls)
        push!(walls, sand)
        sands += 1
    end
    return sands
end

println(part02())

