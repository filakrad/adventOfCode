# import Pkg
# Pkg.add("JSON")

import JSON

loaded = read("./day13.txt", String)
pairs = split(loaded, "\n\n")


function compare(left, right)
    if typeof(left) == Int && typeof(right) == Int
        if left == right
            return 0
        elseif left < right
            return 1
        else
            return 2
        end
    elseif typeof(left) == Vector{Any} && typeof(right) == Int
        return compare(left, [right])
    elseif typeof(left) == Int && typeof(right) == Vector{Any}
        return compare([left], right)
    else
        if length(left) == 0 && length(right) == 0
            return 0
        elseif length(left) == 0
            return 1
        elseif length(right) == 0
            return 2
        else
            x = compare(left[1], right[1])
            if x > 0 
                return x
            else
                lleft = copy(left)
                rright = copy(right)
                popfirst!(lleft)
                popfirst!(rright)
                return compare(lleft, rright)
            end
        end
    end
end


function part01()
    total = 0
    for (i, p) in enumerate(pairs)
        l, r = split(p, "\n")
        right = JSON.parse(r)
        left = JSON.parse(l)
        x = compare(left, right)
        if x == 0
            println("$left, $right")
        elseif x == 1
            total += i
        end
    end
    return total
end


function own_isless(left, right)
    return compare(left, right) == 1
end


function part02()
    all_packets = []
    start = [[2]]
    ending = [[6]]
    push!(all_packets, start)
    push!(all_packets, ending)
    for p in pairs
        l, r = split(p, "\n")
        right = JSON.parse(r)
        left = JSON.parse(l)
        push!(all_packets, left)
        push!(all_packets, right)
    end
    sort!(all_packets, lt=own_isless)

    s = findfirst(x -> x==start, all_packets)
    e = findfirst(x -> x==ending, all_packets)

    return s*e
end


println(part01())
println(part02())

