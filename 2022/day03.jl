
loaded = read("./day03.txt", String)
lines = split(loaded, "\r\n")

first_lower_char = Int('a')
first_upper_char = Int('A')

function get_score(score_char)
    if islowercase(score_char)
        return Int(score_char) - first_lower_char + 1
    else
        return Int(score_char) - first_upper_char + 27
    end
end


function star01()
    score = 0
    for line in lines
        midpoint = length(line) ÷ 2
        common = Set(line[1:midpoint]) ∩ Set(line[midpoint+1:end])
        error_type = pop!(common)
        score += get_score(error_type)
    end
    return score
end

println(star01())

function star02()
    score = 0
    for i = 1:3:length(lines)
        common = Set(lines[i]) ∩ Set(lines[i+1]) ∩ Set(lines[i+2])
        common_char = pop!(common)
        score += get_score(common_char)
    end
    return score
end

println(star02())