loaded = read("./day18.txt", String)
rows = split(loaded, "\n")

int = x ->  parse(Int, x)

the_max = 0
the_min = 123645894
coords = []
for row in rows
    r = split(row, ',') .|> int
    push!(coords, r)
    cmax = maximum(r)
    cmin = minimum(r)
    global the_max = max(the_max, cmax)
    global the_min = min(the_min, cmin)
end

for c in coords
    c .+= 1-the_min
end
the_max += 1-the_min

M = zeros(Int, the_max, the_max, the_max)

for c in coords
    M[c[1], c[2], c[3]] = 1
end

function part01(M)
    total = 0
    for row in coords
        for dir in 1:3
            if dir == 1
                if row[1] == the_max
                    total += 1
                elseif M[row[1] + 1, row[2], row[3]] == 0
                    total += 1
                end
                if row[1] == 1
                    total += 1
                elseif M[row[1] - 1, row[2], row[3]] == 0
                    total += 1
                end
            elseif dir == 2
                if row[2] == the_max
                    total += 1
                elseif M[row[1], row[2] + 1, row[3]] == 0
                    total += 1
                end
                if row[2] == 1
                    total += 1
                elseif M[row[1], row[2] - 1, row[3]] == 0
                    total += 1
                end
            else
                if row[3] == the_max
                    total += 1
                elseif M[row[1], row[2], row[3] + 1] == 0
                    total += 1
                end
                if row[3] == 1
                    total += 1
                elseif M[row[1], row[2], row[3] - 1] == 0
                    total += 1
                end
            end
        end
    end
    return total
end

part01(M)

function part02(input)
    M = copy(input)
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    
end
    