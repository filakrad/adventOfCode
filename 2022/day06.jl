loaded = read("./day06.txt", String)


function parts(expected_length)
    p_end = expected_length

    while true
        data = loaded[p_end-(expected_length-1):p_end]
        data_set = Set(data)
        if length(data_set) == expected_length
            break
        end
        p_end += 1
    end
    return p_end
end

println(parts(4))
println(parts(14))